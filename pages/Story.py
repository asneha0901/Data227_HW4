import streamlit as st
import altair as alt
from utils.io import (overall, paired_long, offense_long_all, defense_long_all)
from charts.charts import (
    overall_bar, stats, offense_chart, defense_chart, final_dashboard, right_panel, offense_home)

st.set_page_config(page_title="Story", layout="wide")



st.title("English Premier League Team Performance between Years")
st.header("**Central question:** *What are characteristic strategies for team performance improvement?*")

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
st.write("Some general observations we can make about teams that improved are that they obviously have more wins but also seem to decrease in fouls")
st.altair_chart(stats(paired_long, sameteams, "Teams that were Consistent"), use_container_width=True)
st.write("Some general observations we can make about teams that were consistent are that they obviously have similar wins between seasons but also seem to be consistent with draws and fouls.")
st.altair_chart(stats(paired_long, depteams, "Teams that Declined"), use_container_width=True)
st.write("Some general observations we can make about teams that declined are that they obviously have fewer wins between seasons but also seem to have more fouls..")


homeimp=(offense_chart(offense_long_all, impteams, "2324", "Home", "Home Offense Games for 2324", "greens")|offense_chart(offense_long_all, impteams, "2425", "Home","Home Offense Games for 2425", "greens"))
awayimp=(offense_chart(offense_long_all, impteams, "2324", "Away", "Away Offense Games for 2324", "greens")|offense_chart(offense_long_all, impteams, "2425", "Away","Away Games for 2425", "greens"))
imp=(homeimp & awayimp).properties(title="Teams that improved").configure_title(anchor="middle")
homesame=(offense_chart(offense_long_all, sameteams, "2324", "Home", "Home Offense Games for 2324", "blues")|offense_chart(offense_long_all, sameteams, "2425", "Home","Home Offense Games for 2425", "blues"))
awaysame=(offense_chart(offense_long_all, sameteams, "2324", "Away", "Away Offense Games for 2324", "blues")|offense_chart(offense_long_all, sameteams, "2425", "Away","Away Offense Games for 2425", "blues"))
same=(homesame & awaysame).properties(title="Teams that were consistent").configure_title(anchor="middle")
homedep=(offense_chart(offense_long_all, depteams, "2324", "Home", "Home Offense Games for 2324", "purples")|offense_chart(offense_long_all, depteams, "2425", "Home","Home Offense Games for 2425", "purples"))
awaydep=(offense_chart(offense_long_all, depteams, "2324", "Away", "Away Offense Games for 2324", "purples")|offense_chart(offense_long_all, depteams, "2425", "Away","Away Offense Games for 2425", "purples"))
dep=(homedep & awaydep).properties(title="Teams that declined").configure_title(anchor="middle")


st.header("3) Are there trends between teams improving their home and/or away **OFFENSE** performance between seasons?")
st.subheader("First we can look at the teams that improved between seasons")
st.altair_chart(imp, use_container_width=True)
st.write("A Key observation for teams that improved is that seemingly even though their performance in terms of offense in home games stays fairly similar between seasons, all 3 teams seem to have performed a lot better in away games in the second season as opposed to the first. This might indicate that a cause behind their improvement is correlated with better performance in away games/ less of a home advantage phenotype observed with these teams.")
st.subheader("Next we can look at the teams that were consistent between seasons")
st.altair_chart(same, use_container_width=True)
st.write("A Key observation for teams that stayed consistent between seasons is that they seem to attempt more shots in total than the teams above which might be a possible strategy for evening out the odds of successful shots.")
st.subheader("Lastly we can look at the teams that declined between seasons")
st.altair_chart(dep, use_container_width=True)
st.write("It seems pretty clearly that teams that declined in performance also overall attempted few shots, both on target or not. This might indicate that it is better for teams (when combining this observation with that of teams that stayed consistent) to attempt more shots even if the accuracy rate is low.")
st.subheader("Summary of Observations and Recommendations")
st.write("Based on the graphs and analysis above it seems that teams should keep two important points in mind: \n" 
"1. To increase chances of consistent performance and prevent low scores, it is better to attempt more shots irregardless of success rates \n" 
"2. For improved performance, a potential offense strategy is to specifically improve away game performance and decrease the margin of home advantage.")

dhomeimp=(defense_chart(defense_long_all, impteams, "2324", "Home", "Home Defense Games for 2324")|defense_chart(defense_long_all, impteams, "2425", "Home", "Home Defense Games for 2425"))
dawayimp=(defense_chart(defense_long_all, impteams, "2324", "Away", "Away Defense Games for 2324")|defense_chart(defense_long_all, impteams, "2425", "Away", "Away Defense Games for 2425"))
dimp=(dhomeimp & dawayimp).properties(title="Teams that improved").configure_title(anchor="middle")

dhomesame=(defense_chart(defense_long_all, sameteams, "2324", "Home", "Home Defense Games for 2324")|defense_chart(defense_long_all, sameteams, "2425", "Home", "Home Defense Games for 2425"))
dawaysame=(defense_chart(defense_long_all, sameteams, "2324", "Away", "Away Defense Games for 2324")|defense_chart(defense_long_all, sameteams, "2425", "Away", "Away Defense Games for 2425"))
dsame=(dhomesame & dawaysame).properties(title="Teams that were consistent").configure_title(anchor="middle")

dhomedep=(defense_chart(defense_long_all, depteams, "2324", "Home", "Home Defense Games for 2324")|defense_chart(defense_long_all, depteams, "2425", "Home", "Home Defense Games for 2425"))
dawaydep=(defense_chart(defense_long_all, depteams, "2324", "Away", "Away Defense Games for 2324")|defense_chart(defense_long_all, depteams, "2425", "Away", "Away Defense Games for 2425"))
ddep=(dhomedep & dawaydep).properties(title="Teams that Declined").configure_title(anchor="middle")

st.header("3) Are there trends between teams improving their home and/or away **DEFENSE** performance between seasons?")
st.subheader("First we can look at the teams that improved between seasons")
st.altair_chart(dimp, use_container_width=True)
st.subheader("Next we can look at the teams that were consistent between seasons")
st.altair_chart(dsame, use_container_width=True)
st.subheader("Lastly we can look at the teams that declined between seasons")
st.altair_chart(ddep, use_container_width=True)
st.subheader("Summary of observation")
st.write("1. There is direct correlation between a teams performance in wins and their defense strategies. Teams that improved also had improved defense and vice versa. \n"
"2. It seems as though the number of shots blocked by a team is a better indicator than the corners they take which means it might be more effective to block goals once they reach target as opposed to kick them off the field when it is in the box.")

season_radio = alt.binding_radio(
    options=["2324", "2425"],
    labels=["23-24 Season", "24-25 Season"],
    name="Select Season:  "
)

season_select = alt.param(name="chosen_season", bind=season_radio, value="2324")
st.header("4) Interactive Dashboard to see other teams")
st.write("Use this interactive dashboard to figure out how specific teams performed in these two seasons and ask yourself similar analysis questions as the ones shown above for the three categories.")
st.write("1. How much of an advantage is home advantage? Does home advantage usually correlate with a stronger defense or offense or both?")
st.write("2. Is there a correlation between shots taken, shots on target, goals and winning the game?") 
st.write("3. Is it perhaps better to attempt more shots even if shot success rate is low?") 
st.write("4. Did certain teams perform better in the first season as opposed to the second?")
st.write("ALTAIR STREAMLIT COMPATIBILITY ISSUE DOESN'T ALLOW THE WHOLE INTERACTIVE DASHBOARD TO BE DISPLAYED - THIS BUG IS WELL DOCUMENTED IN MULTIPLE STREAMLIT DISCUSSION FORUMS AND THERE IS NO PROPOSED SOLUTION THAT WORKS. please not this is entirely out of my control and a bug on the side of streamlit. the code works as expected since it is the exact same as HW3 for the interactive dashboard.")
st.altair_chart(final_dashboard, width="content")
