import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Verdant Spatial Analysis", layout="wide")
st.title("🗺️ Verdant: Spatial Anomaly Analysis")
st.markdown("Grid-based Z-score detection for the May 2023 period.")

try:
    df = pd.read_csv("bicol_grid_anomalies.csv")
except FileNotFoundError:
    st.error("Please run `verdant_grid_extract.py` first to generate the data.")
    st.stop()

total_points = len(df)
extreme_points = len(df[df['is_extreme'] == True])
max_z = df['z_score'].max()

extreme_delta = "Alert" if extreme_points > 0 else "Normal"
extreme_color = "inverse" if extreme_points > 0 else "normal"

col1, col2, col3 = st.columns(3)
col1.metric("Total Grid Points", total_points)
col2.metric("Extreme Anomalies (Z > 2)", extreme_points, extreme_delta, delta_color=extreme_color)
col3.metric("Max Z-Score", max_z, "Peak Heat")

st.markdown("---")
st.subheader("Spatial Heat Anomaly Map")
st.markdown("Red dots indicate areas where the temperature was **more than 2 standard deviations** above the 20-year baseline.")

# FIXED: Removed map_bounds from px.scatter_map
fig = px.scatter_map(
    df, 
    lat="lat", 
    lon="lon", 
    color="z_score",
    size=df['z_score'].abs() + 0.5, 
    color_continuous_scale=px.colors.diverging.RdBu_r, 
    range_color=[-3, 3], 
    zoom=7.0, 
    center={"lat": 13.0, "lon": 123.5}, 
    hover_data=["current_temp", "baseline_temp", "z_score"]
)

# FIXED: Set bounds inside update_layout
fig.update_layout(
    map_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0},
    coloraxis_colorbar=dict(title="Z-Score"),
    map=dict(
        bounds=dict(west=122.0, east=125.0, south=11.5, north=14.5)
    )
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### Analytical Context")
st.info("This spatial methodology demonstrates how regional grids can be processed to identify localized temperature extremes against historical baselines.")