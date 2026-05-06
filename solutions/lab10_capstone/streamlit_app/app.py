import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Capstone Solution", layout="wide")
st.title("Capstone Solution Dashboard")
root = Path(__file__).resolve().parents[3]
df = pd.read_csv(root / "data" / "gapminder.csv")
continent = st.selectbox("Continent", sorted(df.continent.unique()))
d = df[df.continent == continent]
fig = px.line(d.groupby("year", as_index=False).agg(lifeExp=("lifeExp", "mean")), x="year", y="lifeExp")
st.plotly_chart(fig, use_container_width=True)
st.caption("Narrative: tiến bộ life expectancy theo thời gian của từng châu lục.")
