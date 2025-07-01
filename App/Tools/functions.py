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
from mplsoccer import Pitch, Sbopen
from datetime import datetime


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
 
    return f"{datetime.strftime(pd.to_datetime(match['match_date'].values[0]),'%Y-%m-%d %H:%M')} - {_home} vs {_away} ({match['home_score'].values[0]} - {match['away_score'].values[0]})"

def plot_team_matches(team_matches, team, xcol='match_date', ycol='goal_avg'):
    """
    Plot a timeline of matches for a given team.
    """
    # Prepare data for plot
    _team_matches = team_matches.copy()
    _team_matches.sort_values(by='match_date', inplace=True)

    x = _team_matches[xcol]
    y = []
    marker_colors = []
    marker_images = []
    hover_texts = []
    logo_dir = os.path.join(os.path.dirname(__file__), '..', 'logos', 'France - Ligue 1')
    
    for idx, row in _team_matches.iterrows():
        if row['home_team'] == team:
            y_val = row[ycol]
            border_color = 'blue'
            opponent = row['away_team']
        else:
            y_val = row[ycol]
            border_color = 'red'
            opponent = row['home_team']
        y.append(y_val)
        marker_colors.append(border_color)

        # Try to load logo
        marker_images.append(get_logo(opponent))

        hover_texts.append(f"{row['match_date']}<br>{row['home_team']} {row['home_score']} - {row['away_score']} {row['away_team']}<br>Goal average : {row['goal_avg']}<br>Centrality : {row['centrality']}")

    if xcol != 'match_date':
        x = pd.to_numeric(_team_matches[xcol])
    y = pd.to_numeric(y)
    # Create scatter plot
    fig = go.Figure()
    for i, (xs, ys, color, logo, hover) in enumerate(zip(x, y, marker_colors, marker_images, hover_texts)):
        if (logo is not None) & (xcol=='match_date'):
            fig.add_layout_image(
                dict(
                    source=logo,
                    x=xs,
                    y=ys,
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
            x=[xs],
            y=[ys],
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
        xaxis_title=xcol,
        yaxis_title=ycol,
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40)
    )

    if xcol == 'match_date':
        fig.update_layout(
            xaxis=dict(type='category')
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
    
@st.cache_data(show_spinner="Getting centralities")
def get_centralities(team_matches, team):
    team_matches["centrality"] = np.nan
    team_matches.loc[team_matches["home_team"] == team,'centrality'] = team_matches.loc[team_matches["home_team"] == team,'match_id'].apply(lambda x : plot_pass_network(x, team_matches[team_matches["match_id"]==x]["home_team"].values[0])[1])
    team_matches.loc[team_matches["away_team"] == team,'centrality'] = team_matches.loc[team_matches["away_team"] == team,'match_id'].apply(lambda x : plot_pass_network(x, team_matches[team_matches["match_id"]==x]["away_team"].values[0])[1])
    return team_matches

@st.cache_data(show_spinner="Getting goal averages")
def get_goalavg(team_matches, team):
    team_matches["goal_avg"] = np.nan
    team_matches.loc[team_matches["home_team"] == team,'goal_avg'] = team_matches.loc[team_matches["home_team"] == team,'match_id'].apply(lambda x : team_matches[team_matches["match_id"]==x]['home_score'].values[0] - team_matches[team_matches["match_id"]==x]['away_score'].values[0])
    team_matches.loc[team_matches["away_team"] == team,'goal_avg'] = team_matches.loc[team_matches["away_team"] == team,'match_id'].apply(lambda x : team_matches[team_matches["match_id"]==x]['away_score'].values[0] - team_matches[team_matches["match_id"]==x]['home_score'].values[0])
    return team_matches

    
@st.cache_data()
def plot_pass_network(match_id, team):
    parser = Sbopen()
    df, related, freeze, tactics = parser.event(match_id)

    sub = df.loc[df["type_name"] == "Substitution"].loc[df["team_name"] == team].iloc[0]["index"]
    mask_team = (df.type_name == 'Pass') & (df.team_name == team) & (df.index < sub) & (df.outcome_name.isnull()) & (df.sub_type_name != "Throw-in")
    #taking necessary columns
    df_pass = df.loc[mask_team, ['x', 'y', 'end_x', 'end_y', "player_name", "pass_recipient_name"]]
    #adjusting that only the surname of a player is presented.
    df_pass["player_name"] = df_pass["player_name"].apply(lambda x: str(x).split()[-1])
    df_pass["pass_recipient_name"] = df_pass["pass_recipient_name"].apply(lambda x: str(x).split()[-1])

    scatter_df = pd.DataFrame()
    for i, name in enumerate(df_pass["player_name"].unique()):
        passx = df_pass.loc[df_pass["player_name"] == name]["x"].to_numpy()
        recx = df_pass.loc[df_pass["pass_recipient_name"] == name]["end_x"].to_numpy()
        passy = df_pass.loc[df_pass["player_name"] == name]["y"].to_numpy()
        recy = df_pass.loc[df_pass["pass_recipient_name"] == name]["end_y"].to_numpy()
        scatter_df.at[i, "player_name"] = name
        #make sure that x and y location for each circle representing the player is the average of passes and receptions
        scatter_df.at[i, "x"] = np.mean(np.concatenate([passx, recx]))
        scatter_df.at[i, "y"] = np.mean(np.concatenate([passy, recy]))
        #calculate number of passes
        scatter_df.at[i, "no"] = df_pass.loc[df_pass["player_name"] == name].count().iloc[0]

    #adjust the size of a circle so that the player who made more passes
    scatter_df['marker_size'] = (scatter_df['no'] / scatter_df['no'].max() * 1500)

    #counting passes between players
    df_pass["pair_key"] = df_pass.apply(lambda x: "_".join(sorted([x["player_name"], x["pass_recipient_name"]])), axis=1)
    lines_df = df_pass.groupby(["pair_key"]).x.count().reset_index()
    lines_df.rename({'x':'pass_count'}, axis='columns', inplace=True)
    #setting a treshold. You can try to investigate how it changes when you change it.
    lines_df = lines_df[lines_df['pass_count']>2]


    #plot once again pitch and vertices
    pitch = Pitch(pitch_type='statsbomb')
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                        endnote_height=0.04, title_space=0, endnote_space=0)
    fig.set_size_inches(18.5,10.5)
    pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='red', edgecolors='grey', linewidth=1, alpha=1, ax=ax["pitch"], zorder = 3)
    for i, row in scatter_df.iterrows():
        pitch.annotate(row.player_name, xy=(row.x, row.y), c='black', va='center', ha='center', weight = "bold", size=16, ax=ax["pitch"], zorder = 4)

    for i, row in lines_df.iterrows():
            player1 = row["pair_key"].split("_")[0]
            player2 = row['pair_key'].split("_")[1]
            #take the average location of players to plot a line between them
            player1_x = scatter_df.loc[scatter_df["player_name"] == player1]['x'].iloc[0]
            player1_y = scatter_df.loc[scatter_df["player_name"] == player1]['y'].iloc[0]
            player2_x = scatter_df.loc[scatter_df["player_name"] == player2]['x'].iloc[0]
            player2_y = scatter_df.loc[scatter_df["player_name"] == player2]['y'].iloc[0]
            num_passes = row["pass_count"]
            #adjust the line width so that the more passes, the wider the line
            line_width = (num_passes / lines_df['pass_count'].max() * 10)
            #plot lines on the pitch
            pitch.lines(player1_x, player1_y, player2_x, player2_y,
                            alpha=1, lw=line_width, zorder=2, color="red", ax = ax["pitch"])


    #calculate number of successful passes by player
    no_passes = df_pass.groupby(['player_name']).x.count().reset_index()
    no_passes.rename({'x':'pass_count'}, axis='columns', inplace=True)
    #find one who made most passes
    max_no = no_passes["pass_count"].max()
    #calculate the denominator - 10*the total sum of passes
    denominator = 10*no_passes["pass_count"].sum()
    #calculate the nominator
    nominator = (max_no - no_passes["pass_count"]).sum()
    #calculate the centralisation index
    centralisation_index = nominator/denominator

    return fig, centralisation_index