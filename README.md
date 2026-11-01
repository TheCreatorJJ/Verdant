# Project Verdant

## Overview
Project Verdant is a data science pipeline that investigates the correlation between vegetation loss (NDVI) and rising Land Surface Temperature (LST) using 24 years of NASA MODIS satellite data via Google Earth Engine.

## The Hypothesis
In tropical archipelagos like Bicol, Philippines, rapid deforestation and urbanization are directly causing an increase in extreme land surface temperatures. By extracting and analyzing long-term satellite data, this project aims to quantify that relationship and detect statistically significant climate trends.

## Methodology
1. **Data Extraction:** Pulls 24 years (2000-2024) of MODIS `MOD13Q1` (NDVI) and `MOD11A2` (LST) data.
2. **Statistical Analysis:** Utilizes the **Mann-Kendall Trend Test** and **Sen's Slope** to detect the presence and magnitude of climate trends. Calculates Pearson correlation to link vegetation loss with heat anomalies.
3. **Visualization:** Generates a Streamlit dashboard for visual trend detection.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Authenticate Earth Engine: `earthengine authenticate`
3. Extract Data: `python verdant_extract.py`
4. Run Analysis: `python verdant_analyze.py`
5. View Dashboard: `streamlit run verdant_app.py`

## Key Findings (Preliminary)
- Average baseline temperatures in Bicol show high volatility due to El Niño/La Niña cycles.
- Extremes (maximum temperatures) show a more pronounced trend than averages, indicating that climate adaptation must focus on extreme event frequency rather than just mean temperatures.