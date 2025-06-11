import pandas as pd
import requests
import numpy as np
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
scaler = joblib.load(os.path.join(BASE_DIR, 'models', 'xgb_scaler.pkl'))
model = joblib.load(os.path.join(BASE_DIR, 'models', 'xgb_air_quality_model.pkl'))
df = pd.read_excel(os.path.join(BASE_DIR, 'air_data.xlsx'), sheet_name='Air Quality')

def get_aqi_message(aqi):
    if aqi <= 50:
        return "Air is fresh! Take a deep breath 🌳"
    elif aqi <= 100:
        return "Decent air. A good day for a walk 🚶"
    elif aqi <= 200:
        return "Sensitive folks, maybe wear a mask 😷"
    elif aqi <= 300:
        return "Limit outdoor activity. Mask up 😷"
    elif aqi <= 400:
        return "Air is bad. Stay indoors if you can 🏠"
    else:
        return "Airpocalypse! Avoid going out 🚨"

# Define required features
features = ['CO', 'NO', 'NO2', 'NOx', 'O3', 'SO2', 'PM2.5', 'PM10', 'NH3']

API_KEY = 'c24dccc817c29f3a8ccbc2867b0b3ccc'
LAT = 12.825089
LON = 77.515091

url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}'
response = requests.get(url)
data = response.json()
pollutants = data['list'][0]['components']

today_data = {
    'CO': pollutants['co'],
    'NO': pollutants['no'],
    'NO2': pollutants['no2'],
    'NOx': pollutants['no'] + pollutants['no2'],
    'O3': pollutants['o3'],
    'SO2': pollutants['so2'],
    'PM2.5': pollutants['pm2_5'],
    'PM10': pollutants['pm10'],
    'NH3': pollutants['nh3']
}

input_values = [today_data[f] for f in features]
arr = np.array(input_values).reshape(1, -1)
arr_scaled = scaler.transform(arr)
predicted_aqi = model.predict(arr_scaled)[0]
message = get_aqi_message(predicted_aqi)
print(f"\n🌐 Real-time AQI for your campus: {predicted_aqi:.2f} → {message}\n")

# Drop rows with missing feature data
df = df.dropna(subset=features)

# Scale and predict
X = scaler.transform(df[features])
predictions = model.predict(X)
df['Predicted_AQI'] = predictions
df['Message'] = df['Predicted_AQI'].apply(get_aqi_message)

# Show latest 5 predictions
print("\n📢 AQI Predictions and Health Advice:\n")
for i, row in df.tail(5).iterrows():
    print(f"🔹 Predicted AQI: {row['Predicted_AQI']:.2f} → {row['Message']}")

# Save results
df.to_excel(os.path.join(BASE_DIR, 'predicted_air_data.xlsx'), index=False)
print("\n✅ Full predictions saved to 'predicted_air_data.xlsx'")

# Prepare a DataFrame for the real-time prediction
realtime_df = pd.DataFrame([{
    'CO': today_data['CO'],
    'NO': today_data['NO'],
    'NO2': today_data['NO2'],
    'NOx': today_data['NOx'],
    'O3': today_data['O3'],
    'SO2': today_data['SO2'],
    'PM2.5': today_data['PM2.5'],
    'PM10': today_data['PM10'],
    'NH3': today_data['NH3'],
    'Predicted_AQI': predicted_aqi,
    'Message': message,
    'Source': 'Real-time API'
}])

# Add a 'Source' column to the batch DataFrame for clarity
df['Source'] = 'Historical'

# Concatenate the real-time row with the batch predictions
final_df = pd.concat([df, realtime_df], ignore_index=True)

# Save the combined DataFrame
final_df.to_excel(os.path.join(BASE_DIR, 'predicted_air_data.xlsx'), index=False)
print("\n✅ Full predictions (including real-time) saved to 'predicted_air_data.xlsx'")