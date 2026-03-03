
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