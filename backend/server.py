from flask import Flask, request, jsonify, send_from_directory
import random
import datetime

app = Flask(__name__, static_folder='public')

# Example crop database
CROP_DATABASE = {
    'neutral': ['Maize', 'Soybean', 'Sorghum', 'Cowpeas'],
    'acidic': ['Cassava', 'Sweet potatoes', 'Pineapple'],
    'alkaline': ['Barley', 'Beets', 'Alfalfa']
}

@app.route('/process', methods=['POST'])
def process_data():
    data = request.get_json()

    city = data.get('city')
    soil_ph = data.get('soil_ph')
    microbial_health = data.get('microbial_health')
    nearby_crops = data.get('nearby_crops')
    num_crops = data.get('num_crops')
    land_size = data.get('land_size')

    # Simulate weather and soil data
    temperature = round(random.uniform(20, 30), 2)
    soil_moisture = round(random.uniform(10, 35), 2)
    weather = random.choice(['Sunny', 'Rainy', 'Cloudy'])

    # Determine pH type
    ph_type = 'neutral'
    try:
        ph_value = float(soil_ph)
        if ph_value < 6.5:
            ph_type = 'acidic'
        elif ph_value > 7.5:
            ph_type = 'alkaline'
    except:
        ph_type = 'neutral'

    suggested_crops = random.sample(CROP_DATABASE.get(ph_type, []), min(3, len(CROP_DATABASE.get(ph_type, []))))

    estimated_yield = round(float(land_size) * random.uniform(1.5, 3.5), 2)
    estimated_profit = round(estimated_yield * random.uniform(300, 600), 2)

    collected_result = {
        'city': city,
        'temperature': temperature,
        'soil_moisture': soil_moisture,
        'weather': weather,
        'soil_ph': soil_ph,
        'microbial_health': microbial_health,
        'nearby_crops': nearby_crops,
        'suggested_crops': suggested_crops,
        'estimated_yield': estimated_yield,
        'estimated_profit': estimated_profit,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify({'message': 'Data received successfully!', 'result': collected_result})

# Serve frontend files
@app.route('/')
def serve_index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory('public', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)