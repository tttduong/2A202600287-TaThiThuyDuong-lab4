"""
Unit tests for Travel Agent Tools
Tests search_flights, search_hotels, and calculate_budget functions
"""

import sys
from tools import search_flights, search_hotels, calculate_budget
from utils import format_price, parse_expenses, format_expense_table


def test_format_price():
    """Test price formatting"""
    print("\n🧪 Testing format_price()...")
    
    assert format_price(1450000) == "1.450.000đ", "Format price failed"
    assert format_price(890000) == "890.000đ", "Format price failed"
    assert format_price(0) == "0đ", "Format price failed"
    
    print("✅ format_price() tests passed")


def test_parse_expenses():
    """Test expenses parsing"""
    print("\n🧪 Testing parse_expenses()...")
    
    result = parse_expenses("vé_máy_bay:890000,khách_sạn:650000")
    assert result == {"vé_máy_bay": 890000, "khách_sạn": 650000}, "Parse expenses failed"
    
    result = parse_expenses("")
    assert result == {}, "Parse empty expenses failed"
    
    try:
        parse_expenses("invalid_format")
        assert False, "Should raise error for invalid format"
    except ValueError:
        pass
    
    print("✅ parse_expenses() tests passed")


def test_search_flights():
    """Test search_flights tool"""
    print("\n🧪 Testing search_flights()...")

    # Valid route
    result = search_flights.invoke({"origin": "Hà Nội", "destination": "Đà Nẵng"})
    assert "Vietnam Airlines" in result or "VietJet" in result, "Flight search failed"
    assert "✈️" in result, "Flight emoji missing"

    # Invalid route (should try reverse)
    result = search_flights.invoke({"origin": "Đà Nẵng", "destination": "Hà Nội"})
    # Might find reverse route or not

    # Non-existent route
    result = search_flights.invoke({"origin": "Hà Nội", "destination": "Bình Dương"})
    assert "❌" in result or "Không tìm thấy" in result, "Should show error for non-existent route"

    print("✅ search_flights() tests passed")


def test_search_hotels():
    """Test search_hotels tool"""
    print("\n🧪 Testing search_hotels()...")

    # Valid city
    result = search_hotels.invoke({"city": "Đà Nẵng"})
    assert "🏨" in result, "Hotel emoji missing"
    assert "Mường Thanh" in result or "Sala Danang" in result or "Memory" in result, \
        "Hotel names missing"

    # With price filter
    result = search_hotels.invoke({"city": "Đà Nẵng", "max_price_per_night": 500000})
    assert "Memory Hostel" in result or "Christina's" in result, "Budget hotels not found"

    # Invalid city
    result = search_hotels.invoke({"city": "Bình Dương"})
    assert "❌" in result or "Không tìm thấy" in result, "Should show error for invalid city"

    # Price too low
    result = search_hotels.invoke({"city": "Đà Nẵng", "max_price_per_night": 100000})
    assert "❌" in result, "Should show error when price too low"

    print("✅ search_hotels() tests passed")


def test_calculate_budget():
    """Test calculate_budget tool"""
    print("\n🧪 Testing calculate_budget()...")
    
    # Normal case
    result = calculate_budget.invoke({"total_budget": 5000000, "expenses": "vé_máy_bay:890000,khách_sạn:650000"})
    assert "📊" in result, "Budget table emoji missing"
    assert "Tổng chi" in result, "Total expenses missing"
    assert "Còn lại" in result or "VƯỢT" in result, "Remaining budget missing"
    
    # Exceeding budget
    result = calculate_budget.invoke({"total_budget": 1000000, "expenses": "vé_máy_bay:890000,khách_sạn:650000"})
    assert "❌" in result or "VƯỢT" in result, "Should warn about exceeding budget"
    
    # Invalid format
    result = calculate_budget.invoke({"total_budget": 5000000, "expenses": "invalid_format"})
    assert "❌" in result or "Lỗi" in result, "Should show error for invalid format"
    
    # Empty expenses
    result = calculate_budget.invoke({"total_budget": 5000000, "expenses": ""})
    assert "❌" in result or "Không" in result, "Should handle empty expenses"
    
    print("✅ calculate_budget() tests passed")


def test_all_flights():
    """Show all available flights"""
    print("\n📋 AVAILABLE FLIGHTS:")
    print("─" * 70)
    
    flights_data = [
        ("Hà Nội", "Đà Nẵng"),
        ("Hà Nội", "Phú Quốc"),
        ("Hà Nội", "Hồ Chí Minh"),
        ("Hồ Chí Minh", "Đà Nẵng"),
        ("Hồ Chí Minh", "Phú Quốc"),
    ]
    
    for origin, dest in flights_data:
        result = search_flights.invoke({"origin": origin, "destination": dest})
        print(result)
        print()


def test_all_hotels():
    """Show all available hotels"""
    print("\n📋 AVAILABLE HOTELS:")
    print("─" * 70)
    
    cities = ["Đà Nẵng", "Phú Quốc", "Hồ Chí Minh"]
    
    for city in cities:
        result = search_hotels.invoke({"city": city})
        print(result)
        print()


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("🧪 TRAVEL AGENT - UNIT TESTS")
    print("=" * 70)
    
    try:
        # Utility tests
        test_format_price()
        test_parse_expenses()
        
        # Tool tests
        test_search_flights()
        test_search_hotels()
        test_calculate_budget()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        
        # Show available data
        test_all_flights()
        test_all_hotels()
        
        return True
    
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
