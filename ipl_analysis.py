import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(page_title="IPL Analysis Dashboard", layout="wide")
st.title("🏏 IPL Management Analysis Dashboard")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('matches.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Sidebar information
st.sidebar.header("Dataset Overview")
st.sidebar.write(f"**Total Matches:** {len(df)}")
st.sidebar.write(f"**Seasons:** {df['season'].min()} - {df['season'].max()}")
st.sidebar.write(f"**Total Teams:** {len(set(list(df['team1'].unique()) + list(df['team2'].unique())))}")

# Create tabs for different analyses
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Stats 1-2", "Stats 3-4", "Stats 5-6", "Stats 7-8", "Stats 9-10"])

# ============ STAT 1: Matches per Season (Line Chart) ============
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1️⃣ Matches Per Season")
        matches_per_season = df.groupby('season').size()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(matches_per_season.index, matches_per_season.values, marker='o', linewidth=2, markersize=8, color='#1f77b4')
        ax.fill_between(matches_per_season.index, matches_per_season.values, alpha=0.3, color='#1f77b4')
        ax.set_xlabel('Season', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Matches', fontsize=12, fontweight='bold')
        ax.set_title('IPL Matches Per Season Trend', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        st.write(f"**Stat:** Total matches across seasons range from {matches_per_season.min()} to {matches_per_season.max()}")

    # ============ STAT 2: Team Wins Overall (Bar Chart) ============
    with col2:
        st.subheader("2️⃣ Total Wins by Each Team")
        team_wins = df['winner'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(range(len(team_wins)), team_wins.values, color='#2ca02c')
        ax.set_yticks(range(len(team_wins)))
        ax.set_yticklabels(team_wins.index)
        ax.set_xlabel('Number of Wins', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Teams by Total Wins', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, team_wins.values)):
            ax.text(value, i, f' {int(value)}', va='center', fontweight='bold')
        
        st.pyplot(fig)
        
        st.write(f"**Stat:** {team_wins.index[0]} leads with {team_wins.values[0]} wins")

# ============ STAT 3: Toss Decision Impact (Pie Chart) ============
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("3️⃣ Toss Decision Impact on Match Wins")
        
        # Calculate win rate by toss decision
        toss_wins = []
        for decision in df['toss_decision'].unique():
            if pd.notna(decision):
                subset = df[df['toss_decision'] == decision]
                win_count = len(subset)
                toss_wins.append({'decision': decision, 'count': win_count})
        
        toss_df = pd.DataFrame(toss_wins)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#ff7f0e', '#2ca02c']
        wedges, texts, autotexts = ax.pie(toss_df['count'], labels=toss_df['decision'], autopct='%1.1f%%',
                                            colors=colors, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
        ax.set_title('Match Distribution by Toss Decision', fontsize=14, fontweight='bold')
        st.pyplot(fig)
        
        st.write(f"**Stat:** Batting teams won {toss_df[toss_df['decision']=='bat']['count'].values[0] if 'bat' in toss_df['decision'].values else 0} matches vs Fielding teams won {toss_df[toss_df['decision']=='field']['count'].values[0] if 'field' in toss_df['decision'].values else 0} matches")

    # ============ STAT 4: Wins by Runs vs Wickets (Scatter Plot) ============
    with col2:
        st.subheader("4️⃣ Win Margins: Runs vs Wickets")
        
        # Prepare data for scatter plot
        runs_wins = df['win_by_runs'].fillna(0)
        wickets_wins = df['win_by_wickets'].fillna(0)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(runs_wins, wickets_wins, alpha=0.6, s=100, color='#d62728', edgecolors='black')
        ax.set_xlabel('Win by Runs', fontsize=12, fontweight='bold')
        ax.set_ylabel('Win by Wickets', fontsize=12, fontweight='bold')
        ax.set_title('Match Outcomes: Runs vs Wickets', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        max_runs = runs_wins.max()
        max_wickets = wickets_wins.max()
        st.write(f"**Stat:** Max win margin by runs: {int(max_runs)} | Max win margin by wickets: {int(max_wickets)}")

# ============ STAT 5: Top Venues (Bar Chart) ============
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("5️⃣ Top 10 Venues by Match Count")
        
        top_venues = df['venue'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(top_venues)), top_venues.values, color='#9467bd')
        ax.set_xticks(range(len(top_venues)))
        ax.set_xticklabels(top_venues.index, rotation=45, ha='right')
        ax.set_ylabel('Number of Matches', fontsize=12, fontweight='bold')
        ax.set_title('IPL Matches by Top Venues', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        st.pyplot(fig)
        
        st.write(f"**Stat:** {top_venues.index[0]} hosted the most matches with {top_venues.values[0]} games")

    # ============ STAT 6: Player of the Match Frequency (Bar Chart) ============
    with col2:
        st.subheader("6️⃣ Top Players of the Match")
        
        player_counts = df['player_of_match'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(range(len(player_counts)), player_counts.values, color='#bcbd22')
        ax.set_yticks(range(len(player_counts)))
        ax.set_yticklabels(player_counts.index)
        ax.set_xlabel('Player of the Match Awards', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Players of the Match', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, player_counts.values)):
            ax.text(value, i, f' {int(value)}', va='center', fontweight='bold')
        
        st.pyplot(fig)
        
        st.write(f"**Stat:** {player_counts.index[0]} earned {player_counts.values[0]} Player of the Match awards")

# ============ STAT 7: Season-wise Average Win Margin (Line Chart) ============
with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("7️⃣ Average Win Margin by Season")
        
        # Calculate average margin (considering both runs and wickets)
        df['total_margin'] = df['win_by_runs'].fillna(0) + df['win_by_wickets'].fillna(0)
        avg_margin_season = df.groupby('season')['total_margin'].mean()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(avg_margin_season.index, avg_margin_season.values, marker='s', linewidth=2.5, 
                markersize=8, color='#17becf', label='Average Margin')
        ax.fill_between(avg_margin_season.index, avg_margin_season.values, alpha=0.3, color='#17becf')
        ax.set_xlabel('Season', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Win Margin', fontsize=12, fontweight='bold')
        ax.set_title('Season-wise Average Win Margin Trend', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        st.write(f"**Stat:** Highest avg margin in season {int(avg_margin_season.idxmax())}: {avg_margin_season.max():.2f}")

    # ============ STAT 8: Toss Winner vs Match Winner (Stacked Bar) ============
    with col2:
        st.subheader("8️⃣ Toss Winner vs Match Winner Analysis")
        
        # Calculate correlation between toss winner and match winner
        toss_match_correlation = []
        for i, row in df.iterrows():
            if row['toss_winner'] == row['winner']:
                toss_match_correlation.append('Won')
            else:
                toss_match_correlation.append('Lost')
        
        df['toss_match_result'] = toss_match_correlation
        toss_correlation_counts = df['toss_match_result'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_stack = ['#2ca02c', '#d62728']
        wedges, texts, autotexts = ax.pie(toss_correlation_counts.values, 
                                            labels=toss_correlation_counts.index,
                                            autopct='%1.1f%%', colors=colors_stack,
                                            startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
        ax.set_title('Toss Winners Winning Matches', fontsize=14, fontweight='bold')
        st.pyplot(fig)
        
        win_pct = (toss_correlation_counts['Won'] / len(df)) * 100
        st.write(f"**Stat:** Toss winners won {win_pct:.1f}% of their matches ({toss_correlation_counts['Won']} out of {len(df)})")

# ============ STAT 9: City-wise Match Count (Horizontal Bar) ============
with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("9️⃣ Matches by City")
        
        city_counts = df['city'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(range(len(city_counts)), city_counts.values, color='#e377c2')
        ax.set_yticks(range(len(city_counts)))
        ax.set_yticklabels(city_counts.index)
        ax.set_xlabel('Number of Matches', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Cities by Match Count', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, city_counts.values)):
            ax.text(value, i, f' {int(value)}', va='center', fontweight='bold')
        
        st.pyplot(fig)
        
        st.write(f"**Stat:** {city_counts.index[0]} hosted the most IPL matches ({city_counts.values[0]} total)")

    # ============ STAT 10: Win Margin Distribution (Histogram) ============
    with col2:
        st.subheader("🔟 Win Margin Distribution")
        
        # Create distribution of win margins
        margins = df['total_margin'].fillna(0)
        margins = margins[margins > 0]  # Only positive margins
        
        fig, ax = plt.subplots(figsize=(10, 6))
        n, bins, patches = ax.hist(margins, bins=20, color='#7f7f7f', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Win Margin', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Match Win Margins', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        
        st.write(f"**Stat:** Avg win margin: {margins.mean():.2f} | Median: {margins.median():.2f} | Max: {margins.max():.0f}")

# Footer
st.markdown("---")
st.markdown("### 📊 Summary Statistics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Matches", len(df))
with col2:
    st.metric("Total Seasons", df['season'].nunique())
with col3:
    st.metric("Unique Venues", df['venue'].nunique())
with col4:
    st.metric("Unique Teams", len(set(list(df['team1'].unique()) + list(df['team2'].unique()))))

st.markdown("**Dashboard Created for IPL Management Analysis** | Data Source: matches.csv")
