import streamlit as st
import pandas as pd
from vega_datasets import data
import numpy as np


y1o = pd.read_csv("/Users/snehaagarwal/Data227_HW4/data/2324.csv")
y2o = pd.read_csv("/Users/snehaagarwal/Data227_HW4/data/2425.csv")

@st.cache_data
def clean_up(df: pd.DataFrame) -> pd.DataFrame:
    y = df
    num_cols = ["FTHG","FTAG","HS","AS","HST","AST","HC","AC","HR","AR"]
    for c in num_cols:
        if c in y.columns:
            y[c] = pd.to_numeric(y[c], errors="coerce")
    return y

y1 = clean_up(y1o)
y2 = clean_up(y2o)

def home(df: pd.DataFrame, season: str) -> pd.DataFrame:
    y1_home = df
    y1_home["Team"] = y1_home["HomeTeam"]
    y1_home["CornersAgainst"] = y1_home["AC"]
    y1_home["BlockedShotsByTeam"] = y1_home["AST"] - y1_home["FTAG"]
    y1_home["ShotsAttempted"] = y1_home["HS"]
    y1_home["ShotsOnTarget"] = y1_home["HST"]
    y1_home["Goals"] = y1_home["FTHG"]
    ds_home = (
        y1_home.groupby("Team", as_index=False)[
            ["CornersAgainst","BlockedShotsByTeam","ShotsAttempted","ShotsOnTarget","Goals"]
        ].sum()
    )
    ds_home["Season"] = season
    ds_home["Venue"] = "Home"
    ds_home = ds_home[["Season","Venue","Team","CornersAgainst","BlockedShotsByTeam","ShotsAttempted","ShotsOnTarget","Goals"]]
    return ds_home

y1_home = home(y1, "2324")
y2_home = home(y2, "2425")

def away(df: pd.DataFrame, season: str) -> pd.DataFrame:
    y1_away = df
    y1_away["Team"] = y1_away["AwayTeam"]
    y1_away["CornersAgainst"] = y1_away["HC"]
    y1_away["BlockedShotsByTeam"] = y1_away["HST"] - y1_away["FTHG"]
    y1_away["ShotsAttempted"] = y1_away["AS"]
    y1_away["ShotsOnTarget"] = y1_away["AST"]
    y1_away["Goals"] = y1_away["FTAG"]
    ds_away = (
        y1_away.groupby("Team", as_index=False)[
            ["CornersAgainst","BlockedShotsByTeam","ShotsAttempted","ShotsOnTarget","Goals"]
        ].sum()
    )
    ds_away["Season"] = season
    ds_away["Venue"] = "Away"
    ds_away = ds_away[["Season","Venue","Team","CornersAgainst","BlockedShotsByTeam","ShotsAttempted","ShotsOnTarget","Goals"]]
    return ds_away

y1_away = away(y1, "2324")
y2_away = away(y2, "2425")

def overallfunc(df: pd.DataFrame, season: str) -> pd.DataFrame:
    y1_home_res = pd.DataFrame({
        "Team": df["HomeTeam"],
        "Wins": (df["FTR"] == "H").astype(int),
        "Draws": (df["FTR"] == "D").astype(int),
        "RedCards": df["HR"].fillna(0),
    })
    y1_away_res = pd.DataFrame({
        "Team": df["AwayTeam"],
        "Wins": (df["FTR"] == "A").astype(int),
        "Draws": (df["FTR"] == "D").astype(int),
        "RedCards": df["AR"].fillna(0),
    })

    overall = (
        pd.concat([y1_home_res, y1_away_res], ignore_index=True)
        .groupby("Team", as_index=False)[["Wins","Draws","RedCards"]].sum()
    )
    overall = overall.rename(columns={"Wins": f"Wins_{season}",
    "Draws": f"Draws_{season}",
    "RedCards": f"RedCards_{season}"})
    return overall

overall_y1 = overallfunc(y1, "2324")
overall_y2 = overallfunc(y2, "2425")
overall = overall_y2.merge(overall_y1, on="Team", how="outer")
overall["WinsDiff_2425_minus_2324title"] = overall["Wins_2425"] - overall["Wins_2324"]
overall["WinsDiff_2425_minus_2324vals"] = overall["WinsDiff_2425_minus_2324title"].replace(np.nan, 0.3).replace(0.0,0.1)

overall = overall.sort_values(["Wins_2425","WinsDiff_2425_minus_2324title"], ascending=False).reset_index(drop=True)

teams = sorted(overall["Team"].dropna().unique().tolist())

paired_long = pd.concat([
    overall[["Team", "Wins_2324"]].rename(columns={"Wins_2324": "value"}).assign(metric="Wins", season="2324"),
    overall[["Team", "Wins_2425"]].rename(columns={"Wins_2425": "value"}).assign(metric="Wins", season="2425"),
    overall[["Team", "Draws_2324"]].rename(columns={"Draws_2324": "value"}).assign(metric="Draws", season="2324"),
    overall[["Team", "Draws_2425"]].rename(columns={"Draws_2425": "value"}).assign(metric="Draws", season="2425"),
    overall[["Team", "RedCards_2324"]].rename(columns={"RedCards_2324": "value"}).assign(metric="RedCards", season="2324"),
    overall[["Team", "RedCards_2425"]].rename(columns={"RedCards_2425": "value"}).assign(metric="RedCards", season="2425"),
], ignore_index=True)
paired_long["season"] = pd.Categorical(paired_long["season"], categories=["2324", "2425"], ordered=True)

df_all = pd.concat([
    y1_home, y1_away,
    y2_home, y2_away
], ignore_index=True)

def offense_dataset(df):
    off = df.copy()
    off["Goals"]          = off["Goals"].clip(lower=0)
    off["ShotsOnTarget"]  = off[["ShotsOnTarget", "Goals"]].max(axis=1)
    off["ShotsAttempted"] = off[["ShotsAttempted", "ShotsOnTarget"]].max(axis=1)
    off["Goals_part"]         = off["Goals"]
    off["SOT_not_goal_part"]  = (off["ShotsOnTarget"] - off["Goals"]).clip(lower=0)
    off["Shot_not_SOT_part"]  = (off["ShotsAttempted"] - off["ShotsOnTarget"]).clip(lower=0)
    component_order  = ["Shot_not_SOT_part", "SOT_not_goal_part", "Goals_part"]
    component_labels = {
        "Shot_not_SOT_part":  "Shots (not on target)",
        "SOT_not_goal_part":  "Shots on target (not goals)",
        "Goals_part":         "Goals",
    }
    offense_long = off.melt(
        id_vars=["Team", "Venue", "Season", "ShotsAttempted"],
        value_vars=component_order,
        var_name="Component", value_name="Count",
    )
    offense_long["Component"]      = pd.Categorical(offense_long["Component"], component_order, ordered=True)
    offense_long["ComponentLabel"] = offense_long["Component"].map(component_labels)
    return offense_long

def defense_dataset(df):
    metric_order  = ["CornersAgainst", "BlockedShotsByTeam"]
    metric_labels = {
        "CornersAgainst":     "Corners against",
        "BlockedShotsByTeam": "Blocked shots by team",
    }
    defense_long = df.melt(
        id_vars=["Team", "Venue", "Season"],
        value_vars=metric_order,
        var_name="Metric", value_name="Value",
    )
    defense_long["Metric"]      = pd.Categorical(defense_long["Metric"], metric_order, ordered=True)
    defense_long["MetricLabel"] = defense_long["Metric"].map(metric_labels)
    return defense_long

offense_long_all = offense_dataset(df_all)
defense_long_all = defense_dataset(df_all)