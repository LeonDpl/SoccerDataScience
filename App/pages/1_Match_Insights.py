from statsbombpy import sb
from mplsoccer import Pitch
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns



import warnings
warnings.filterwarnings('ignore')

import streamlit as st


# Fix import error for Streamlit pages
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Tools.constants import PLAYERS, TACTICAL_POSITIONS
from Tools.functions import get_logo_team, get_matches, plot_team_matches, get_match_title, plot_events_heatmap, plot_events_pitch, show_lineup


st.set_page_config(page_title="Match insights", layout="wide")
st.title("Match insights")
#st.selectbox("Select a player", PLAYERS.keys())

competitions = ["<Select a competition>"]
competitions.extend(sb.competitions()["competition_name"].unique())
competition = st.selectbox("Select a competition", competitions)

seasons = st.multiselect("Select seasons", 
               sb.competitions()[sb.competitions()["competition_name"] == competition]["season_name"].unique(), 
               default=sb.competitions()[sb.competitions()["competition_name"] == competition]["season_name"].unique())

competitions_df = sb.competitions()[sb.competitions()["competition_name"]==competition]
competitions_df = competitions_df[competitions_df["season_name"].isin(seasons)]

if len(competitions_df) > 0:
    matches = get_matches(competitions_df)

    teams = ["<select a team>"]
    teams.extend(matches["home_team"].unique())

    team = st.selectbox("Select a team", teams)


    if team != "<select a team>":
        team_matches = matches[(matches["home_team"] == team) | (matches["away_team"] == team)]
        #st.dataframe(team_matches)
        click_team_matches = st.plotly_chart(plot_team_matches(team_matches, team), 
                                             use_container_width=True,
                                             on_select="rerun",
                                             selection_mode="points")
        
        if len(click_team_matches["selection"]["points"]) <= 0:
            st.html('<p style="text-align: center;">Select a match for more insights.</p>')
        else:
            match = team_matches[team_matches["match_date"] == click_team_matches["selection"]["points"][0]["x"]]
            st.html(get_match_title(match))

            
            l, r = st.columns(2)

            with l:
                st.html(f'<p style="text-align: center;">{get_logo_team(match["home_team"].values[0])} ({match["home_score"].values[0]})</p>')
                team_lineup = sb.lineups(match_id=match["match_id"].values[0])[match["home_team"].values[0]]
                show_lineup(team_lineup)
            
            with r:
                st.html(f'<p style="text-align: center;">{get_logo_team(match["away_team"].values[0])} ({match["away_score"].values[0]})</p>')
                team_lineup = sb.lineups(match_id=match["match_id"].values[0])[match["away_team"].values[0]]
                show_lineup(team_lineup)
            

            events = sb.events(match_id=match["match_id"].values[0])
            events = events[events['minute']>=0]

            eventsFilter = {
                "All" : events["type"].unique(),
                "Positive" : ["Pass", "Shot", "Ball Recovery", "Carry", "Dribble", "Duel", "Interception"],
                "Negative" : ["Foul Committed", "Foul Won", "Miscontrol", "Dispossessed", "Dribbled Past"],
                "None" : []
            }

            filter = st.segmented_control("Filter Events",
                                             options=eventsFilter.keys(),
                                             default="All")
            
            defaultEvTypes = eventsFilter[filter]
            
            evTypes = st.pills("Event Types",
                               options=eventsFilter["All"],
                               selection_mode="multi",
                               default=defaultEvTypes)
            
            if len(evTypes) > 0:
                events = events[events["type"].isin(evTypes)]

                st.plotly_chart(plot_events_heatmap(events), use_container_width=True)

            # TODO : plot event pitch
            # - Handle team position at game start and halftime change
            #st.pyplot(plot_events_pitch(events), use_container_width=True)

            
            
            