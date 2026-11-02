import pandas as pd
import pymannkendall as mk
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("bicol_climate_data.csv")

print("--- VERDANT CLIMATE ANALYSIS ---")

# 1. Trend Analysis
df['LST_Rolling'] = df['LST_Max'].rolling(window=3, center=True).mean()
trend_data = df.dropna(subset=['LST_Rolling'])
temp_trend = mk.hamed_rao_modification_test(trend_data['LST_Rolling'])
print(f"Smoothed Trend: {temp_trend.trend.upper()} (p-value: {temp_trend.p:.4f})")

# 2. Random Forest Attribution
X = df[['NDVI', 'Nightlights']]
y = df['LST_Max']

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)

print(f"NDVI Influence: {rf_model.feature_importances_[0]*100:.1f}%")
print(f"Nightlights Influence: {rf_model.feature_importances_[1]*100:.1f}%")