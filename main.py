"""
TravelBuddy Smart Travel Assistant — CLI Entry Point
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Validate API key before importing agent
if not os.environ.get("OPENAI_API_KEY"):
    print("❌ Lỗi: Chưa có OPENAI_API_KEY.")
    print("   Tạo file .env với nội dung: OPENAI_API_KEY=sk-...")
    sys.exit(1)

from agent import run_agent_turn  # noqa: E402 (import after env check)

BANNER = """
╔════════════════════════════════════════════════════╗
║        TravelBuddy Smart Travel Assistant          ║
║        Trợ lý Du lịch Thông minh — GPT-4o         ║
╠════════════════════════════════════════════════════╣
║  Lệnh đặc biệt:                                    ║
║    'new'  — Bắt đầu kế hoạch chuyến đi mới        ║
║    'quit' — Thoát                                  ║
╚════════════════════════════════════════════════════╝

Ví dụ: "Tôi muốn đi Paris 7 ngày từ New York, ngân sách $4000"
"""

WELCOME_HINT = (
    "💡 Thử hỏi: \"Lên kế hoạch 5 ngày Tokyo từ LA, ngân sách $3500\" "
    "hoặc \"Muốn đi Sài Gòn 10 ngày từ New York, tổng budget $5000\""
)


def main() -> None:
    print(BANNER)
    print(WELCOME_HINT)
    print()

    conversation_history: list = []

    while True:
        try:
            user_input = input("Bạn: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nChúc bạn chuyến đi vui vẻ! ✈️")
            break

        if not user_input:
            continue

        lower = user_input.lower()

        if lower in ("quit", "exit", "thoát", "bye"):
            print("Chúc bạn chuyến đi vui vẻ! ✈️")
            break

        if lower in ("new", "mới", "reset"):
            conversation_history = []
            print("\n🆕 Bắt đầu kế hoạch chuyến đi mới...\n")
            continue

        if lower in ("help", "trợ giúp"):
            print(WELCOME_HINT)
            continue

        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})

        print("\n⏳ TravelBuddy đang phân tích và tìm kiếm...\n")

        try:
            response_text, conversation_history = run_agent_turn(conversation_history)
            print(f"\nTravelBuddy:\n{response_text}\n")
            print("─" * 60)
        except Exception as e:
            print(f"\n❌ Lỗi: {e}\n")
            # Remove the failed user message to keep history consistent
            if conversation_history and conversation_history[-1]["role"] == "user":
                conversation_history.pop()


if __name__ == "__main__":
    main()
