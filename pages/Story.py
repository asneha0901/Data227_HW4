import streamlit as st
import altair as alt
from utils.io import (overall)
from charts.charts import (
    overall_bar)

st.set_page_config(page_title="Story", layout="wide")



st.title("A Data Story: Seattle Weather Patterns")
st.markdown("**Central question:** *What patterns (seasonality and extremes) show up in daily weather over time?*")

st.header("1) Total Change in Wins for the teams")
st.write("To begin with let us just see which teams improved and which teams fell off")
st.altair_chart(overall_bar(overall), use_container_width=True)
st.caption("Takeaway:")