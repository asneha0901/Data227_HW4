import streamlit as st
import altair as alt
from utils.io import (overall, paired_long)
from charts.charts import (
    overall_bar, stats)

st.set_page_config(page_title="Story", layout="wide")



st.title("English Premier League Team Performance between Years")
st.markdown("**Central question:** *What are characteristic strategies for team performance improvement?*")

st.header("1) Total Change in Wins for the teams")
st.write("To begin with let us just see which teams improved and which teams fell off")
st.altair_chart(overall_bar(overall), use_container_width=True)
st.write("Takeaway: We can classify 3 groups of teams: those that improved significantly (Nott'm Forest, Brentford and Brighton), those that were consistent players (Aston Villa, Liverpool and Crystal Palace) and those whose performance got a lot worse in the second season (Man United, Arsenal and Tottenham)")
st.write("Using these three categories we can take a closer static look at what kind of changes they share or diverge on depending on fouls, wins and draws")

impteams=["Nott'm Forest", "Brentford", "Brighton"]
sameteams=["Liverpool", "Aston Villa", "Crystal Palace"]
depteams=["Tottenham", "Man United", "Arsenal"]

st.header("2) How do different classes of team performance change appear in terms of per-game performance (as opposed to aggregate ranking)")
st.write("Building upon our takeaway from the first view of team performance, we can start to look at how these teams performed between the two years")
st.altair_chart(stats(paired_long, impteams, "Teams that Improved"), use_container_width=True)
st.altair_chart(stats(paired_long, sameteams, "Teams that were Consistent"), use_container_width=True)
st.altair_chart(stats(paired_long, depteams, "Teams that Declined"), use_container_width=True)

st.header()