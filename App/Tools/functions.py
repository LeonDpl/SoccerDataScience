# functions.py
# This file contains helper functions for the Streamlit app.

import streamlit as st
from statsbombpy import sb
import pandas as pd

import plotly.graph_objects as go
import os
from PIL import Image
import base64

import numpy as np
from mplsoccer import Pitch


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Tools.constants import PLAYERS, TACTICAL_POSITIONS



@st.cache_data()
def get_matches(competition, season):
    """
    Fetch matches for a given competition and season.
    """
    return sb.matches(competition_id=competition, season_id=season)

@st.cache_data()
def get_matches(competitions):
    """
    Fetch matches for a given competition and season.
    """
    matches = pd.DataFrame()
    data = []
    for ix, row in competitions.iterrows():
        _matches = sb.matches(competition_id=row["competition_id"], season_id=row["season_id"])
        data.append(_matches)
    
    matches = pd.concat(data)
    
    matches['match_date'] = pd.to_datetime(matches['match_date'] + ' ' + matches['kick_off'] )

    return matches

def get_logo(team):
    """
    Get the logo for a given team.
    """
    logo_dir = os.path.join(os.path.dirname(__file__), '..', 'logos', 'France - Ligue 1')
    logo_path = os.path.join(logo_dir, f"{team}.png")
    
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded}"
    else:
        return None
    
def get_logo_team(team):
    logo = get_logo(team)
    if logo:
        logoteam = f"<img src='{logo}' style='height:30px;'> {team}"
    else:
        logoteam = team

    return logoteam


def get_match_title(match):
    """
    Generate a title for the match based on the team and match details.
    """
    _home = get_logo_team(match['home_team'].values[0])
    _away = get_logo_team(match['away_team'].values[0])
 
    return f"{match['match_date'].values[0]} - {_home} vs {_away} ({match['home_score'].values[0]} - {match['away_score'].values[0]})"

def plot_team_matches(team_matches, team):
    """
    Plot a timeline of matches for a given team.
    """
    # Prepare data for plot
    _team_matches = team_matches.copy()
    _team_matches.sort_values(by='match_date', inplace=True)

    x = _team_matches['match_date']
    y = []
    marker_colors = []
    marker_images = []
    hover_texts = []
    logo_dir = os.path.join(os.path.dirname(__file__), '..', 'logos', 'France - Ligue 1')

    for idx, row in _team_matches.iterrows():
        if row['home_team'] == team:
            y_val = row['home_score'] - row['away_score']
            border_color = 'blue'
            opponent = row['away_team']
        else:
            y_val = row['away_score'] - row['home_score']
            border_color = 'red'
            opponent = row['home_team']
        y.append(y_val)
        marker_colors.append(border_color)

        # Try to load logo
        marker_images.append(get_logo(opponent))

        hover_texts.append(f"{row['match_date']}<br>{row['home_team']} {row['home_score']} - {row['away_score']} {row['away_team']}")

    # Create scatter plot
    fig = go.Figure()
    for i, (date, score, color, logo, hover) in enumerate(zip(x, y, marker_colors, marker_images, hover_texts)):
        if logo:
            fig.add_layout_image(
                dict(
                    source=logo,
                    x=date,
                    y=score,
                    xref="x",
                    yref="y",
                    sizex=1.5,
                    sizey=1.5,
                    xanchor="center",
                    yanchor="middle",
                    layer="above"
                )
            )
        fig.add_trace(go.Scatter(
            x=[date],
            y=[score],
            mode="markers",
            marker=dict(
                size=20,
                color='white',
                line=dict(color=color, width=4),
                symbol='circle'
            ),
            hovertemplate=hover,
            showlegend=False
        ))

    fig.update_layout(
        title="Match Results (Goal Difference)",
        xaxis_title="Match Date",
        yaxis_title="Goal Difference",
        xaxis=dict(type='category'),
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig

def plot_events_heatmap(events):
    """
    Plot a heatmap of events for a given team.
    """

    events = events[['minute', 'player', 'team']]
    events['player_team'] = '(' + events['team'] + ') ' + events['player']
    events = events[['minute','player_team']]

    events['minute_bin'] = events['minute'].astype(int)

    # Create a pivot table: rows=player, columns=minute, values=count of appearances
    heatmap_data = events.groupby(['player_team', 'minute_bin']).size().unstack(fill_value=0)
    heatmap_data['tot'] = heatmap_data.sum(axis=1)
    heatmap_data.sort_values(by='tot', ascending=True, inplace=True)
    heatmap_data = heatmap_data[[c for c in heatmap_data.columns if c != 'tot']]

    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale="Greys",
            colorbar=dict(title="Count"),
            zmin=0
        )
    )

    fig.update_layout(
        width=1200,
        height=30 * len(heatmap_data.index),  # dynamic height
        xaxis_title="Minute",
        yaxis_title="Player",
        title="Player Event Frequency by Minute",
        margin=dict(l=120, r=20, t=50, b=50)
    )

    return fig

def plot_events_pitch(events, pitch_length=120, pitch_width=80, bins_x=30, bins_y=20):
    """
    Plot a density heatmap of event locations using Plotly, with a soccer pitch as background.
    Args:
        events: DataFrame with a 'location' column (list of [x, y])
        pitch_length: Length of the pitch (default 120)
        pitch_width: Width of the pitch (default 80)
        bins_x: Number of bins along x
        bins_y: Number of bins along y
    Returns:
        Plotly Figure
    """
    # Extract x and y coordinates from the 'location' column
    locations = events['location'].dropna().tolist()
    x = [loc[0] for loc in locations if isinstance(loc, list) and len(loc) == 2]
    y = [loc[1] for loc in locations if isinstance(loc, list) and len(loc) == 2]

    pitch = Pitch(pitch_type='statsbomb')
    fig, ax = pitch.draw()
    stats = pitch.bin_statistic(x, y, bins=(120,80))
    pitch.heatmap(stats, ax=ax, alpha=0.5, cmap='afmhot')

    return fig

def show_lineup(match_lineup):
    team_lineup = match_lineup.copy()#sb.lineups(match_id=match["match_id"].values[0])[match["home_team"].values[0]]
    team_lineup["Player"] = team_lineup.apply(lambda x: x["player_nickname"] if x["player_nickname"] is not None else x["player_name"], axis=1)
    team_lineup["Jersey"] = team_lineup["jersey_number"]
    team_lineup["Position"] = team_lineup["positions"].apply(lambda x: [TACTICAL_POSITIONS[i["position_id"]]["tag"] for i in x])

    st.dataframe(team_lineup[["Player","Jersey", "Position"]],
                column_config={
                        "Player": st.column_config.TextColumn("Player"),
                        "Jersey": st.column_config.TextColumn("Jersey"),
                        "Position": st.column_config.ListColumn("Positions", width="medium")
                },
                hide_index=True,
                use_container_width=True)