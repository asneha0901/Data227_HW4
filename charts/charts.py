
import altair as alt
import pandas as pd

#MAKING THE STATIC STORIES

def overall_bar(df: pd.DataFrame) -> alt.Chart:
    sel = alt.selection_point(fields=["Team"], toggle=True, empty="none")
    return(alt.Chart(df)
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
    .properties(width=340, height=380, title="Change in Wins (23-24 to 24-25)"))


