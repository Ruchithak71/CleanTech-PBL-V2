from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import requests

app = Flask(__name__)
CORS(app)

# Load your scaler and model (update the paths if needed)
scaler = joblib.load('models/xgb_scaler.pkl')
model = joblib.load('models/xgb_air_quality_model.pkl')

OPENWEATHER_API_KEY = 'c24dccc817c29f3a8ccbc2867b0b3ccc'  # <-- Replace with your real API key

def get_aqi_message(aqi):
    if aqi <= 50:
        return {"message": "Air is fresh! Take a deep breath 🌳", "media": "media/fresh-air.mp4"}
    elif aqi <= 100:
        return {"message": "Decent air. A good day for a walk 🚶", "media": "media/walking.mp4"}
    elif aqi <= 200:
        return {"message": "Sensitive folks, maybe wear a mask 😷", "media": "media/mask.mp4"}
    elif aqi <= 300:
        return {"message": "Limit outdoor activity. Mask up 😷", "media": "media/pollution.mp4"}
    elif aqi <= 400:
        return {"message": "Air is bad. Stay indoors if you can 🏠", "media": "media/pollution.mp4"}
    else:
        return {"message": "Airpocalypse! Avoid going out 🚨", "media": "media/pollution1.mp4"}

@app.route('/realtime-aqi', methods=['GET'])
def realtime_aqi():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        if not lat or not lon:
            return jsonify({'error': 'Missing latitude or longitude'}), 400

        # Fetch real-time pollutant data from OpenWeatherMap
        url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}'
        resp = requests.get(url)
        data = resp.json()
        if 'list' not in data or not data['list']:
            return jsonify({'error': 'No data from OpenWeatherMap'}), 500

        components = data['list'][0]['components']
        # Map OpenWeatherMap keys to your model's features
        features = ['CO', 'NO', 'NO2', 'NOx', 'O3', 'SO2', 'PM2.5', 'PM10', 'NH3']
        feature_map = {
            'CO': components.get('co', 0),
            'NO': components.get('no', 0),
            'NO2': components.get('no2', 0),
            'NOx': components.get('no', 0) + components.get('no2', 0),
            'O3': components.get('o3', 0),
            'SO2': components.get('so2', 0),
            'PM2.5': components.get('pm2_5', 0),
            'PM10': components.get('pm10', 0),
            'NH3': components.get('nh3', 0)
        }
        input_values = [feature_map[f] for f in features]

        arr = np.array(input_values).reshape(1, -1)
        arr_scaled = scaler.transform(arr)
        predicted_aqi = model.predict(arr_scaled)[0]
        msg_obj = get_aqi_message(predicted_aqi)

        return jsonify({
            'predicted_aqi': float(predicted_aqi),
            'message': msg_obj['message'],
            'media': msg_obj['media'],
            **feature_map
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)