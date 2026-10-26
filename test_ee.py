import ee

# Initialize
ee.Initialize(project='verdant-ee-project')

# seed location = Legazpi City
point = ee.Geometry.Point([123.7438, 13.1391])

print("Searching for satellite data...")

# Get image from 2023
dataset = ee.ImageCollection('MODIS/061/MOD11A2') \
    .filterDate('2023-01-01', '2023-12-31') \
    .filterBounds(point)

first_image = dataset.first()

print("Extracting temperature...")

# Reduce the region to a single number
temp_dict = first_image.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=point,
    scale=1000
)

temp_kelvin = temp_dict.get('LST_Day_1km').getInfo()

if temp_kelvin is None:
    print(" That specific pixel was cloudy or missing. Try a different date.")
else:
    temp_celsius = (temp_kelvin * 0.02) - 273.15
    print(f" Legazpi City Temp: {temp_celsius:.2f} °C")