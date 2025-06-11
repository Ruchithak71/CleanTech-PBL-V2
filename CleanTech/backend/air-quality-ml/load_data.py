# load_data.py

import pandas as pd
from add_aqi import calculate_overall_aqi

# Load Excel
df = pd.read_excel('air_data.xlsx', sheet_name='Air Quality')

# Add AQI column
df['AQI'] = df.apply(calculate_overall_aqi, axis=1)

# Save updated DataFrame for training
df.to_csv('processed_air_data.csv', index=False)

print("✅ Data loaded and AQI calculated. Saved to data/processed_air_data.csv")

