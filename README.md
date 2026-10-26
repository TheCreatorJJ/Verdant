# Project Canopy

## Overview
Project Canopy is a data science pipeline that calculates the correlation between vegetation loss (NDVI) and rising Land Surface Temperature (LST) using NASA MODIS satellite data.

## The Hypothesis
In Bicol, Philippines, rapid deforestation is directly causing a rise in land surface temperatures. By correlating 5 years of satellite data, we can prove this causal link.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Authenticate Earth Engine: `earthengine authenticate`
3. Run the script: `python canopy_engine.py`
4. View the generated chart: `legazpi_correlation.png`

## Output
The script generates a dual-axis chart showing the inverse relationship between NDVI (Green) and LST (Red) over time, alongside a Pearson correlation coefficient.