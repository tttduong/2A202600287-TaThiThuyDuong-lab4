from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from tools import search_flights, search_hotels, calculate_budget
from config import MODEL_NAME, SYSTEM_PROMPT_PATH, VERBOSE
from dotenv import load_dotenv

load_dotenv()

# 1. Đọc System Prompt
try:
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    print(f"❌ Lỗi: Không tìm thấy {SYSTEM_PROMPT_PATH}")
    exit(1)

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
try:
    llm = ChatOpenAI(model=MODEL_NAME)
    llm_with_tools = llm.bind_tools(tools_list)
    if VERBOSE:
        print(f"✅ Initialized LLM: {MODEL_NAME}")
except Exception as e:
    print(f"❌ Lỗi khởi tạo LLM: {str(e)}")
    exit(1)

# 4. Agent Node with Error Handling
def agent_node(state: AgentState):
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    try:
        response = llm_with_tools.invoke(messages)
        
        # === LOGGING ===
        if VERBOSE and response.tool_calls:
            for tc in response.tool_calls:
                print(f"🔧 Tool: {tc['name']}({tc['args']})")
        elif VERBOSE:
            print(f"💬 Direct response (no tools needed)")
        
        return {"messages": [response]}
    
    except Exception as e:
        print(f"❌ Lỗi agent: {str(e)}")
        error_msg = HumanMessage(content=f"❌ Xin lỗi, có lỗi xảy ra: {str(e)}")
        return {"messages": [error_msg]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# --- Khai báo edges ---
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌍 TravelBuddy - Trợ Lý Du Lịch Thông Minh")
    print("=" * 60)
    print("💡 Gõ 'quit' hoặc 'exit' để thoát")
    print("=" * 60 + "\n")
    
    while True:
        try:
            user_input = input("👤 Bạn: ").strip()
            if user_input.lower() in ("quit", "exit", "q"):
                print("👋 Cảm ơn bạn đã sử dụng TravelBuddy. Chúc bạn có một chuyến đi vui vẻ!")
                break
            
            if not user_input:
                print("⚠️  Vui lòng nhập câu hỏi của bạn.\n")
                continue
                
            if VERBOSE:
                print("\n⏳ TravelBuddy đang suy nghĩ...")
            
            try:
                result = graph.invoke({"messages": [("human", user_input)]})
                final = result["messages"][-1]
                print(f"\n🤖 TravelBuddy: {final.content}\n")
            except Exception as e:
                print(f"❌ Lỗi khi xử lý: {str(e)}\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}\n")