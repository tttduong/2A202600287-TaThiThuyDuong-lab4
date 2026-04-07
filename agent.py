"""
Core agentic loop for TravelBuddy.
Uses OpenAI gpt-4o with function calling.
"""
import json
import os
from openai import OpenAI
from tools import TOOL_DEFINITIONS, dispatch_tool
from prompts import SYSTEM_PROMPT

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-4o"


def run_agent_turn(conversation_history: list) -> tuple[str, list]:
    """
    Execute one full agentic turn (may involve multiple tool calls).
    Returns (final_text_response, updated_history).

    History format: list of OpenAI message dicts.
    """
    messages = conversation_history.copy()

    iteration = 0
    max_iterations = 20  # safety guard

    while iteration < max_iterations:
        iteration += 1

        response = client.chat.completions.create(
            model=MODEL,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            temperature=0.3,
        )

        msg = response.choices[0].message

        # Convert to serializable dict for history storage
        assistant_msg = {"role": "assistant", "content": msg.content or ""}
        if msg.tool_calls:
            assistant_msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ]

        messages.append(assistant_msg)

        # No tool calls → Claude is done
        if not msg.tool_calls:
            return msg.content or "", messages

        # Process all tool calls
        for tc in msg.tool_calls:
            tool_name = tc.function.name
            try:
                tool_args = json.loads(tc.function.arguments)
            except json.JSONDecodeError:
                tool_args = {}

            # Display to user
            print(f"\n  🔧 Đang gọi: {tool_name}")
            _print_args_summary(tool_name, tool_args)

            # Execute
            try:
                result = dispatch_tool(tool_name, tool_args)
                result_str = json.dumps(result, ensure_ascii=False, indent=2)
                _print_result_summary(tool_name, result)
            except Exception as e:
                result_str = json.dumps({"error": str(e)}, ensure_ascii=False)
                print(f"  ❌ Lỗi: {e}")

            # Each tool result is a separate message with role "tool"
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result_str,
            })

    # Max iterations reached
    return "Xin lỗi, quá trình xử lý mất quá nhiều bước. Vui lòng thử lại.", messages


def _print_args_summary(tool_name: str, args: dict) -> None:
    """Print a concise summary of tool arguments."""
    summaries = {
        "search_flights": lambda a: f"     {a.get('origin_city')} → {a.get('destination_city')} | {a.get('departure_date')} | {a.get('num_passengers', 1)} khách",
        "search_hotels": lambda a: f"     {a.get('city')} | {a.get('check_in_date')} → {a.get('check_out_date')}",
        "check_budget": lambda a: f"     Ngân sách: ${a.get('total_budget_usd')} | Bay: ${a.get('planned_flight_cost', 0)} | KS: ${a.get('planned_hotel_cost', 0)}",
        "optimize_trip": lambda a: f"     Điểm đến: {a.get('destination')} | {a.get('trip_dates', {}).get('num_nights')} đêm",
    }
    fn = summaries.get(tool_name)
    if fn:
        try:
            print(fn(args))
        except Exception:
            pass


def _print_result_summary(tool_name: str, result: dict) -> None:
    """Print a concise summary of tool result."""
    if "error" in result:
        print(f"  ❌ {result['error']}")
        return

    if tool_name == "search_flights":
        opts = result.get("options", [])
        print(f"  ✅ Tìm thấy {len(opts)} chuyến bay | Rẻ nhất: ${result.get('cheapest_total_usd', '?')} ({result.get('cheapest_airline', '')})")
    elif tool_name == "search_hotels":
        opts = result.get("options", [])
        print(f"  ✅ Tìm thấy {len(opts)} khách sạn tại {result.get('city', '')} | Từ ${result.get('cheapest_per_night_usd', '?')}/đêm")
    elif tool_name == "check_budget":
        print(f"  ✅ Còn lại: ${result.get('remaining_usd', '?')} | Trạng thái: {result.get('budget_status_emoji', '')} {result.get('budget_status', '')}")
    elif tool_name == "optimize_trip":
        combo = result.get("recommended_combination", {})
        print(f"  ✅ Điểm tổng hợp: {combo.get('value_score', '?')}/10 | Đánh giá: {combo.get('fit_rating', '')}")
