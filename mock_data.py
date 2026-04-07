"""
Mock data for TravelBuddy Smart Travel Assistant.
All prices in USD. Data is realistic but simulated.
"""

# ── City normalization ────────────────────────────────────────────────────────

CITY_ALIASES = {
    # New York
    "new york": "NYC", "new york city": "NYC", "nyc": "NYC", "jfk": "NYC",
    "lga": "NYC", "ewr": "NYC",
    # Los Angeles
    "los angeles": "LAX", "la": "LAX", "lax": "LAX",
    # Paris
    "paris": "PAR", "cdg": "PAR",
    # Tokyo
    "tokyo": "TYO", "nrt": "TYO", "hnd": "TYO",
    # London
    "london": "LON", "lhr": "LON", "lgw": "LON",
    # Bangkok
    "bangkok": "BKK", "bkk": "BKK",
    # Singapore
    "singapore": "SIN", "sin": "SIN",
    # Sydney
    "sydney": "SYD", "syd": "SYD",
    # Dubai
    "dubai": "DXB", "dxb": "DXB",
    # Ho Chi Minh City
    "ho chi minh": "SGN", "hcmc": "SGN", "saigon": "SGN", "sgn": "SGN",
    "ho chi minh city": "SGN",
    # Hanoi
    "hanoi": "HAN", "ha noi": "HAN", "han": "HAN",
}

CITY_DISPLAY = {
    "NYC": "New York", "LAX": "Los Angeles", "PAR": "Paris",
    "TYO": "Tokyo", "LON": "London", "BKK": "Bangkok",
    "SIN": "Singapore", "SYD": "Sydney", "DXB": "Dubai",
    "SGN": "Ho Chi Minh City", "HAN": "Hanoi",
}


def normalize_city(name: str) -> str:
    """Normalize city name/code to uppercase key. Returns original uppercased if unknown."""
    key = name.strip().lower()
    return CITY_ALIASES.get(key, name.strip().upper())


# ── Flight Database ───────────────────────────────────────────────────────────
# Keyed by (origin_code, dest_code). Prices are one-way per person (economy).

FLIGHT_DATABASE: dict[tuple, list[dict]] = {
    ("NYC", "PAR"): [
        {"flight_id": "AF_101", "airline": "Air France", "departure": "10:30",
         "arrival": "23:45", "duration_hrs": 7.5, "price_usd": 680,
         "class": "economy", "stops": 0, "seats_left": 8,
         "business_price_usd": 2100},
        {"flight_id": "UA_202", "airline": "United Airlines", "departure": "08:00",
         "arrival": "22:10", "duration_hrs": 9.2, "price_usd": 540,
         "class": "economy", "stops": 1, "seats_left": 15,
         "business_price_usd": 1850},
        {"flight_id": "DL_303", "airline": "Delta", "departure": "18:50",
         "arrival": "09:05+1", "duration_hrs": 8.3, "price_usd": 610,
         "class": "economy", "stops": 0, "seats_left": 4,
         "business_price_usd": 1980},
        {"flight_id": "BA_404", "airline": "British Airways", "departure": "12:00",
         "arrival": "07:30+1", "duration_hrs": 10.5, "price_usd": 490,
         "class": "economy", "stops": 1, "seats_left": 22,
         "business_price_usd": 1700},
        {"flight_id": "LH_505", "airline": "Lufthansa", "departure": "21:30",
         "arrival": "14:00+1", "duration_hrs": 9.5, "price_usd": 520,
         "class": "economy", "stops": 1, "seats_left": 10,
         "business_price_usd": 1760},
    ],
    ("NYC", "TYO"): [
        {"flight_id": "JL_101", "airline": "Japan Airlines", "departure": "12:55",
         "arrival": "16:20+1", "duration_hrs": 14.5, "price_usd": 780,
         "class": "economy", "stops": 0, "seats_left": 6,
         "business_price_usd": 3200},
        {"flight_id": "NH_202", "airline": "ANA", "departure": "10:45",
         "arrival": "14:30+1", "duration_hrs": 14.8, "price_usd": 740,
         "class": "economy", "stops": 0, "seats_left": 11,
         "business_price_usd": 3100},
        {"flight_id": "UA_303", "airline": "United Airlines", "departure": "11:00",
         "arrival": "15:40+1", "duration_hrs": 15.7, "price_usd": 650,
         "class": "economy", "stops": 1, "seats_left": 18,
         "business_price_usd": 2800},
        {"flight_id": "AA_404", "airline": "American Airlines", "departure": "08:30",
         "arrival": "14:00+1", "duration_hrs": 16.5, "price_usd": 620,
         "class": "economy", "stops": 1, "seats_left": 25,
         "business_price_usd": 2650},
    ],
    ("LAX", "TYO"): [
        {"flight_id": "JL_501", "airline": "Japan Airlines", "departure": "14:00",
         "arrival": "18:30+1", "duration_hrs": 11.5, "price_usd": 720,
         "class": "economy", "stops": 0, "seats_left": 9,
         "business_price_usd": 2900},
        {"flight_id": "NH_502", "airline": "ANA", "departure": "11:30",
         "arrival": "16:00+1", "duration_hrs": 11.5, "price_usd": 690,
         "class": "economy", "stops": 0, "seats_left": 14,
         "business_price_usd": 2800},
        {"flight_id": "UA_503", "airline": "United Airlines", "departure": "09:00",
         "arrival": "14:50+1", "duration_hrs": 12.8, "price_usd": 580,
         "class": "economy", "stops": 1, "seats_left": 20,
         "business_price_usd": 2400},
    ],
    ("LAX", "LON"): [
        {"flight_id": "BA_601", "airline": "British Airways", "departure": "19:00",
         "arrival": "13:30+1", "duration_hrs": 10.5, "price_usd": 620,
         "class": "economy", "stops": 0, "seats_left": 7,
         "business_price_usd": 2500},
        {"flight_id": "VS_602", "airline": "Virgin Atlantic", "departure": "16:30",
         "arrival": "11:15+1", "duration_hrs": 10.75, "price_usd": 590,
         "class": "economy", "stops": 0, "seats_left": 12,
         "business_price_usd": 2300},
        {"flight_id": "AA_603", "airline": "American Airlines", "departure": "08:00",
         "arrival": "07:30+1", "duration_hrs": 11.5, "price_usd": 530,
         "class": "economy", "stops": 1, "seats_left": 30,
         "business_price_usd": 2100},
    ],
    ("NYC", "BKK"): [
        {"flight_id": "TG_701", "airline": "Thai Airways", "departure": "23:30",
         "arrival": "06:00+2", "duration_hrs": 18.5, "price_usd": 860,
         "class": "economy", "stops": 1, "seats_left": 15,
         "business_price_usd": 3500},
        {"flight_id": "CX_702", "airline": "Cathay Pacific", "departure": "00:30",
         "arrival": "07:45+2", "duration_hrs": 19.2, "price_usd": 790,
         "class": "economy", "stops": 1, "seats_left": 20,
         "business_price_usd": 3200},
    ],
    ("LAX", "BKK"): [
        {"flight_id": "TG_801", "airline": "Thai Airways", "departure": "22:00",
         "arrival": "05:30+2", "duration_hrs": 17.5, "price_usd": 780,
         "class": "economy", "stops": 1, "seats_left": 12,
         "business_price_usd": 3100},
        {"flight_id": "SQ_802", "airline": "Singapore Airlines", "departure": "01:00",
         "arrival": "10:30+2", "duration_hrs": 17.5, "price_usd": 820,
         "class": "economy", "stops": 1, "seats_left": 8,
         "business_price_usd": 3400},
    ],
    ("NYC", "SGN"): [
        {"flight_id": "VN_901", "airline": "Vietnam Airlines", "departure": "11:30",
         "arrival": "21:00+1", "duration_hrs": 22.5, "price_usd": 900,
         "class": "economy", "stops": 1, "seats_left": 18,
         "business_price_usd": 3600},
        {"flight_id": "CX_902", "airline": "Cathay Pacific", "departure": "00:30",
         "arrival": "08:00+2", "duration_hrs": 20.5, "price_usd": 840,
         "class": "economy", "stops": 1, "seats_left": 25,
         "business_price_usd": 3300},
    ],
    ("NYC", "HAN"): [
        {"flight_id": "VN_A01", "airline": "Vietnam Airlines", "departure": "11:30",
         "arrival": "18:00+1", "duration_hrs": 21.5, "price_usd": 880,
         "class": "economy", "stops": 1, "seats_left": 20,
         "business_price_usd": 3500},
        {"flight_id": "SQ_A02", "airline": "Singapore Airlines", "departure": "09:00",
         "arrival": "16:30+1", "duration_hrs": 22.5, "price_usd": 820,
         "class": "economy", "stops": 1, "seats_left": 15,
         "business_price_usd": 3300},
    ],
    ("LAX", "PAR"): [
        {"flight_id": "AF_B01", "airline": "Air France", "departure": "15:00",
         "arrival": "12:30+1", "duration_hrs": 11.5, "price_usd": 720,
         "class": "economy", "stops": 0, "seats_left": 7,
         "business_price_usd": 2600},
        {"flight_id": "AA_B02", "airline": "American Airlines", "departure": "18:30",
         "arrival": "16:00+1", "duration_hrs": 11.5, "price_usd": 660,
         "class": "economy", "stops": 0, "seats_left": 14,
         "business_price_usd": 2400},
    ],
}

# ── Hotel Database ────────────────────────────────────────────────────────────
# Keyed by city code. price_per_night_usd is for standard double room.

HOTEL_DATABASE: dict[str, list[dict]] = {
    "PAR": [
        {"hotel_id": "H_PAR_01", "name": "Le Grand Marais", "stars": 4,
         "price_per_night_usd": 220, "neighborhood": "Le Marais",
         "amenities": ["WiFi", "Breakfast", "Gym", "Bar"],
         "rating": 9.1, "distance_center_km": 1.2, "rooms_available": 5,
         "highlights": "Boutique hotel in historic district, 5 min walk to Pompidou"},
        {"hotel_id": "H_PAR_02", "name": "Hôtel Montparnasse Garden", "stars": 3,
         "price_per_night_usd": 140, "neighborhood": "Montparnasse",
         "amenities": ["WiFi", "Restaurant"],
         "rating": 8.4, "distance_center_km": 3.0, "rooms_available": 12,
         "highlights": "Good value, near Catacombs and Luxembourg Garden"},
        {"hotel_id": "H_PAR_03", "name": "Paris Luxury Palace", "stars": 5,
         "price_per_night_usd": 480, "neighborhood": "8th Arrondissement",
         "amenities": ["WiFi", "Breakfast", "Spa", "Pool", "Concierge", "Restaurant"],
         "rating": 9.6, "distance_center_km": 0.8, "rooms_available": 3,
         "highlights": "Steps from Champs-Élysées, Michelin-star restaurant on site"},
        {"hotel_id": "H_PAR_04", "name": "République Budget Inn", "stars": 2,
         "price_per_night_usd": 80, "neighborhood": "République",
         "amenities": ["WiFi"],
         "rating": 7.6, "distance_center_km": 2.5, "rooms_available": 20,
         "highlights": "Affordable, near Place de la République metro"},
        {"hotel_id": "H_PAR_05", "name": "Bastille Art Hotel", "stars": 4,
         "price_per_night_usd": 195, "neighborhood": "Bastille",
         "amenities": ["WiFi", "Bar", "Gym"],
         "rating": 8.8, "distance_center_km": 2.0, "rooms_available": 8,
         "highlights": "Design hotel near Opera Bastille, vibrant nightlife area"},
    ],
    "TYO": [
        {"hotel_id": "H_TYO_01", "name": "Shinjuku Grand Hotel", "stars": 4,
         "price_per_night_usd": 180, "neighborhood": "Shinjuku",
         "amenities": ["WiFi", "Restaurant", "Gym", "Onsen"],
         "rating": 9.0, "distance_center_km": 1.5, "rooms_available": 10,
         "highlights": "Great transport links, rooftop onsen, city views"},
        {"hotel_id": "H_TYO_02", "name": "Shibuya Crossing Inn", "stars": 3,
         "price_per_night_usd": 120, "neighborhood": "Shibuya",
         "amenities": ["WiFi", "Breakfast"],
         "rating": 8.5, "distance_center_km": 2.0, "rooms_available": 18,
         "highlights": "Walking distance to famous Shibuya crossing and shopping"},
        {"hotel_id": "H_TYO_03", "name": "Asakusa Tradition Hotel", "stars": 3,
         "price_per_night_usd": 100, "neighborhood": "Asakusa",
         "amenities": ["WiFi", "Japanese Breakfast"],
         "rating": 8.9, "distance_center_km": 3.5, "rooms_available": 7,
         "highlights": "Traditional Japanese rooms, near Senso-ji Temple"},
        {"hotel_id": "H_TYO_04", "name": "Tokyo Luxury Towers", "stars": 5,
         "price_per_night_usd": 420, "neighborhood": "Roppongi",
         "amenities": ["WiFi", "Spa", "Pool", "3 Restaurants", "Concierge"],
         "rating": 9.4, "distance_center_km": 2.0, "rooms_available": 5,
         "highlights": "Iconic views of Tokyo skyline and Mt. Fuji on clear days"},
        {"hotel_id": "H_TYO_05", "name": "Capsule & Suite Akihabara", "stars": 2,
         "price_per_night_usd": 65, "neighborhood": "Akihabara",
         "amenities": ["WiFi", "Shared Lounge"],
         "rating": 8.2, "distance_center_km": 4.0, "rooms_available": 30,
         "highlights": "Unique capsule-style rooms, budget-friendly, tech district"},
    ],
    "LON": [
        {"hotel_id": "H_LON_01", "name": "Covent Garden Boutique", "stars": 4,
         "price_per_night_usd": 240, "neighborhood": "Covent Garden",
         "amenities": ["WiFi", "Bar", "Restaurant"],
         "rating": 9.0, "distance_center_km": 1.0, "rooms_available": 6,
         "highlights": "Heart of London theatre district, 10 min walk to Trafalgar Sq"},
        {"hotel_id": "H_LON_02", "name": "Notting Hill Budget Stay", "stars": 3,
         "price_per_night_usd": 160, "neighborhood": "Notting Hill",
         "amenities": ["WiFi", "Breakfast"],
         "rating": 8.3, "distance_center_km": 3.5, "rooms_available": 15,
         "highlights": "Charming neighbourhood, Portobello Market nearby"},
        {"hotel_id": "H_LON_03", "name": "The Strand Palace", "stars": 5,
         "price_per_night_usd": 520, "neighborhood": "The Strand",
         "amenities": ["WiFi", "Spa", "Pool", "Restaurant", "Concierge"],
         "rating": 9.5, "distance_center_km": 0.5, "rooms_available": 4,
         "highlights": "Historic luxury hotel, steps from National Gallery"},
        {"hotel_id": "H_LON_04", "name": "Shoreditch Hostel Plus", "stars": 2,
         "price_per_night_usd": 90, "neighborhood": "Shoreditch",
         "amenities": ["WiFi", "Bar"],
         "rating": 7.9, "distance_center_km": 4.0, "rooms_available": 25,
         "highlights": "Trendy East London, great for nightlife and street art"},
    ],
    "BKK": [
        {"hotel_id": "H_BKK_01", "name": "Riverside Luxury Bangkok", "stars": 5,
         "price_per_night_usd": 200, "neighborhood": "Riverside",
         "amenities": ["WiFi", "Pool", "Spa", "2 Restaurants", "River View"],
         "rating": 9.3, "distance_center_km": 2.0, "rooms_available": 8,
         "highlights": "Stunning Chao Phraya views, free river shuttle to temples"},
        {"hotel_id": "H_BKK_02", "name": "Sukhumvit City Hotel", "stars": 4,
         "price_per_night_usd": 95, "neighborhood": "Sukhumvit",
         "amenities": ["WiFi", "Pool", "Breakfast", "Gym"],
         "rating": 8.7, "distance_center_km": 3.5, "rooms_available": 20,
         "highlights": "Great value 4-star, BTS Skytrain access, vibrant area"},
        {"hotel_id": "H_BKK_03", "name": "Khao San Budget Inn", "stars": 2,
         "price_per_night_usd": 35, "neighborhood": "Khao San Road",
         "amenities": ["WiFi", "Bar"],
         "rating": 7.5, "distance_center_km": 2.5, "rooms_available": 40,
         "highlights": "Backpacker hub, lively nightlife, close to Grand Palace"},
        {"hotel_id": "H_BKK_04", "name": "Silom Comfort Suites", "stars": 3,
         "price_per_night_usd": 65, "neighborhood": "Silom",
         "amenities": ["WiFi", "Breakfast", "Pool"],
         "rating": 8.4, "distance_center_km": 2.8, "rooms_available": 14,
         "highlights": "Business district, easy MRT access to night markets"},
    ],
    "SGN": [
        {"hotel_id": "H_SGN_01", "name": "District 1 Grand Hotel", "stars": 4,
         "price_per_night_usd": 85, "neighborhood": "District 1",
         "amenities": ["WiFi", "Pool", "Breakfast", "Restaurant"],
         "rating": 9.0, "distance_center_km": 0.5, "rooms_available": 12,
         "highlights": "Centre of action, walking distance to Ben Thanh Market"},
        {"hotel_id": "H_SGN_02", "name": "Bui Vien Backpacker Lodge", "stars": 2,
         "price_per_night_usd": 25, "neighborhood": "Backpacker Street",
         "amenities": ["WiFi", "Bar"],
         "rating": 7.8, "distance_center_km": 1.0, "rooms_available": 35,
         "highlights": "Budget-friendly, buzzing street food and nightlife outside"},
        {"hotel_id": "H_SGN_03", "name": "Saigon Luxury Tower", "stars": 5,
         "price_per_night_usd": 180, "neighborhood": "District 1",
         "amenities": ["WiFi", "Spa", "Pool", "2 Restaurants", "City View"],
         "rating": 9.5, "distance_center_km": 0.3, "rooms_available": 6,
         "highlights": "Panoramic city views, rooftop infinity pool"},
        {"hotel_id": "H_SGN_04", "name": "Pham Ngu Lao Comfort", "stars": 3,
         "price_per_night_usd": 45, "neighborhood": "District 1",
         "amenities": ["WiFi", "Breakfast"],
         "rating": 8.5, "distance_center_km": 0.8, "rooms_available": 22,
         "highlights": "Great mid-range value, helpful staff, easy city access"},
    ],
    "HAN": [
        {"hotel_id": "H_HAN_01", "name": "Old Quarter Heritage Hotel", "stars": 4,
         "price_per_night_usd": 70, "neighborhood": "Old Quarter",
         "amenities": ["WiFi", "Breakfast", "Rooftop Bar"],
         "rating": 9.1, "distance_center_km": 0.3, "rooms_available": 10,
         "highlights": "Historic building, steps from Hoan Kiem Lake, rooftop views"},
        {"hotel_id": "H_HAN_02", "name": "Hanoi Budget Guesthouse", "stars": 2,
         "price_per_night_usd": 20, "neighborhood": "Old Quarter",
         "amenities": ["WiFi"],
         "rating": 7.9, "distance_center_km": 0.5, "rooms_available": 28,
         "highlights": "Most affordable option, authentic local neighbourhood"},
        {"hotel_id": "H_HAN_03", "name": "Tay Ho Lakeside Retreat", "stars": 4,
         "price_per_night_usd": 90, "neighborhood": "Tay Ho (West Lake)",
         "amenities": ["WiFi", "Pool", "Restaurant", "Lake View"],
         "rating": 9.3, "distance_center_km": 5.0, "rooms_available": 8,
         "highlights": "Tranquil lakeside setting, expat neighbourhood, great cafes"},
    ],
}

# ── Daily Cost Estimates ──────────────────────────────────────────────────────
# Average daily spending per person (excluding hotel), in USD

DAILY_COST_ESTIMATES: dict[str, dict] = {
    "PAR": {"low": 60,  "mid": 100, "high": 200, "currency": "EUR", "note": "Museum Pass saves ~€50/week"},
    "TYO": {"low": 50,  "mid": 85,  "high": 180, "currency": "JPY", "note": "IC Card for transit, ~¥1000/day"},
    "LON": {"low": 75,  "mid": 120, "high": 250, "currency": "GBP", "note": "Oyster card for tube, free museums"},
    "BKK": {"low": 30,  "mid": 55,  "high": 120, "currency": "THB", "note": "Street food lunch ~$3, tuk-tuks cheap"},
    "SGN": {"low": 25,  "mid": 45,  "high": 100, "currency": "VND", "note": "Pho breakfast ~$2, Grab rides cheap"},
    "HAN": {"low": 20,  "mid": 40,  "high": 90,  "currency": "VND", "note": "Bun cha lunch ~$2, bia hoi ~$0.50"},
    "SIN": {"low": 70,  "mid": 110, "high": 230, "currency": "SGD", "note": "Hawker centres ~$5/meal"},
    "SYD": {"low": 80,  "mid": 130, "high": 260, "currency": "AUD", "note": "Opal card for transit"},
    "DXB": {"low": 80,  "mid": 130, "high": 300, "currency": "AED", "note": "Alcohol expensive, malls free A/C"},
}

# ── Exchange Rates (to USD) ───────────────────────────────────────────────────
EXCHANGE_RATES: dict[str, float] = {
    "EUR": 0.92,  # 1 USD = 0.92 EUR
    "JPY": 149.5,
    "GBP": 0.79,
    "THB": 35.2,
    "VND": 25100,
    "SGD": 1.35,
    "AUD": 1.55,
    "AED": 3.67,
}
