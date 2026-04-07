"""
Data loader for Travel Agent - Prepares data for future DB integration
"""

from tools import FLIGHTS_DB, HOTELS_DB


def load_flights_database():
    """
    Load flights database
    In the future, this could connect to a real API or database
    """
    return FLIGHTS_DB


def load_hotels_database():
    """
    Load hotels database
    In the future, this could connect to a real API or database
    """
    return HOTELS_DB


def get_available_cities():
    """Get list of cities with available flights"""
    cities = set()
    for origin, destination in FLIGHTS_DB.keys():
        cities.add(origin)
        cities.add(destination)
    return sorted(list(cities))


def get_available_hotels_cities():
    """Get list of cities with available hotels"""
    return sorted(list(HOTELS_DB.keys()))


def get_flight_routes():
    """Get all available flight routes"""
    return list(FLIGHTS_DB.keys())


def print_database_summary():
    """Print a summary of available flights and hotels"""
    print("=" * 60)
    print("🗂️  DATA LOADER - DATABASE SUMMARY")
    print("=" * 60)
    
    print("\n✈️  FLIGHTS DATABASE:")
    print(f"  - Total routes: {len(FLIGHTS_DB)}")
    for route, flights in FLIGHTS_DB.items():
        print(f"    {route[0]} → {route[1]}: {len(flights)} flights")
    
    print("\n🏨 HOTELS DATABASE:")
    print(f"  - Total cities: {len(HOTELS_DB)}")
    for city, hotels in HOTELS_DB.items():
        print(f"    {city}: {len(hotels)} hotels")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print_database_summary()
