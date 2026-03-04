
import altair as alt
import pandas as pd

#MAKING THE STATIC STORIES

def overall_bar(df: pd.DataFrame) -> alt.Chart:
    sel = alt.selection_point(fields=["Team"], toggle=True, empty="none")
    return(alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("Team:N", sort='-y',
                axis=alt.Axis(labelAngle=-90)),
        y=alt.Y("WinsDiff_2425_minus_2324vals:Q", title="Wins (24-25 minus 23-24)"),
        color=alt.Color("Team:N", legend=None),
        opacity=alt.condition(sel, alt.value(1.0), alt.value(0.25)),
        tooltip=[
            alt.Tooltip("Team:N"),
            alt.Tooltip("Wins_2425:Q", title="Wins 2425"),
            alt.Tooltip("Wins_2324:Q", title="Wins 2324"),
            alt.Tooltip("WinsDiff_2425_minus_2324title:Q", title="\u0394 Wins"),
        ],
    )
    .add_params(sel)
    .properties(width=340, height=380, title="Change in Wins (23-24 to 24-25)"))



def stats(paired_long, teams, chart_title):
    base_right = (
        alt.Chart(paired_long)
        .transform_filter(alt.FieldOneOfPredicate(field='Team', oneOf=teams))
        .encode(
            x=alt.X("season:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("value:Q", title=None),
            color=alt.Color("Team:N", legend=alt.Legend(title="Selected Teams")),
            detail="Team:N",
        )
    )

    paired_lines  = base_right.mark_line()
    paired_points = base_right.mark_point(size=120)
    paired_labels = (
        base_right
        .transform_filter(alt.datum.season == "2425")
        .mark_text(align="left", dx=8, dy=0)
        .encode(text="Team:N")
    )

    def trend_panel(metric_name, y_title, panel_title):
        return (
            alt.layer(paired_lines, paired_points, paired_labels)
            .transform_filter(alt.datum.metric == metric_name)
            .encode(y=alt.Y("value:Q", title=y_title))
            .properties(width=380, height=115, title=panel_title)
        )

    middle_side = alt.hconcat(
        trend_panel("Wins",     "Wins",      "Wins (23-24 to 24-25)"),
        trend_panel("Draws",    "Draws",     "Draws (23-24 to 24-25)"),
        trend_panel("RedCards", "Red Cards", "Red Cards (23-24 to 24-25)"),
    ).resolve_scale(y="independent").properties(title=chart_title)
    return middle_side

def offense_chart(offense_long_all, teams, season, venue, title, scheme):
    offense = alt.Chart(offense_long_all).transform_filter(alt.FieldOneOfPredicate(field='Team', oneOf=teams)).transform_filter(alt.datum.Season == season).transform_filter(alt.datum.Venue == venue).mark_bar().encode(
    x=alt.X(
        "Team:N",
        sort=alt.SortField("ShotsAttempted:Q", order="descending"),
        axis=alt.Axis(labelAngle=-45),
        title=None,
    ),
    y=alt.Y("sum(Count):Q", title="Shots"),
    color=alt.Color("ComponentLabel:N", scale=alt.Scale(scheme=scheme), legend=alt.Legend(title=None, orient="bottom")),
    order=alt.Order("Component:O"),
    tooltip=[
        alt.Tooltip("Team:N"),
        alt.Tooltip("sum(Count):Q", title="Total shots"),
    ],
    ).properties(width=310, height=200, title=title)
    return offense

def defense_chart(defense_long_all, team,season, venue, title):
    base = (
        alt.Chart(defense_long_all)
        .transform_filter(alt.FieldOneOfPredicate(field='Team', oneOf=team))                                  # team filter from Step 3
        .transform_filter(alt.datum.Season == season)     # season radio from Step 4
        .transform_filter(alt.datum.Venue == venue)
        .encode(
            y=alt.Y("Team:N", sort="-x", title=None),
            x=alt.X("Value:Q", title="Defense events"),
            yOffset=alt.YOffset("Metric:N"),
            tooltip=[
                alt.Tooltip("Team:N"),
                alt.Tooltip("MetricLabel:N", title="Metric"),
                alt.Tooltip("Value:Q"),
            ],
        )
    )
    stems = base.mark_rule(color="white")
    dots  = base.mark_point(size=90).encode(
        color=alt.Color("MetricLabel:N", title=None, scale=alt.Scale(scheme="set1"))
    )
    defense = alt.layer(stems, dots).properties(title=title)
    return defense

from utils.io import (overall, paired_long, offense_long_all, defense_long_all)
sel = alt.selection_point(fields=["Team"], toggle=True, empty="none")

bars = (
    alt.Chart(overall)
    .mark_bar()
    .encode(
        x=alt.X("Team:N", sort=alt.SortField("WinsDiff_2425_minus_2324", order="descending"),
                axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("WinsDiff_2425_minus_2324vals:Q", title="Wins (24-25 minus 23-24)"),
        color=alt.Color("Team:N", legend=None),
        opacity=alt.condition(sel, alt.value(1.0), alt.value(0.25)),
        tooltip=[
            alt.Tooltip("Team:N"),
            alt.Tooltip("Wins_2425:Q", title="Wins 2425"),
            alt.Tooltip("Wins_2324:Q", title="Wins 2324"),
            alt.Tooltip("WinsDiff_2425_minus_2324title:Q", title="\u0394 Wins"),
        ],
    )
    .add_params(sel)
    .properties(width=340, height=380, title="Change in Wins (23-24 to 24-25)")
)
base_right = (
    alt.Chart(paired_long)
    .transform_filter(sel)
    .encode(
        x=alt.X("season:N", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("value:Q", title=None),
        color=alt.Color("Team:N", legend=alt.Legend(title=None, orient="bottom-left")),
        detail="Team:N",
    )
)

paired_lines  = base_right.mark_line()
paired_points = base_right.mark_point(size=120)
paired_labels = (
    base_right
    .transform_filter(alt.datum.season == "2425")
    .mark_text(align="left", dx=8, dy=0)
    .encode(text="Team:N")
)
def trend_panel(metric_name, y_title, panel_title):
    return (
        alt.layer(paired_lines, paired_points, paired_labels)
        .transform_filter(alt.datum.metric == metric_name)
        .encode(y=alt.Y("value:Q", title=y_title))
        .properties(width=300, height=115, title=panel_title)
    )

middle_side2 = alt.vconcat(
    trend_panel("Wins",     "Wins",      "Wins (23-24 to 24-25)"),
    trend_panel("Draws",    "Draws",     "Draws (23-24 to 24-25)"),
    trend_panel("RedCards", "Red Cards", "Red Cards (23-24 to 24-25)"),
).resolve_scale(y="independent")

season_radio = alt.binding_radio(
    options=["2324", "2425"],
    labels=["23-24 Season", "24-25 Season"],
    name="Select Season:  "
)
season_select = alt.param(name="chosen_season", bind=season_radio, value="2324")

offense_home = alt.Chart(offense_long_all).transform_filter(sel).transform_filter(f"datum.Season == chosen_season").transform_filter(alt.datum.Venue == "Home").mark_bar().encode(
    x=alt.X(
        "Team:N",
        sort=alt.SortField("ShotsAttempted:Q", order="descending"),
        axis=alt.Axis(labelAngle=-45),
        title=None,
    ),
    y=alt.Y("sum(Count):Q", title="Shots"),
    color=alt.Color("ComponentLabel:N", title=None, scale=alt.Scale(scheme="set2")),
    order=alt.Order("Component:O"),
    tooltip=[
        alt.Tooltip("Team:N"),
        alt.Tooltip("sum(Count):Q", title="Total shots"),
    ],
    ).properties(width=150, height=100,title="Home Offense")

offense_away = alt.Chart(offense_long_all).transform_filter(sel).transform_filter(f"datum.Season == chosen_season").transform_filter(alt.datum.Venue == "Away").mark_bar().encode(
    x=alt.X(
        "Team:N",
        sort=alt.SortField("ShotsAttempted:Q", order="descending"),
        axis=alt.Axis(labelAngle=-45),
        title=None,
    ),
    y=alt.Y("sum(Count):Q", title="Shots"),
    color=alt.Color("ComponentLabel:N", title=None, scale=alt.Scale(scheme="set2")),
    order=alt.Order("Component:O"),
    tooltip=[
        alt.Tooltip("Team:N"),
        alt.Tooltip("sum(Count):Q", title="Total shots"),
    ],
    ).properties(width=150, height=100,title="Away Offense")

base_home = (
    alt.Chart(defense_long_all)
        .transform_filter(sel)                                 
        .transform_filter(f"datum.Season == chosen_season")    
        .transform_filter(alt.datum.Venue == "Home")
        .encode(
            y=alt.Y("Team:N", sort="-x", title=None),
            x=alt.X("Value:Q", title="Defense events"),
            yOffset=alt.YOffset("Metric:N"),
            tooltip=[
                alt.Tooltip("Team:N"),
                alt.Tooltip("MetricLabel:N", title="Metric"),
                alt.Tooltip("Value:Q"),
            ],
        )
    )
stems_home = base_home.mark_rule()
dots_home  = base_home.mark_point(size=90).encode(
    color=alt.Color("MetricLabel:N", title=None, scale=alt.Scale(scheme="set1"))
)
defense_home = alt.layer(stems_home, dots_home).properties(width=150, height=100,title="Home Defense")

base_away = (
    alt.Chart(defense_long_all)
        .transform_filter(sel)                                 
        .transform_filter(f"datum.Season == chosen_season")    
        .transform_filter(alt.datum.Venue == "Away")
        .encode(
            y=alt.Y("Team:N", sort="-x", title=None),
            x=alt.X("Value:Q", title="Defense events"),
            yOffset=alt.YOffset("Metric:N"),
            tooltip=[
                alt.Tooltip("Team:N"),
                alt.Tooltip("MetricLabel:N", title="Metric"),
                alt.Tooltip("Value:Q"),
            ],
        )
    )
stems_away = base_home.mark_rule()
dots_away  = base_home.mark_point(size=90).encode(
    color=alt.Color("MetricLabel:N", title=None, scale=alt.Scale(scheme="set1"))
)
defense_away = alt.layer(stems_away, dots_away).properties(width=150, height=100,title="Away Defense")

right_panel = alt.vconcat(
    alt.hconcat(offense_home, defense_home, spacing=12),
    alt.hconcat(offense_away, defense_away, spacing=12),
    spacing=16,
).add_params(season_select).properties(
    title="Home & Away — Offense & Defense (filtered by selected teams & season)"
)

final_dashboard = (alt.hconcat(bars, middle_side2,right_panel, spacing=12)
    .resolve_scale(color="independent")
    .properties(title="Premier League Dashboard — Select teams to explore")
)

