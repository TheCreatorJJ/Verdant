import pandas as pd
import pymannkendall as mk
from scipy.stats import pearsonr

# 1. Load the data
df = pd.read_csv("bicol_climate_data.csv")

print("--- EARTH SYSTEM TREND ANALYSIS ---")

# 2. Mann-Kendall Test for Temperature (Is it getting hotter?)
temp_trend = mk.original_test(df['Temperature_C'])
print("\n🌡️ Temperature Trend Analysis:")
print(f"Trend Direction: {temp_trend.trend}")
print(f"p-value: {temp_trend.p:.4f} (Significant if < 0.05)")
print(f"Sen's Slope (Rate of change): {temp_trend.slope:.3f} °C per year")

# 3. Mann-Kendall Test for Vegetation (Is it getting greener or browner?)
ndvi_trend = mk.original_test(df['NDVI'])
print("\n🌱 Vegetation (NDVI) Trend Analysis:")
print(f"Trend Direction: {ndvi_trend.trend}")
print(f"p-value: {ndvi_trend.p:.4f} (Significant if < 0.05)")
print(f"Sen's Slope (Rate of change): {ndvi_trend.slope:.5f} NDVI per year")

# 4. Pearson Correlation (Do heat and vegetation move together?)
correlation, p_value = pearsonr(df['NDVI'], df['Temperature_C'])
print("\n🔗 Correlation (NDVI vs. Temperature):")
print(f"Pearson Correlation (r): {correlation:.3f}")
print(f"Correlation p-value: {p_value:.4f}")

if correlation < -0.5:
    print("🚨 CONCLUSION: Strong negative correlation! As vegetation drops, heat rises in Bicol.")
else:
    print("ℹ️ CONCLUSION: No strong inverse relationship found.")