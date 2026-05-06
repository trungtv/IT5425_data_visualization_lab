import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Lab09 Solution", layout="wide")
st.title("Lab 09 Solution — Data Storytelling")
root = Path(__file__).resolve().parents[2]
df = pd.read_csv(root / "data" / "gapminder.csv")
year = st.slider("Year", int(df.year.min()), int(df.year.max()), 2007)
d = df[df.year == year]
fig = px.scatter(d, x="gdpPercap", y="lifeExp", color="continent", size="pop", log_x=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown("Takeaway: GDP per capita có quan hệ thuận với life expectancy, nhưng khác biệt theo khu vực.")
