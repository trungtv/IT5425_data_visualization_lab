"""
IT5425 Lab 09 — mở rộng skeleton này theo notebook.
Chạy: streamlit run app.py
"""

import plotly.express as px
import streamlit as st

st.set_page_config(page_title="IT5425 Lab 09", layout="wide")
st.title("Data storytelling (template)")

df = px.data.gapminder()
st.markdown(
    "Thay Gapminder bằng dataset của bạn; thêm **các section** tương ứng "
    "_setup → insight → takeaway_ theo Ch.9."
)

year = st.slider("Year", int(df.year.min()), int(df.year.max()), 2007)
subset = df[df.year == year].copy()

col1, col2 = st.columns(2)
with col1:
    continents = sorted(subset.continent.unique())
    pick = st.multiselect("Continents", continents, default=continents)
with col2:
    st.metric("Countries (filtered)", len(subset[subset.continent.isin(pick)]))

filt = subset[subset.continent.isin(pick)]
fig = px.scatter(
    filt,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=55,
    title=f"GDP per capita vs life expectancy — {year}",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Reflection slot")
st.text_area(
    "Ghi 2–3 câu narrative bạn muốn reader nhớ sau khi dùng app (sẽ chuyển vào báo cáo).",
    key="reflection",
)
