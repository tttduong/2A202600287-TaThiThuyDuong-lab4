"""
Utility functions for Travel Agent
- Format prices with Vietnamese number format
- Parse expenses string
- Parse relative dates (ngày mai, cuối tuần, etc.)
- Other helper functions
"""

from datetime import datetime, timedelta


def format_price(price: int) -> str:
    """
    Format price with thousand separators and VND currency
    Example: 1450000 → "1.450.000đ"
    """
    if price < 0:
        return f"-{format_price(abs(price))}"
    
    price_str = str(price)
    # Add thousand separators from right to left
    reversed_str = price_str[::-1]
    groups = [reversed_str[i:i+3] for i in range(0, len(reversed_str), 3)]
    formatted = ".".join(groups)[::-1]
    return f"{formatted}đ"


def format_currency(price: int) -> str:
    """Alias for format_price"""
    return format_price(price)


def parse_relative_date(text: str) -> str:
    """
    Parse Vietnamese relative date expressions and convert to YYYY-MM-DD format
    
    Supported phrases:
    - "ngày mai" / "mai" → tomorrow
    - "hôm nay" → today
    - "ngày kia" → day after tomorrow
    - "tuần sau" → next week (7 days later)
    - "cuối tuần" → this weekend (Saturday)
    - "thứ 2" / "thứ 3" / ... / "chủ nhật" → next occurrence of that day
    
    Example:
        parse_relative_date("ngày mai") → "2024-04-09"  (if today is 2024-04-08)
        parse_relative_date("2024-04-10") → "2024-04-10"  (already a date, return as-is)
    
    Returns: ISO format date string (YYYY-MM-DD)
    """
    text = text.lower().strip()
    today = datetime.now()
    
    # If it's already a date format, return it as-is
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return text
    except ValueError:
        pass
    
    # Map Vietnamese day names
    day_map = {
        "thứ 2": 0, "thứ ba": 1, "thứ 3": 1, "thứ tư": 2, "thứ 4": 2,
        "thứ năm": 3, "thứ 5": 3, "thứ sáu": 4, "thứ 6": 4,
        "thứ bảy": 5, "thứ 7": 5, "chủ nhật": 6
    }
    
    # Relative date mapping
    relative_dates = {
        "hôm nay": 0,
        "ngày mai": 1,
        "mai": 1,
        "ngày kia": 2,
        "kia": 2,
        "tuần sau": 7,
        "cuối tuần": 5 if today.weekday() < 5 else (12 - today.weekday())  # next Saturday
    }
    
    # Check relative expressions
    for phrase, days_offset in relative_dates.items():
        if phrase in text:
            target_date = today + timedelta(days=days_offset)
            return target_date.strftime("%Y-%m-%d")
    
    # Check day of week
    for day_phrase, weekday in day_map.items():
        if day_phrase in text:
            current_weekday = today.weekday()
            days_ahead = (weekday - current_weekday) % 7
            if days_ahead == 0:
                days_ahead = 7  # If it's today, go to next week
            target_date = today + timedelta(days=days_ahead)
            return target_date.strftime("%Y-%m-%d")
    
    # If no match found, return today's date
    return today.strftime("%Y-%m-%d")


def parse_expenses(expenses_str: str) -> dict:
    """
    Parse expenses string into dictionary
    Input format: "vé_máy_bay:890000,khách_sạn:650000"
    Output: {"vé_máy_bay": 890000, "khách_sạn": 650000}
    
    Raises ValueError if format is invalid
    """
    if not expenses_str or not expenses_str.strip():
        return {}
    
    expenses_dict = {}
    try:
        items = expenses_str.split(",")
        for item in items:
            item = item.strip()
            if not item:
                continue
            
            if ":" not in item:
                raise ValueError(f"Invalid format: '{item}'. Expected 'name:amount'")
            
            name, amount_str = item.split(":", 1)
            name = name.strip()
            
            try:
                amount = int(amount_str.strip())
                if amount < 0:
                    raise ValueError(f"Amount cannot be negative: {amount}")
                expenses_dict[name] = amount
            except ValueError as e:
                if "invalid literal" in str(e):
                    raise ValueError(f"Invalid amount: '{amount_str.strip()}'. Must be an integer")
                raise
        
        return expenses_dict
    
    except Exception as e:
        raise ValueError(f"Failed to parse expenses: {str(e)}")


def format_expense_table(expenses_dict: dict, total_budget: int) -> str:
    """
    Format expenses into a nice table
    Returns: formatted string with table and remaining budget info
    """
    total_expenses = sum(expenses_dict.values())
    remaining = total_budget - total_expenses
    
    # Build table
    lines = ["📊 Bảng chi phí:"]
    for name, amount in expenses_dict.items():
        lines.append(f"  - {name}: {format_price(amount)}")
    
    lines.append("  " + "─" * 30)
    lines.append(f"  Tổng chi: {format_price(total_expenses)}")
    lines.append(f"  Ngân sách ban đầu: {format_price(total_budget)}")
    
    if remaining >= 0:
        lines.append(f"  Còn lại: {format_price(remaining)} ✅")
    else:
        lines.append(f"  ⚠️ VƯỢT NGÂN SÁCH: {format_price(abs(remaining))} ❌")
    
    return "\n".join(lines)
