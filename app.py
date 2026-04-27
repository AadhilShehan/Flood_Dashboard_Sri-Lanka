import streamlit as st
import pandas as pd
df = pd.read_excel("cleaned_flood_data.xlsx")
df["Date"]= pd.to_datetime(df["Date"])

st.title("Flood Impact Dashboard - Sri Lanka")
st.markdown("This dashboard provides insights into the flood impacts across different districts in Sri Lanka, including key metrics, trends, and visualizations to help understand the extent of flooding and its effects on the population and agriculture.")

st.sidebar.header("Filter Options")
districts = st.sidebar.multiselect("Select District", options=df["District"].unique(), default=df["District"].unique())
df_filtered = df[df["District"].isin(districts)]

st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Flooded area (ha)", f"{int(df_filtered["Flooded_Area_ha"].sum()):,}")
col2.metric("Population Exposed", f"{int(df_filtered["Population_Exposed"].sum()):,}")
top_district = (df_filtered.groupby("District")["Flooded_Area_ha"].sum().idxmax())
col3.metric("Most Affected District", top_district)

date_range = st.sidebar.date_input("Select Date Range", [df["Date"].min(), df["Date"].max()])
df_filtered = df[(df["District"].isin(districts)) & (df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]

st.subheader("Flood Trend Over Time")
trend = df_filtered.groupby("Date")["Flooded_Area_ha"].sum()
st.line_chart(trend)
st.caption("This chart shows how flood intensity has changed overtime across selected districts.")

st.subheader("Top Affected Districts")
top_districts = df_filtered.groupby("District")["Flooded_Area_ha"].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_districts)

import matplotlib.pyplot as plt
st.subheader("Population Exposure by District")
population = df_filtered.groupby("District")["Population_Exposed"].sum()
population = population.sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
ax.pie(population, labels=population.index, autopct="%1.1f%%", startangle=140)
st.pyplot(fig)
st.caption("This pie chart highlights the proportion of population exposed to across the most affected districts.")

import seaborn as sns
st.subheader("Agricultural Impact")
heatmap_data = df_filtered.pivot_table(values="Cropland_Flooded_ha", index="District", columns="Date", aggfunc="sum").fillna(0)
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax)
st.pyplot(fig)
st.caption("The heatmap shows agricultural land affected by floods across districts overtime. Darker colours indicate higher impact.")

