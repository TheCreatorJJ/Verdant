import ee
import pandas as pd

ee.Initialize(project='verdant-ee-project')
bicol_region = ee.Geometry.Rectangle([122.0, 11.5, 125.0, 14.5])

# Create Grid
lat_list = [11.5 + i * 0.2 for i in range(15)]
lon_list = [122.0 + i * 0.2 for i in range(15)]
grid_points = [ee.Feature(ee.Geometry.Point([lon, lat]), {'lat': lat, 'lon': lon}) 
               for lat in lat_list for lon in lon_list]
bicol_grid = ee.FeatureCollection(grid_points)

def get_lst_collection(start_date, end_date):
    return ee.ImageCollection('MODIS/061/MOD11A2') \
        .filterDate(start_date, end_date) \
        .filterBounds(bicol_region) \
        .select('LST_Day_1km') \
        .map(lambda img: img.multiply(0.02).subtract(273.15))

print("1. Calculating 20-Year Baseline (Temporal Mean & StdDev)...")
baseline_col = get_lst_collection('2000-05-01', '2020-05-31')

# Reduce over TIME to get the mean and stdDev for each pixel
baseline_img = baseline_col.reduce(ee.Reducer.mean().combine(ee.Reducer.stdDev(), sharedInputs=True))

# Extract baseline stats for the grid
baseline_stats = baseline_img.reduceRegions(
    collection=bicol_grid,
    reducer=ee.Reducer.first(), # Use 'first' because the image already has mean/stdDev bands
    scale=1000
).getInfo()

baseline_dict = {}
for feature in baseline_stats['features']:
    lat = feature['properties']['lat']
    lon = feature['properties']['lon']
    mean = feature['properties'].get('LST_Day_1km_mean')
    std = feature['properties'].get('LST_Day_1km_stdDev')
    
    if mean is not None and std is not None and std > 0:
        baseline_dict[(lat, lon)] = (mean, std)

print(f"✅ Found valid baseline data for {len(baseline_dict)} out of {len(grid_points)} grid points.")

print("2. Calculating Current Temp for May 2023...")
current_col = get_lst_collection('2023-05-01', '2023-05-31')
current_img = current_col.mean() # Spatial mean for the current month

current_stats = current_img.reduceRegions(
    collection=bicol_grid,
    reducer=ee.Reducer.mean(),
    scale=1000
).getInfo()

print("3. Calculating Z-Scores...")
data = []

for feature in current_stats['features']:
    lat = feature['properties']['lat']
    lon = feature['properties']['lon']
    current_temp = feature['properties'].get('mean')
    
    if (lat, lon) in baseline_dict and current_temp is not None:
        mean, std = baseline_dict[(lat, lon)]
        z_score = (current_temp - mean) / std
        is_extreme = bool(abs(z_score) > 2.0)
        
        data.append({
            "lat": lat,
            "lon": lon,
            "current_temp": round(current_temp, 2),
            "baseline_temp": round(mean, 2),
            "z_score": round(z_score, 2),
            "is_extreme": is_extreme
        })

if len(data) > 0:
    df = pd.DataFrame(data)
    df.to_csv("bicol_grid_anomalies.csv", index=False)
    print(f"\n✅ Successfully calculated Z-scores for {len(data)} grid points and saved to CSV!")
else:
    print("\n❌ Data list is still empty.")