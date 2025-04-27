import requests
import datetime
from data_storage import store_daily_data, export_data_to_csv

# API Keys & Polygon ID
AGRO_API_KEY = 'your_api_key_here'
POLYGON_ID = 'your_polygon_id_here'

# --- Agromonitoring API Calls ---
def get_current_weather(polygon_id):
    try:
        url = f"https://api.agromonitoring.com/agro/1.0/weather?polyid={polygon_id}&appid={AGRO_API_KEY}"
        response = requests.get(url)
        data = response.json()
        return {
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"]
        }
    except:
        return None

def get_forecast_weather(lat, lon):
    try:
        url = f"https://api.agromonitoring.com/agro/1.0/weather/forecast?lat={lat}&lon={lon}&appid={AGRO_API_KEY}"
        response = requests.get(url)
        data = response.json()
        return data[:3]  # return next 3 forecasts
    except:
        return []

def get_soil_moisture(polygon_id):
    try:
        url = f"https://api.agromonitoring.com/agro/1.0/soilmoisture?polyid={polygon_id}&appid={AGRO_API_KEY}"
        response = requests.get(url)
        data = response.json()
        return data.get("moisture")
    except:
        return None

# --- Crop Suggestion Logic ---
def suggest_crops(soil_moisture, microbial_health, peer_data, weather_desc):
    suggestions = []
    if microbial_health == "high":
        suggestions.extend(["Maize", "Tomatoes", "Lettuce"])
    elif microbial_health == "medium":
        suggestions.extend(["Groundnuts", "Soybeans", "Sunflower"])
    else:
        suggestions.extend(["Sorghum", "Millet", "Cassava"])

    if soil_moisture and soil_moisture < 0.15:
        suggestions = [crop for crop in suggestions if crop in ["Sorghum", "Millet", "Cassava"]]

    if "rain" in weather_desc.lower():
        suggestions.append("Rice")

    if peer_data.lower() not in suggestions:
        suggestions.append(peer_data.capitalize())

    return list(set(suggestions))

# --- Yield & Profit Estimation ---
def estimate_yield_and_profit(crops_count, land_size, microbial_health):
    base_yield = {
        "high": 4.0,
        "medium": 2.5,
        "low": 1.5
    }
    yield_per_crop = base_yield.get(microbial_health, 1.0)
    total_yield = yield_per_crop * land_size * crops_count
    estimated_profit = total_yield * 100  # $100 per tonne estimate
    return total_yield, estimated_profit

# --- Main Program ---
def main():
    print("Welcome to AgriSense360 - Smart Farming Assistant")

    microbial_health = input("Enter your soil microbial health (high, medium, low): ").lower()
    peer_data = input("What are nearby farmers growing?: ")
    crops_count = int(input("How many crops do you want to plant?: "))
    land_size = float(input("Enter your total land size in hectares: "))

    weather = get_current_weather(POLYGON_ID)
    soil_moisture = get_soil_moisture(POLYGON_ID)

    if not weather or soil_moisture is None:
        print("Error fetching weather or soil data. Please check your polygon and API key.")
        return

    # Optional: forecast preview (could be used in future logic)
    forecast = get_forecast_weather(lat=-17.8249, lon=30.9756)

    crop_suggestions = suggest_crops(soil_moisture, microbial_health, peer_data, weather["description"])
    estimated_yield, estimated_profit = estimate_yield_and_profit(crops_count, land_size, microbial_health)

    print("\n--- SMART RECOMMENDATIONS ---")
    print(f"Weather: {weather['description'].capitalize()}, Temperature: {weather['temperature']}°C")
    print(f"Soil Moisture: {soil_moisture:.3f}")
    print(f"Suggested Crops: {', '.join(crop_suggestions)}")
    print(f"Estimated Yield: {estimated_yield:.2f} tonnes")
    print(f"Estimated Profit: ${estimated_profit:.2f}")

    today = datetime.date.today().isoformat()
    data = {
        "date": today,
        "weather": weather['description'],
        "temperature": weather['temperature'],
        "soil_moisture": soil_moisture,
        "microbial_health": microbial_health,
        "peer_data": peer_data,
        "crop_suggestions": crop_suggestions,
        "yield_estimate": estimated_yield,
        "profit_estimate": estimated_profit
    }
    store_daily_data(data)

    export = input("Export results to CSV? (yes/no): ").strip().lower()
    if export == "yes":
        export_data_to_csv()
        print("Data exported successfully.")

if __name__ == "__main__":
    main()
