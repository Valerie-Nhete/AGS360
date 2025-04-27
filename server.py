from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# OpenWeather API Key
OPENWEATHER_API_KEY = "your_api_key_here"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return temperature, description
    else:
        return None, None

@app.route('/')
def home():
    return "AgriSense360 Backend Server Running!"

@app.route('/process', methods=['POST'])
def process_data():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    city = data.get('city')
    soil_ph = float(data.get('soil_ph'))
    microbial_health = data.get('microbial_health')
    crop = data.get('crop')
    land_size = float(data.get('land_size'))
    crops_count = int(data.get('crops_count'))

    # --- Fetch real weather data ---
    temperature, weather_description = get_weather(city)

    # --- Smart crop suggestion logic ---
    crop_suggestions = []
    if microbial_health == "high":
        crop_suggestions = ["Maize", "Tomatoes", "Lettuce"]
    elif microbial_health == "medium":
        crop_suggestions = ["Groundnuts", "Soybeans", "Sunflower"]
    else:
        crop_suggestions = ["Sorghum", "Millet", "Cassava"]

    if soil_ph < 5.5:
        crop_suggestions = [c for c in crop_suggestions if c not in ["Lettuce", "Soybeans"]]
    elif soil_ph > 7.5:
        crop_suggestions = [c for c in crop_suggestions if c not in ["Tomatoes", "Groundnuts"]]

    # Estimating yield and profit
    base_yield = {
        "high": 4.0,
        "medium": 2.5,
        "low": 1.5
    }
    yield_per_crop = base_yield.get(microbial_health, 1.0)
    total_yield = yield_per_crop * land_size * crops_count
    estimated_profit = total_yield * 100  # $100 per tonne assumption

    response = {
        "temperature": temperature,
        "weather_description": weather_description,
        "crop_suggestions": crop_suggestions,
        "estimated_yield": round(total_yield, 2),
        "estimated_profit": round(estimated_profit, 2)
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)