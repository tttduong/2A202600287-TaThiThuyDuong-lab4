"""
Tool definitions (OpenAI function calling format) and Python handlers.
"""
import json
from datetime import datetime, date
from mock_data import (
    FLIGHT_DATABASE, HOTEL_DATABASE, DAILY_COST_ESTIMATES,
    normalize_city, CITY_DISPLAY
)

# ── OpenAI Tool Schemas ───────────────────────────────────────────────────────

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_flights",
            "description": (
                "Tìm kiếm các chuyến bay có sẵn giữa hai thành phố theo ngày. "
                "Trả về tối đa 5 lựa chọn chuyến bay với giá, thời gian bay, số điểm dừng, "
                "và số ghế còn lại. LUÔN gọi tool này trước khi đưa ra gợi ý về chuyến bay."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "origin_city": {
                        "type": "string",
                        "description": "Thành phố khởi hành hoặc mã sân bay (vd: 'Hà Nội', 'New York', 'NYC', 'JFK')"
                    },
                    "destination_city": {
                        "type": "string",
                        "description": "Thành phố đến hoặc mã sân bay (vd: 'Paris', 'Tokyo', 'CDG')"
                    },
                    "departure_date": {
                        "type": "string",
                        "description": "Ngày khởi hành định dạng YYYY-MM-DD"
                    },
                    "return_date": {
                        "type": "string",
                        "description": "Ngày về định dạng YYYY-MM-DD, tùy chọn cho chuyến một chiều"
                    },
                    "num_passengers": {
                        "type": "integer",
                        "description": "Số hành khách, mặc định là 1",
                        "default": 1
                    },
                    "cabin_class": {
                        "type": "string",
                        "enum": ["economy", "business", "first"],
                        "description": "Hạng ghế ưu tiên"
                    }
                },
                "required": ["origin_city", "destination_city", "departure_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_hotels",
            "description": (
                "Tìm kiếm khách sạn tại thành phố đến. Trả về các lựa chọn ở nhiều mức giá "
                "khác nhau (ngân sách, trung bình, cao cấp) với giá, đánh giá, tiện ích, và "
                "tình trạng phòng trống. LUÔN gọi tool này trước khi đưa ra gợi ý về chỗ ở."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Thành phố cần tìm khách sạn"
                    },
                    "check_in_date": {
                        "type": "string",
                        "description": "Ngày nhận phòng định dạng YYYY-MM-DD"
                    },
                    "check_out_date": {
                        "type": "string",
                        "description": "Ngày trả phòng định dạng YYYY-MM-DD"
                    },
                    "num_guests": {
                        "type": "integer",
                        "description": "Số khách, mặc định là 1",
                        "default": 1
                    },
                    "max_price_per_night": {
                        "type": "number",
                        "description": "Giá tối đa mỗi đêm tính bằng USD (tùy chọn)"
                    },
                    "min_stars": {
                        "type": "integer",
                        "description": "Số sao tối thiểu (1-5)",
                        "enum": [1, 2, 3, 4, 5]
                    }
                },
                "required": ["city", "check_in_date", "check_out_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_budget",
            "description": (
                "Kiểm tra ngân sách du lịch của người dùng, xem còn bao nhiêu, và đánh giá "
                "liệu các lựa chọn chuyến bay + khách sạn có phù hợp ngân sách không. "
                "Dùng tool này để xác nhận khả năng chi trả TRƯỚC KHI gọi optimize_trip."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "total_budget_usd": {
                        "type": "number",
                        "description": "Tổng ngân sách chuyến đi của người dùng tính bằng USD"
                    },
                    "planned_flight_cost": {
                        "type": "number",
                        "description": "Chi phí chuyến bay đã chọn tính bằng USD (tùy chọn)"
                    },
                    "planned_hotel_cost": {
                        "type": "number",
                        "description": "Tổng chi phí khách sạn cho tất cả các đêm tính bằng USD (tùy chọn)"
                    },
                    "num_days": {
                        "type": "integer",
                        "description": "Tổng số ngày chuyến đi, để ước tính tiền chi tiêu hàng ngày"
                    },
                    "destination_city": {
                        "type": "string",
                        "description": "Thành phố đến, dùng để ước tính chi phí sinh hoạt địa phương"
                    }
                },
                "required": ["total_budget_usd"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "optimize_trip",
            "description": (
                "GỌI TOOL NÀY SAU CÙNG sau khi đã tìm kiếm chuyến bay, khách sạn và kiểm tra ngân sách. "
                "Kết hợp tất cả thông tin đã thu thập để tạo ra gợi ý chuyến đi tối ưu với phân tích "
                "đánh đổi (trade-off). Tool này TỔNG HỢP dữ liệu từ nhiều nguồn thành một khuyến nghị "
                "toàn diện duy nhất — đây là trái tim của TravelBuddy."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string",
                        "description": "Điểm đến của chuyến đi"
                    },
                    "trip_dates": {
                        "type": "object",
                        "properties": {
                            "departure": {"type": "string", "description": "Ngày khởi hành YYYY-MM-DD"},
                            "return_date": {"type": "string", "description": "Ngày về YYYY-MM-DD"},
                            "num_nights": {"type": "integer", "description": "Số đêm lưu trú"}
                        },
                        "required": ["departure", "num_nights"]
                    },
                    "selected_flight": {
                        "type": "object",
                        "description": "Chuyến bay tốt nhất được chọn từ kết quả search_flights",
                        "properties": {
                            "flight_id": {"type": "string"},
                            "airline": {"type": "string"},
                            "price_usd": {"type": "number"},
                            "duration_hrs": {"type": "number"},
                            "stops": {"type": "integer"},
                            "departure": {"type": "string"}
                        },
                        "required": ["airline", "price_usd"]
                    },
                    "selected_hotel": {
                        "type": "object",
                        "description": "Khách sạn tốt nhất được chọn từ kết quả search_hotels",
                        "properties": {
                            "hotel_id": {"type": "string"},
                            "name": {"type": "string"},
                            "price_per_night_usd": {"type": "number"},
                            "total_cost_usd": {"type": "number"},
                            "stars": {"type": "integer"},
                            "rating": {"type": "number"},
                            "neighborhood": {"type": "string"}
                        },
                        "required": ["name", "price_per_night_usd", "total_cost_usd"]
                    },
                    "budget_analysis": {
                        "type": "object",
                        "description": "Kết quả từ check_budget",
                        "properties": {
                            "total_budget_usd": {"type": "number"},
                            "remaining_usd": {"type": "number"},
                            "budget_status": {"type": "string"},
                            "daily_spending_available_usd": {"type": "number"}
                        },
                        "required": ["total_budget_usd", "remaining_usd"]
                    },
                    "user_priorities": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Ưu tiên của người dùng, vd: ['rẻ nhất', 'nhanh nhất', 'thoải mái nhất', 'trung tâm']"
                    }
                },
                "required": ["destination", "trip_dates", "selected_flight", "selected_hotel", "budget_analysis"]
            }
        }
    }
]


# ── Python Handler Functions ──────────────────────────────────────────────────

def _parse_date(date_str: str) -> date:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {date_str}")


def search_flights(origin_city: str, destination_city: str, departure_date: str,
                   return_date: str = None, num_passengers: int = 1,
                   cabin_class: str = "economy") -> dict:
    origin_key = normalize_city(origin_city)
    dest_key = normalize_city(destination_city)
    route_key = (origin_key, dest_key)

    flights = FLIGHT_DATABASE.get(route_key, [])

    # Try reverse route if no direct match
    if not flights:
        reverse_key = (dest_key, origin_key)
        raw = FLIGHT_DATABASE.get(reverse_key, [])
        # Swap origin/destination for display
        flights = [{**f, "note": "Reverse route — adjust times accordingly"} for f in raw]

    if not flights:
        return {
            "route": f"{origin_city} → {destination_city}",
            "error": f"Không tìm thấy chuyến bay cho tuyến {origin_city} → {destination_city}. "
                     f"Vui lòng thử: NYC, LAX, PAR, TYO, LON, BKK, SGN, HAN.",
            "available_routes": [f"{o} → {d}" for (o, d) in FLIGHT_DATABASE.keys()],
        }

    # Apply cabin class pricing
    result_flights = []
    for f in flights:
        price = f["price_usd"] * num_passengers
        if cabin_class == "business":
            price = f.get("business_price_usd", f["price_usd"] * 3) * num_passengers
        elif cabin_class == "first":
            price = f.get("business_price_usd", f["price_usd"] * 3) * 1.4 * num_passengers

        result_flights.append({
            "flight_id": f["flight_id"],
            "airline": f["airline"],
            "departure_time": f["departure"],
            "arrival_time": f["arrival"],
            "duration_hrs": f["duration_hrs"],
            "price_usd": round(price, 0),
            "price_per_person_usd": round(price / num_passengers, 0),
            "cabin_class": cabin_class,
            "stops": f["stops"],
            "stops_label": "Direct" if f["stops"] == 0 else f"{f['stops']} stop(s)",
            "seats_left": f["seats_left"],
        })

    result_flights.sort(key=lambda x: x["price_usd"])

    return {
        "route": f"{CITY_DISPLAY.get(origin_key, origin_city)} → {CITY_DISPLAY.get(dest_key, destination_city)}",
        "departure_date": departure_date,
        "return_date": return_date,
        "passengers": num_passengers,
        "cabin_class": cabin_class,
        "options": result_flights[:5],
        "cheapest_total_usd": result_flights[0]["price_usd"],
        "cheapest_airline": result_flights[0]["airline"],
        "direct_flights_available": any(f["stops"] == 0 for f in result_flights),
    }


def search_hotels(city: str, check_in_date: str, check_out_date: str,
                  num_guests: int = 1, max_price_per_night: float = None,
                  min_stars: int = None) -> dict:
    city_key = normalize_city(city)
    hotels = HOTEL_DATABASE.get(city_key, [])

    if not hotels:
        return {
            "city": city,
            "error": f"Không tìm thấy khách sạn tại {city}. "
                     f"Các thành phố có sẵn: Paris, Tokyo, London, Bangkok, Ho Chi Minh City, Hanoi.",
            "available_cities": list(HOTEL_DATABASE.keys()),
        }

    # Calculate nights
    try:
        nights = (_parse_date(check_out_date) - _parse_date(check_in_date)).days
    except ValueError:
        nights = 7  # fallback

    if nights <= 0:
        nights = 1

    # Filter and compute totals
    result_hotels = []
    for h in hotels:
        if max_price_per_night and h["price_per_night_usd"] > max_price_per_night:
            continue
        if min_stars and h["stars"] < min_stars:
            continue

        total = h["price_per_night_usd"] * nights
        result_hotels.append({
            "hotel_id": h["hotel_id"],
            "name": h["name"],
            "stars": h["stars"],
            "stars_label": "⭐" * h["stars"],
            "neighborhood": h["neighborhood"],
            "price_per_night_usd": h["price_per_night_usd"],
            "total_cost_usd": total,
            "rating": h["rating"],
            "amenities": h["amenities"],
            "rooms_available": h["rooms_available"],
            "distance_center_km": h["distance_center_km"],
            "highlights": h["highlights"],
            "urgency": "Chỉ còn ít phòng!" if h["rooms_available"] <= 5 else "Còn phòng",
        })

    result_hotels.sort(key=lambda x: x["rating"], reverse=True)

    daily_costs = DAILY_COST_ESTIMATES.get(city_key, {"mid": 60, "note": ""})

    return {
        "city": CITY_DISPLAY.get(city_key, city),
        "check_in": check_in_date,
        "check_out": check_out_date,
        "nights": nights,
        "guests": num_guests,
        "options": result_hotels,
        "cheapest_per_night_usd": min((h["price_per_night_usd"] for h in result_hotels), default=0),
        "estimated_daily_activities_usd": daily_costs.get("mid", 60),
        "local_tip": daily_costs.get("note", ""),
    }


def check_budget(total_budget_usd: float, planned_flight_cost: float = 0,
                 planned_hotel_cost: float = 0, num_days: int = None,
                 destination_city: str = None) -> dict:
    committed = (planned_flight_cost or 0) + (planned_hotel_cost or 0)
    remaining = total_budget_usd - committed
    pct_used = round((committed / total_budget_usd) * 100, 1) if total_budget_usd > 0 else 0

    # Daily spending estimate
    daily_available = round(remaining / num_days, 0) if num_days and num_days > 0 else None

    # City cost-of-living lookup
    city_key = normalize_city(destination_city) if destination_city else None
    city_costs = DAILY_COST_ESTIMATES.get(city_key, {}) if city_key else {}
    local_daily_mid = city_costs.get("mid", 60)
    local_tip = city_costs.get("note", "")

    # Budget status
    if pct_used < 50:
        status = "rất thoải mái"
        status_emoji = "✅"
    elif pct_used < 70:
        status = "thoải mái"
        status_emoji = "✅"
    elif pct_used < 85:
        status = "ổn"
        status_emoji = "⚠️"
    else:
        status = "chặt chẽ"
        status_emoji = "🔴"

    warnings = []
    if pct_used > 85:
        warnings.append(f"Chuyến bay + khách sạn chiếm {pct_used}% ngân sách — ít tiền cho hoạt động")
    if daily_available and daily_available < local_daily_mid:
        warnings.append(
            f"Ngân sách hàng ngày còn lại (${daily_available:.0f}) thấp hơn mức khuyến nghị "
            f"cho {destination_city} (${local_daily_mid}/ngày)"
        )
    if remaining < 0:
        warnings.append("CẢNH BÁO: Chuyến bay + khách sạn VƯỢT ngân sách!")

    return {
        "total_budget_usd": total_budget_usd,
        "flight_cost_usd": planned_flight_cost or 0,
        "hotel_cost_usd": planned_hotel_cost or 0,
        "committed_usd": committed,
        "remaining_usd": round(remaining, 0),
        "pct_used": pct_used,
        "budget_status": status,
        "budget_status_emoji": status_emoji,
        "daily_spending_available_usd": daily_available,
        "recommended_daily_spend_usd": local_daily_mid,
        "local_tip": local_tip,
        "warnings": warnings,
        "is_feasible": remaining >= 0,
    }


def optimize_trip(destination: str, trip_dates: dict, selected_flight: dict,
                  selected_hotel: dict, budget_analysis: dict,
                  user_priorities: list = None) -> dict:
    total_cost = selected_flight["price_usd"] + selected_hotel["total_cost_usd"]
    budget = budget_analysis["total_budget_usd"]
    remaining_after = budget - total_cost
    pct_used = round((total_cost / budget) * 100, 1) if budget > 0 else 0

    # Composite value score (0-10)
    # Lower cost % → higher score; higher hotel rating → higher score
    cost_score = max(0, 10 - (pct_used / 10))  # 0% = 10pts, 100% = 0pts
    hotel_rating = selected_hotel.get("rating", 8.0)
    rating_score = (hotel_rating / 10) * 10  # normalize to 0-10
    stops_penalty = selected_flight.get("stops", 0) * 0.3
    value_score = round((cost_score * 0.4 + rating_score * 0.6) - stops_penalty, 1)
    value_score = max(0.0, min(10.0, value_score))

    # Fit rating
    if pct_used < 55:
        fit_rating = "Xuất sắc"
    elif pct_used < 70:
        fit_rating = "Tốt"
    elif pct_used < 85:
        fit_rating = "Ổn"
    else:
        fit_rating = "Chặt chẽ"

    # Trade-off analysis
    trade_offs = []
    flight_stops = selected_flight.get("stops", 0)
    if flight_stops > 0:
        trade_offs.append(
            f"✈️ Chuyến bay có {flight_stops} điểm dừng — tiết kiệm tiền nhưng thêm thời gian di chuyển"
        )
    if pct_used > 70:
        trade_offs.append(
            f"💰 Chuyến bay + khách sạn dùng {pct_used}% ngân sách — lên kế hoạch chi tiêu hoạt động cẩn thận"
        )
    stars = selected_hotel.get("stars", 3)
    if stars <= 2:
        trade_offs.append(
            f"🏨 Khách sạn {stars} sao — tiết kiệm nhưng tiện ích hạn chế hơn"
        )
    daily = budget_analysis.get("daily_spending_available_usd")
    if daily and daily < 50:
        trade_offs.append(
            f"📅 Ngân sách hàng ngày còn lại ~${daily:.0f} — cần ăn uống tại địa phương và tránh tour đắt tiền"
        )

    # Money-saving tips by destination
    city_key = normalize_city(destination)
    city_costs = DAILY_COST_ESTIMATES.get(city_key, {})
    base_tips = [
        f"🍜 {city_costs.get('note', 'Ăn tại quán địa phương để tiết kiệm 40-60% chi phí ăn uống')}",
        "🚇 Mua thẻ giao thông tuần/tháng thay vì vé lẻ",
        "📅 Đặt trước các điểm tham quan phổ biến để tránh xếp hàng và đôi khi rẻ hơn",
    ]

    # Alternative suggestion hint
    alternatives_hint = []
    if flight_stops > 0:
        alternatives_hint.append(
            f"Bay thẳng sẽ thoải mái hơn (~${selected_flight['price_usd'] * 1.15:.0f} ước tính)"
        )
    if stars < 4:
        alternatives_hint.append(
            f"Nâng lên 4 sao sẽ cải thiện trải nghiệm đáng kể "
            f"(~+${selected_hotel['price_per_night_usd'] * 0.5 * trip_dates.get('num_nights', 5):.0f})"
        )

    return {
        "optimization_complete": True,
        "destination": destination,
        "trip_duration_nights": trip_dates.get("num_nights"),
        "recommended_combination": {
            "flight": {
                "airline": selected_flight.get("airline"),
                "flight_id": selected_flight.get("flight_id"),
                "price_usd": selected_flight["price_usd"],
                "stops": selected_flight.get("stops", 0),
                "departure_time": selected_flight.get("departure", selected_flight.get("departure_time")),
            },
            "hotel": {
                "name": selected_hotel["name"],
                "stars": stars,
                "neighborhood": selected_hotel.get("neighborhood"),
                "price_per_night_usd": selected_hotel["price_per_night_usd"],
                "total_hotel_usd": selected_hotel["total_cost_usd"],
                "rating": hotel_rating,
            },
            "total_flight_hotel_usd": round(total_cost, 0),
            "pct_of_budget_used": pct_used,
            "remaining_for_activities_usd": round(remaining_after, 0),
            "value_score": value_score,
            "fit_rating": fit_rating,
        },
        "trade_offs": trade_offs,
        "upgrade_options": alternatives_hint,
        "money_saving_tips": base_tips,
        "summary": (
            f"Điểm giá trị tổng hợp: {value_score}/10 — "
            f"cân bằng giữa chi phí ({pct_used}% ngân sách), "
            f"tiện nghi ({stars}⭐ / {hotel_rating}/10), và lịch trình bay."
        ),
    }


# ── Dispatcher ────────────────────────────────────────────────────────────────

_HANDLERS = {
    "search_flights": search_flights,
    "search_hotels": search_hotels,
    "check_budget": check_budget,
    "optimize_trip": optimize_trip,
}


def dispatch_tool(tool_name: str, tool_input: dict) -> dict:
    handler = _HANDLERS.get(tool_name)
    if not handler:
        return {"error": f"Unknown tool: {tool_name}"}
    try:
        return handler(**tool_input)
    except TypeError as e:
        return {"error": f"Invalid arguments for {tool_name}: {e}"}
