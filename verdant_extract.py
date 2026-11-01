import ee
import pandas as pd
import time

ee.Initialize(project='verdant-ee-project') 

legazpi = ee.Geometry.Point([123.7438, 13.1391])
# SMALLER AREA: 10km radius to focus on the city and avoid the ocean
aoi = legazpi.buffer(10000) 

print("Fetching refined urban heat data (April only)...")

data = []

for year in range(2000, 2025):
    # Focus ONLY on April (The hottest month)
    start_date = f'{year}-04-01'
    end_date = f'{year}-04-30'
    
    try:
        # 1. Get NDVI (Use MEAN for the month)
        ndvi_col = ee.ImageCollection('MODIS/061/MOD13Q1') \
            .filterDate(start_date, end_date) \
            .filterBounds(aoi)
        ndvi_val = ndvi_col.select('NDVI').mean().multiply(0.0001).reduceRegion(
            reducer=ee.Reducer.mean(), geometry=aoi, scale=250).get('NDVI').getInfo()
        
        # 2. Get LST (Use MEDIAN of the daily maximums to avoid cloud/sensor noise)
        lst_col = ee.ImageCollection('MODIS/061/MOD11A2') \
            .filterDate(start_date, end_date) \
            .filterBounds(aoi)
            
        # We take the mean of the LST_Day_1km band for April
        lst_val = lst_col.select('LST_Day_1km').mean().multiply(0.02).subtract(273.15).reduceRegion(
            reducer=ee.Reducer.mean(), geometry=aoi, scale=1000).get('LST_Day_1km').getInfo()
        
        if ndvi_val is not None and lst_val is not None:
            data.append({
                "Year": year,
                "NDVI": round(ndvi_val, 4),
                "Max_Temp_C": round(lst_val, 2) 
            })
            print(f"Year {year}: April Avg Temp={lst_val:.1f}°C")
            
        time.sleep(1) 
    except Exception as e:
        print(f"Skipping {year}: {e}")

df = pd.DataFrame(data)
df.to_csv("bicol_climate_data.csv", index=False)