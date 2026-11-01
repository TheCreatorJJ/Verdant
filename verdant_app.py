import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pymannkendall as mk

st.set_page_config(page_title="Verdant: Earth Trend Detective", layout="wide")
st.title("🌱 Verdant: Bicol Extreme Heat Detective")
st.markdown("Tracking peak seasonal heat vs. vegetation (2000-2024).")

df = pd.read_csv("bicol_climate_data.csv")

temp_trend = mk.original_test(df['Max_Temp_C'])
ndvi_trend = mk.original_test(df['NDVI'])

col1, col2, col3 = st.columns(3)
col1.metric("Peak Heat Trend", f"{temp_trend.trend.capitalize()}", f"{temp_trend.slope:.3f} °C/yr")
col2.metric("Vegetation Trend", f"{ndvi_trend.trend.capitalize()}", f"{ndvi_trend.slope:.5f} NDVI/yr")
col3.metric("Trend Significance (p-value)", f"{temp_trend.p:.4f}", "Statistically Significant" if temp_trend.p < 0.05 else "Not Significant")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Year'], y=df['Max_Temp_C'], name="Peak Temp (°C)", line=dict(color='firebrick', width=3)))
fig.add_trace(go.Scatter(x=df['Year'], y=df['NDVI'], name="Vegetation Index", yaxis="y2", line=dict(color='forestgreen', width=3)))

fig.update_layout(
    title="Bicol Region: Extreme Heat vs. Vegetation",
    xaxis=dict(title="Year"),
    yaxis=dict(title=dict(text="Peak Temp (°C)", font=dict(color="firebrick")), tickfont=dict(color="firebrick")),
    yaxis2=dict(title=dict(text="NDVI (Greenness)", font=dict(color="forestgreen")), tickfont=dict(color="forestgreen"), anchor="x", overlaying="y", side="right"),
    legend=dict(x=0.01, y=0.99)
)
st.plotly_chart(fig, use_container_width=True)