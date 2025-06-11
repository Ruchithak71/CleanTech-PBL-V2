import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
import joblib

# Load the processed data
df = pd.read_csv('processed_air_data.csv')

# Define features and target
features = ['CO', 'NO', 'NO2', 'NOx', 'O3', 'SO2', 'PM2.5', 'PM10', 'NH3']
target = 'AQI'

X = df[features]
y = df[target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)

print("📊 Model Evaluation:")
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R² Score:", r2_score(y_test, y_pred))

# Save model and scaler
joblib.dump(model, 'models/xgb_air_quality_model.pkl')
joblib.dump(scaler, 'models/xgb_scaler.pkl')
print("✅ Model and scaler saved.")
