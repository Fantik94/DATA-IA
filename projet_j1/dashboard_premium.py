#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DASHBOARD PREMIUM SPOTIFY 2023
===============================
Dashboard avec charte graphique cohérente et fonctionnalités avancées

Auteur : Expert Data Scientist
Date : 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="🎵 Spotify Premium Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Charte graphique Spotify cohérente
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_BLACK = "#191414"
SPOTIFY_DARK = "#121212"
SPOTIFY_GRAY = "#535353"
SPOTIFY_LIGHT_GRAY = "#B3B3B3"
SPOTIFY_WHITE = "#FFFFFF"

# CSS avec charte graphique unifiée
st.markdown(f"""
<style>
    /* Variables CSS */
    :root {{
        --spotify-green: {SPOTIFY_GREEN};
        --spotify-black: {SPOTIFY_BLACK};
        --spotify-dark: {SPOTIFY_DARK};
        --spotify-gray: {SPOTIFY_GRAY};
        --spotify-light-gray: {SPOTIFY_LIGHT_GRAY};
        --spotify-white: {SPOTIFY_WHITE};
    }}
    
    /* Header principal */
    .main-header {{
        background: linear-gradient(135deg, var(--spotify-green), var(--spotify-black));
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: var(--spotify-white);
        text-align: center;
        box-shadow: 0 10px 40px rgba(29, 185, 84, 0.3);
        position: relative;
        overflow: hidden;
    }}
    
    .main-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        z-index: 1;
    }}
    
    .main-header h1, .main-header p {{
        position: relative;
        z-index: 2;
    }}
    
    /* Cards et métriques */
    .metric-card {{
        background: linear-gradient(135deg, var(--spotify-white), #f8f9fa);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid transparent;
        background-clip: padding-box;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 15px;
        padding: 2px;
        background: linear-gradient(135deg, var(--spotify-green), var(--spotify-black));
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask-composite: subtract;
        z-index: -1;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(29, 185, 84, 0.2);
    }}
    
    /* Top cards spéciales */
    .top-card {{
        background: linear-gradient(135deg, var(--spotify-green), #1ed760);
        color: var(--spotify-white);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(29, 185, 84, 0.3);
        border: none;
    }}
    
    .top-card h3, .top-card h4 {{
        color: var(--spotify-white) !important;
        margin: 0.5rem 0;
    }}
    
    /* Sidebar styling */
    .sidebar .sidebar-content {{
        background: linear-gradient(180deg, var(--spotify-dark), var(--spotify-black));
        color: var(--spotify-white);
    }}
    
    /* Filtres et contrôles */
    .stSelectbox > div > div {{
        background: var(--spotify-white);
        border: 2px solid var(--spotify-green);
        border-radius: 10px;
        color: var(--spotify-black);
    }}
    
    .stSlider > div > div > div > div {{
        background: var(--spotify-green);
    }}
    
    .stMultiSelect > div > div {{
        background: var(--spotify-white);
        border: 2px solid var(--spotify-green);
        border-radius: 10px;
    }}
    
    /* Boutons */
    .stButton > button {{
        background: linear-gradient(135deg, var(--spotify-green), #1ed760);
        color: var(--spotify-white);
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(29, 185, 84, 0.4);
        background: linear-gradient(135deg, #1ed760, var(--spotify-green));
    }}
    
    /* Section headers */
    .section-header {{
        background: linear-gradient(90deg, var(--spotify-green), var(--spotify-black));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        text-align: center;
    }}
    
    /* Insights box */
    .insight-box {{
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.1), rgba(29, 185, 84, 0.2));
        border: 2px solid var(--spotify-green);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: var(--spotify-black);
    }}
    
    /* Custom tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: linear-gradient(135deg, var(--spotify-white), #f8f9fa);
        border: 2px solid var(--spotify-green);
        border-radius: 10px 10px 0 0;
        color: var(--spotify-black);
        font-weight: bold;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, var(--spotify-green), #1ed760);
        color: var(--spotify-white);
    }}
    
    /* Dataframes */
    .stDataFrame {{
        border: 2px solid var(--spotify-green);
        border-radius: 10px;
        overflow: hidden;
    }}
    
    /* Progress bars et métriques */
    .stProgress > div > div > div > div {{
        background: var(--spotify-green);
    }}
    
    .metric-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background: var(--spotify-white);
        border-radius: 10px;
        border: 2px solid var(--spotify-green);
        margin: 0.5rem 0;
    }}
    
    /* Animations */
    @keyframes spotifyPulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(29, 185, 84, 0.7); }}
        70% {{ box-shadow: 0 0 0 10px rgba(29, 185, 84, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(29, 185, 84, 0); }}
    }}
    
    .pulse-animation {{
        animation: spotifyPulse 2s infinite;
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Chargement et nettoyage des données"""
    import os
    
    # Chercher le fichier CSV dans différents répertoires possibles
    possible_paths = [
        'spotify-2023.csv',
        'projet_j1/spotify-2023.csv',
        '../spotify-2023.csv',
        os.path.join(os.path.dirname(__file__), '..', 'spotify-2023.csv'),
        os.path.join(os.path.dirname(__file__), 'spotify-2023.csv')
    ]
    
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if csv_path is None:
        st.error("❌ Fichier spotify-2023.csv non trouvé.")
        st.info("💡 Vous pouvez:")
        st.markdown("- Télécharger le fichier depuis le [dépôt GitHub](https://github.com/bapti/DATA-IA)")
        st.markdown("- Ou utiliser le bouton ci-dessous pour charger votre propre fichier CSV")
        
        uploaded_file = st.file_uploader("📁 Charger votre fichier CSV Spotify", type=['csv'])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding='latin-1')
        else:
            st.warning("⚠️ En attente du fichier de données...")
            st.stop()
    else:
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(csv_path, encoding='latin-1')
    
    # Nettoyage
    df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
    
    numeric_cols = ['in_spotify_playlists', 'in_spotify_charts', 'in_apple_playlists', 
                   'in_apple_charts', 'in_deezer_playlists', 'in_deezer_charts', 
                   'in_shazam_charts']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').replace('', '0')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Variables dérivées
    df['total_playlists'] = (df['in_spotify_playlists'] + df['in_apple_playlists'] + 
                            df['in_deezer_playlists'])
    df['total_charts'] = (df['in_spotify_charts'] + df['in_apple_charts'] + 
                         df['in_deezer_charts'] + df['in_shazam_charts'])
    
    # Date de sortie
    try:
        df['release_date'] = pd.to_datetime(
            df['released_year'].astype(str) + '-' + 
            df['released_month'].astype(str) + '-' + 
            df['released_day'].astype(str),
            errors='coerce'
        )
    except:
        df['release_date'] = pd.NaT
    
    # Catégorisation avec émojis
    df['success_category'] = pd.cut(df['streams'], 
                                  bins=[0, 100_000_000, 500_000_000, 1_000_000_000, float('inf')],
                                  labels=['🌱 Émergent', '⭐ Populaire', '🔥 Hit', '💎 Mega-Hit'])
    
    df = df.dropna(subset=['streams'])
    return df

def create_spotify_color_palette():
    """Palette de couleurs cohérente Spotify"""
    return [
        SPOTIFY_GREEN,
        "#1ed760",
        "#1aa34a",
        "#0e7e32",
        SPOTIFY_BLACK,
        SPOTIFY_GRAY,
        SPOTIFY_LIGHT_GRAY
    ]

def create_sidebar_filters(df):
    """Sidebar avec design Spotify cohérent"""
    st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #1DB954, #191414); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;'>
        <h2 style='color: white; margin: 0;'>🎛️ CONTRÔLES</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Section principale d'analyse
    st.sidebar.markdown("### 🎯 **TYPE D'ANALYSE**")
    analysis_mode = st.sidebar.radio(
        "",
        ["📊 Vue d'ensemble", "🏆 Top Performers", "🎼 Analyse Musicale", "📅 Tendances", "⚔️ Comparaisons"],
        key="analysis_mode"
    )
    
    st.sidebar.markdown("---")
    
    # Filtres temporels
    st.sidebar.markdown("### 📅 **PÉRIODE**")
    years = sorted(df['released_year'].unique())
    year_range = st.sidebar.select_slider(
        "Années d'analyse",
        options=years,
        value=(max(years)-2, max(years)),
        format_func=lambda x: f"📅 {x}"
    )
    
    # Filtres de succès
    st.sidebar.markdown("### 🎯 **NIVEAUX DE SUCCÈS**")
    categories = df['success_category'].cat.categories.tolist()
    selected_categories = st.sidebar.multiselect(
        "",
        categories,
        default=categories
    )
    
    # Filtres avancés dans un expander
    with st.sidebar.expander("🔧 **FILTRES AVANCÉS**"):
        # Plage de streams
        min_streams = int(df['streams'].min() // 1_000_000)
        max_streams = int(df['streams'].max() // 1_000_000)
        streams_range = st.slider(
            "Streams (millions)",
            min_streams, max_streams,
            (min_streams, max_streams),
            format="%d M"
        )
        
        # Nombre d'artistes
        artist_range = st.slider(
            "Nombre d'artistes",
            1, int(df['artist_count'].max()),
            (1, int(df['artist_count'].max()))
        )
        
        # Caractéristiques musicales
        st.markdown("**🎵 Caractéristiques Musicales**")
        danceability_range = st.slider("💃 Danceability", 0, 100, (0, 100))
        energy_range = st.slider("⚡ Energy", 0, 100, (0, 100))
        valence_range = st.slider("😊 Valence", 0, 100, (0, 100))
    
    # Paramètres d'affichage
    with st.sidebar.expander("🎨 **AFFICHAGE**"):
        top_n = st.slider("Nombre d'éléments dans les tops", 5, 20, 10)
        show_percentages = st.checkbox("Afficher les pourcentages", True)
        animate_charts = st.checkbox("Animations", True)
    
    return {
        'analysis_mode': analysis_mode,
        'year_range': year_range,
        'categories': selected_categories,
        'streams_range': (streams_range[0] * 1_000_000, streams_range[1] * 1_000_000),
        'artist_range': artist_range,
        'danceability_range': danceability_range,
        'energy_range': energy_range,
        'valence_range': valence_range,
        'top_n': top_n,
        'show_percentages': show_percentages,
        'animate_charts': animate_charts
    }

def apply_filters(df, filters):
    """Application des filtres"""
    filtered_df = df.copy()
    
    # Filtres temporels
    filtered_df = filtered_df[
        (filtered_df['released_year'] >= filters['year_range'][0]) &
        (filtered_df['released_year'] <= filters['year_range'][1])
    ]
    
    # Filtres de succès
    if filters['categories']:
        filtered_df = filtered_df[filtered_df['success_category'].isin(filters['categories'])]
    
    # Filtres numériques
    filtered_df = filtered_df[
        (filtered_df['streams'] >= filters['streams_range'][0]) &
        (filtered_df['streams'] <= filters['streams_range'][1]) &
        (filtered_df['artist_count'] >= filters['artist_range'][0]) &
        (filtered_df['artist_count'] <= filters['artist_range'][1]) &
        (filtered_df['danceability_%'] >= filters['danceability_range'][0]) &
        (filtered_df['danceability_%'] <= filters['danceability_range'][1]) &
        (filtered_df['energy_%'] >= filters['energy_range'][0]) &
        (filtered_df['energy_%'] <= filters['energy_range'][1]) &
        (filtered_df['valence_%'] >= filters['valence_range'][0]) &
        (filtered_df['valence_%'] <= filters['valence_range'][1])
    ]
    
    return filtered_df

def create_kpis_dashboard(df):
    """KPIs avec design Spotify unifié"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    kpis = [
        ("🎵", "Titres", f"{len(df):,}", "Nombre total de titres"),
        ("📊", "Streams", f"{df['streams'].sum()/1e9:.1f}B", "Streams cumulés"),
        ("📈", "Moyenne", f"{df['streams'].mean()/1e6:.0f}M", "Streams par titre"),
        ("🎤", "Artistes", f"{df['artist(s)_name'].nunique():,}", "Artistes uniques"),
        ("🏆", "Hits", f"{len(df[df['success_category'].isin(['🔥 Hit', '💎 Mega-Hit'])])} ({len(df[df['success_category'].isin(['🔥 Hit', '💎 Mega-Hit'])])/len(df)*100:.1f}%)", "Hits et Mega-hits")
    ]
    
    for i, (icon, label, value, description) in enumerate(kpis):
        with [col1, col2, col3, col4, col5][i]:
            st.markdown(f"""
            <div class="metric-card pulse-animation">
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div style="font-size: 1.2rem; font-weight: bold; color: {SPOTIFY_GREEN};">{label}</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: {SPOTIFY_BLACK};">{value}</div>
                    <div style="font-size: 0.8rem; color: {SPOTIFY_GRAY};">{description}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def create_top_performers(df, filters):
    """Section Top Performers avec design cohérent"""
    st.markdown('<h2 class="section-header">🏆 TOP PERFORMERS</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top Artistes
        st.markdown("""
        <div class="top-card">
            <h3>🎤 TOP ARTISTES PAR STREAMS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        top_artists = df.groupby('artist(s)_name')['streams'].sum().sort_values(ascending=False).head(filters['top_n'])
        
        fig_artists = go.Figure(data=[
            go.Bar(
                y=top_artists.index[::-1],
                x=top_artists.values[::-1],
                orientation='h',
                marker=dict(
                    color=create_spotify_color_palette()[:len(top_artists)],
                    line=dict(color=SPOTIFY_WHITE, width=2)
                ),
                text=[f"{v/1e9:.1f}B" for v in top_artists.values[::-1]],
                textposition='outside',
                hovertemplate="<b>%{y}</b><br>Streams: %{x:,.0f}<extra></extra>"
            )
        ])
        
        fig_artists.update_layout(
            title="",
            xaxis_title="Streams Totaux",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=SPOTIFY_BLACK),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_artists, use_container_width=True)
    
    with col2:
        # Top Titres
        st.markdown("""
        <div class="top-card">
            <h3>🎵 TOP TITRES PAR STREAMS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        top_songs = df.nlargest(filters['top_n'], 'streams')[['track_name', 'artist(s)_name', 'streams', 'success_category']]
        
        for i, (_, song) in enumerate(top_songs.iterrows()):
            rank_color = SPOTIFY_GREEN if i < 3 else SPOTIFY_GRAY
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {SPOTIFY_WHITE}, #f8f9fa);
                border: 2px solid {rank_color};
                border-radius: 10px;
                padding: 1rem;
                margin: 0.5rem 0;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 1.2rem; font-weight: bold; color: {SPOTIFY_BLACK};">
                            #{i+1} {song['track_name'][:30]}{'...' if len(song['track_name']) > 30 else ''}
                        </div>
                        <div style="color: {SPOTIFY_GRAY}; font-size: 0.9rem;">
                            {song['artist(s)_name'][:40]}{'...' if len(song['artist(s)_name']) > 40 else ''}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: bold; color: {SPOTIFY_GREEN};">
                            {song['streams']/1e9:.1f}B
                        </div>
                        <div style="font-size: 0.8rem;">
                            {song['success_category']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def create_donut_charts_spotify(df, filters):
    """Graphiques en donut avec palette Spotify"""
    st.markdown('<h2 class="section-header">🍩 RÉPARTITIONS</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Donut succès
        success_counts = df['success_category'].value_counts()
        colors_success = [SPOTIFY_GREEN, "#1ed760", "#1aa34a", "#0e7e32"]
        
        fig1 = go.Figure(data=[go.Pie(
            labels=success_counts.index,
            values=success_counts.values,
            hole=0.6,
            marker=dict(colors=colors_success, line=dict(color=SPOTIFY_WHITE, width=3)),
            textinfo='label+percent',
            textfont=dict(size=12, color=SPOTIFY_BLACK),
            hovertemplate="<b>%{label}</b><br>Nombre: %{value}<br>Pourcentage: %{percent}<extra></extra>"
        )])
        
        fig1.update_layout(
            title=dict(text="🎯 Niveaux de Succès", x=0.5, font=dict(size=16, color=SPOTIFY_BLACK)),
            showlegend=True,
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig1.add_annotation(
            text=f"<b>{len(df)}</b><br>Titres",
            x=0.5, y=0.5,
            font=dict(size=16, color=SPOTIFY_BLACK),
            showarrow=False
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Donut collaborations
        collab_counts = df['artist_count'].value_counts().sort_index()
        
        fig2 = go.Figure(data=[go.Pie(
            labels=[f"{i} Artiste{'s' if i > 1 else ''}" for i in collab_counts.index],
            values=collab_counts.values,
            hole=0.6,
            marker=dict(colors=create_spotify_color_palette(), line=dict(color=SPOTIFY_WHITE, width=3)),
            textinfo='label+percent',
            textfont=dict(size=12, color=SPOTIFY_BLACK)
        )])
        
        fig2.update_layout(
            title=dict(text="👥 Collaborations", x=0.5, font=dict(size=16, color=SPOTIFY_BLACK)),
            showlegend=True,
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with col3:
        # Donut années
        year_counts = df['released_year'].value_counts().sort_index()
        
        fig3 = go.Figure(data=[go.Pie(
            labels=year_counts.index,
            values=year_counts.values,
            hole=0.6,
            marker=dict(colors=create_spotify_color_palette(), line=dict(color=SPOTIFY_WHITE, width=3)),
            textinfo='label+percent',
            textfont=dict(size=12, color=SPOTIFY_BLACK)
        )])
        
        fig3.update_layout(
            title=dict(text="📅 Répartition Annuelle", x=0.5, font=dict(size=16, color=SPOTIFY_BLACK)),
            showlegend=True,
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig3, use_container_width=True)

def create_musical_analysis(df, filters):
    """Analyse musicale avec design cohérent"""
    st.markdown('<h2 class="section-header">🎼 ANALYSE MUSICALE</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart des caractéristiques
        musical_features = ['danceability_%', 'energy_%', 'valence_%', 'acousticness_%']
        
        # Profil moyen par catégorie
        categories = ['🔥 Hit', '💎 Mega-Hit', '⭐ Populaire', '🌱 Émergent']
        colors = [SPOTIFY_GREEN, "#1ed760", "#1aa34a", "#0e7e32"]
        
        fig_radar = go.Figure()
        
        for i, category in enumerate(categories):
            if category in df['success_category'].values:
                category_data = df[df['success_category'] == category]
                if len(category_data) > 0:
                    values = category_data[musical_features].mean().values
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=values,
                        theta=[f.replace('_%', '').title() for f in musical_features],
                        fill='toself',
                        name=category,
                        line=dict(color=colors[i], width=3),
                        fillcolor=f"rgba{tuple(list(map(int, [colors[i][1:][j:j+2] for j in (0, 2, 4)])) + [0.2])}"
                    ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color=SPOTIFY_GRAY),
                angularaxis=dict(color=SPOTIFY_BLACK)
            ),
            showlegend=True,
            title=dict(text="🎯 Profils Musicaux par Succès", x=0.5, font=dict(size=16, color=SPOTIFY_BLACK)),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Top genres par BPM
        st.markdown("### 🥁 **ANALYSE BPM**")
        
        # Bins BPM
        df['bpm_range'] = pd.cut(df['bpm'], bins=[0, 90, 120, 140, 180, 300], 
                                labels=['Lent', 'Modéré', 'Rapide', 'Très Rapide', 'Extrême'])
        
        bpm_success = df.groupby(['bpm_range', 'success_category']).size().unstack(fill_value=0)
        
        fig_bpm = go.Figure()
        
        for i, category in enumerate(bpm_success.columns):
            fig_bpm.add_trace(go.Bar(
                name=category,
                x=bpm_success.index,
                y=bpm_success[category],
                marker_color=create_spotify_color_palette()[i],
                text=bpm_success[category],
                textposition='auto'
            ))
        
        fig_bpm.update_layout(
            title="Distribution BPM par Succès",
            xaxis_title="Plage BPM",
            yaxis_title="Nombre de titres",
            barmode='stack',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=SPOTIFY_BLACK)
        )
        
        st.plotly_chart(fig_bpm, use_container_width=True)

def create_temporal_trends(df, filters):
    """Tendances temporelles avec design Spotify"""
    st.markdown('<h2 class="section-header">📅 TENDANCES TEMPORELLES</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Évolution par mois
        st.markdown("""
        <div class="top-card">
            <h3>📈 ÉVOLUTION PAR MOIS DE SORTIE</h3>
        </div>
        """, unsafe_allow_html=True)
        
        monthly_stats = df.groupby('released_month').agg({
            'streams': ['mean', 'count']
        }).round(0)
        
        monthly_stats.columns = ['Streams_Moy', 'Nb_Sorties']
        
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
                 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        
        fig_monthly = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Streams moyens
        fig_monthly.add_trace(
            go.Bar(
                x=months,
                y=[monthly_stats.loc[i, 'Streams_Moy'] if i in monthly_stats.index else 0 for i in range(1, 13)],
                name="Streams Moyens",
                marker_color=SPOTIFY_GREEN,
                yaxis="y"
            ),
            secondary_y=False,
        )
        
        # Nombre de sorties
        fig_monthly.add_trace(
            go.Scatter(
                x=months,
                y=[monthly_stats.loc[i, 'Nb_Sorties'] if i in monthly_stats.index else 0 for i in range(1, 13)],
                mode='lines+markers',
                name="Nb Sorties",
                line=dict(color="#1ed760", width=3),
                marker=dict(size=8),
                yaxis="y2"
            ),
            secondary_y=True,
        )
        
        fig_monthly.update_xaxes(title_text="Mois")
        fig_monthly.update_yaxes(title_text="Streams Moyens", secondary_y=False, color=SPOTIFY_GREEN)
        fig_monthly.update_yaxes(title_text="Nombre de Sorties", secondary_y=True, color="#1ed760")
        
        fig_monthly.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=SPOTIFY_BLACK),
            legend=dict(x=0.01, y=0.99)
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    with col2:
        # Évolution par année
        st.markdown("""
        <div class="top-card">
            <h3>📊 ÉVOLUTION ANNUELLE</h3>
        </div>
        """, unsafe_allow_html=True)
        
        yearly_stats = df.groupby('released_year').agg({
            'streams': ['mean', 'sum', 'count']
        })
        yearly_stats.columns = ['Streams_Moy', 'Streams_Total', 'Nb_Titres']
        
        fig_yearly = go.Figure()
        
        fig_yearly.add_trace(go.Scatter(
            x=yearly_stats.index,
            y=yearly_stats['Streams_Moy'],
            mode='lines+markers',
            name='Streams Moyens',
            line=dict(color=SPOTIFY_GREEN, width=4),
            marker=dict(size=10, color=SPOTIFY_GREEN),
            fill='tozeroy',
            fillcolor=f'rgba(29, 185, 84, 0.2)'
        ))
        
        fig_yearly.update_layout(
            title="Performance Moyenne par Année",
            xaxis_title="Année",
            yaxis_title="Streams Moyens",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=SPOTIFY_BLACK)
        )
        
        st.plotly_chart(fig_yearly, use_container_width=True)
    
    # Insights temporels
    st.markdown("### 💡 **INSIGHTS TEMPORELS**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        best_month = monthly_stats['Streams_Moy'].idxmax()
        best_month_name = months[best_month-1]
        st.markdown(f"""
        <div class="insight-box">
            <h4>🏆 Meilleur Mois</h4>
            <p><strong>{best_month_name}</strong></p>
            <p>{monthly_stats.loc[best_month, 'Streams_Moy']:,.0f} streams moy.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        best_year = yearly_stats['Streams_Moy'].idxmax()
        st.markdown(f"""
        <div class="insight-box">
            <h4>📅 Meilleure Année</h4>
            <p><strong>{best_year}</strong></p>
            <p>{yearly_stats.loc[best_year, 'Streams_Moy']:,.0f} streams moy.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        growth = ((yearly_stats['Streams_Moy'].iloc[-1] - yearly_stats['Streams_Moy'].iloc[0]) / yearly_stats['Streams_Moy'].iloc[0] * 100)
        st.markdown(f"""
        <div class="insight-box">
            <h4>📈 Évolution</h4>
            <p><strong>{growth:+.1f}%</strong></p>
            <p>Depuis {yearly_stats.index[0]}</p>
        </div>
        """, unsafe_allow_html=True)

def create_comparisons(df, filters):
    """Comparaisons avancées avec boutons interactifs"""
    st.markdown('<h2 class="section-header">⚔️ COMPARAISONS INTERACTIVES</h2>', unsafe_allow_html=True)
    
    # Boutons de comparaison
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        hits_vs_other = st.button("🔥 Hits vs Autres", key="hits_comparison")
    with col2:
        solo_vs_collab = st.button("👤 Solo vs Collab", key="collab_comparison")
    with col3:
        major_vs_minor = st.button("🎵 Majeur vs Mineur", key="mode_comparison")
    with col4:
        recent_vs_old = st.button("📅 2023 vs 2022", key="year_comparison")
    
    # Section de comparaison
    if hits_vs_other:
        st.markdown("### 🔥 **HITS vs AUTRES TITRES**")
        
        hits = df[df['success_category'].isin(['🔥 Hit', '💎 Mega-Hit'])]
        others = df[~df['success_category'].isin(['🔥 Hit', '💎 Mega-Hit'])]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Métriques hits
            st.markdown(f"""
            <div class="top-card">
                <h4>🔥 HITS & MEGA-HITS</h4>
                <p><strong>{len(hits)}</strong> titres ({len(hits)/len(df)*100:.1f}%)</p>
                <p><strong>{hits['streams'].mean()/1e6:.0f}M</strong> streams moy.</p>
                <p><strong>{hits['danceability_%'].mean():.0f}%</strong> danceability</p>
                <p><strong>{hits['energy_%'].mean():.0f}%</strong> energy</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Métriques autres
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {SPOTIFY_BLACK};">⭐ AUTRES TITRES</h4>
                <p><strong>{len(others)}</strong> titres ({len(others)/len(df)*100:.1f}%)</p>
                <p><strong>{others['streams'].mean()/1e6:.0f}M</strong> streams moy.</p>
                <p><strong>{others['danceability_%'].mean():.0f}%</strong> danceability</p>
                <p><strong>{others['energy_%'].mean():.0f}%</strong> energy</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Graphique de comparaison
        features = ['danceability_%', 'energy_%', 'valence_%', 'acousticness_%']
        hits_profile = hits[features].mean()
        others_profile = others[features].mean()
        
        fig_comparison = go.Figure()
        
        fig_comparison.add_trace(go.Bar(
            name='Hits',
            x=[f.replace('_%', '') for f in features],
            y=hits_profile,
            marker_color=SPOTIFY_GREEN,
            text=[f"{v:.0f}%" for v in hits_profile],
            textposition='outside'
        ))
        
        fig_comparison.add_trace(go.Bar(
            name='Autres',
            x=[f.replace('_%', '') for f in features],
            y=others_profile,
            marker_color=SPOTIFY_GRAY,
            text=[f"{v:.0f}%" for v in others_profile],
            textposition='outside'
        ))
        
        fig_comparison.update_layout(
            title="Profil Musical : Hits vs Autres",
            xaxis_title="Caractéristiques",
            yaxis_title="Valeur Moyenne (%)",
            barmode='group',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=SPOTIFY_BLACK)
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    elif solo_vs_collab:
        st.markdown("### 👤 **SOLO vs COLLABORATIONS**")
        
        solo = df[df['artist_count'] == 1]
        collab = df[df['artist_count'] > 1]
        
        col1, col2 = st.columns(2)
        
        with col1:
            success_rate_solo = len(solo[solo['success_category'].isin(['🔥 Hit', '💎 Mega-Hit'])]) / len(solo) * 100
            st.markdown(f"""
            <div class="top-card">
                <h4>👤 ARTISTES SOLO</h4>
                <p><strong>{len(solo)}</strong> titres</p>
                <p><strong>{solo['streams'].mean()/1e6:.0f}M</strong> streams moy.</p>
                <p><strong>{success_rate_solo:.1f}%</strong> taux de succès</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            success_rate_collab = len(collab[collab['success_category'].isin(['🔥 Hit', '💎 Mega-Hit'])]) / len(collab) * 100
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {SPOTIFY_BLACK};">🤝 COLLABORATIONS</h4>
                <p><strong>{len(collab)}</strong> titres</p>
                <p><strong>{collab['streams'].mean()/1e6:.0f}M</strong> streams moy.</p>
                <p><strong>{success_rate_collab:.1f}%</strong> taux de succès</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif major_vs_minor:
        st.markdown("### 🎵 **MODE MAJEUR vs MINEUR**")
        
        major = df[df['mode'] == 'Major']
        minor = df[df['mode'] == 'Minor']
        
        if len(major) > 0 and len(minor) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="top-card">
                    <h4>🎵 MODE MAJEUR</h4>
                    <p><strong>{len(major)}</strong> titres</p>
                    <p><strong>{major['streams'].mean()/1e6:.0f}M</strong> streams moy.</p>
                    <p><strong>{major['valence_%'].mean():.0f}%</strong> valence moy.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: {SPOTIFY_BLACK};">🎼 MODE MINEUR</h4>
                    <p><strong>{len(minor)}</strong> titres</p>
                    <p><strong>{minor['streams'].mean()/1e6:.0f}M</strong> streams moy.</p>
                    <p><strong>{minor['valence_%'].mean():.0f}%</strong> valence moy.</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif recent_vs_old:
        st.markdown("### 📅 **2023 vs 2022**")
        
        recent = df[df['released_year'] == 2023]
        old = df[df['released_year'] == 2022]
        
        if len(recent) > 0 and len(old) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="top-card">
                    <h4>📅 SORTIES 2023</h4>
                    <p><strong>{len(recent)}</strong> titres</p>
                    <p><strong>{recent['streams'].mean()/1e6:.0f}M</strong> streams moy.</p>
                    <p><strong>{recent['total_playlists'].mean():.0f}</strong> playlists moy.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: {SPOTIFY_BLACK};">📅 SORTIES 2022</h4>
                    <p><strong>{len(old)}</strong> titres</p>
                    <p><strong>{old['streams'].mean()/1e6:.0f}M</strong> streams moy.</p>
                    <p><strong>{old['total_playlists'].mean():.0f}</strong> playlists moy.</p>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="insight-box">
            <h4>👆 Cliquez sur un bouton ci-dessus pour voir les comparaisons !</h4>
            <p>Explorez les différences entre :</p>
            <ul>
                <li>🔥 Hits vs autres titres</li>
                <li>👤 Artistes solo vs collaborations</li>
                <li>🎵 Mode majeur vs mineur</li>
                <li>📅 Sorties récentes vs anciennes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Fonction principale avec design cohérent"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🎵 SPOTIFY PREMIUM ANALYTICS</h1>
        <p>Dashboard professionnel avec charte graphique Spotify</p>
        <p>🏆 Tops • 🍩 Donuts • 📊 Analytics • 🎨 Design Premium</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    df = load_data()
    
    # Filtres sidebar
    filters = create_sidebar_filters(df)
    filtered_df = apply_filters(df, filters)
    
    if len(filtered_df) == 0:
        st.error("⚠️ Aucune donnée correspondante. Ajustez vos filtres.")
        return
    
    # KPIs
    create_kpis_dashboard(filtered_df)
    
    # Contenu selon le mode d'analyse
    if filters['analysis_mode'] == "📊 Vue d'ensemble":
        create_donut_charts_spotify(filtered_df, filters)
        
    elif filters['analysis_mode'] == "🏆 Top Performers":
        create_top_performers(filtered_df, filters)
        
    elif filters['analysis_mode'] == "🎼 Analyse Musicale":
        create_musical_analysis(filtered_df, filters)
        
    elif filters['analysis_mode'] == "📅 Tendances":
        create_temporal_trends(filtered_df, filters)
        
    elif filters['analysis_mode'] == "⚔️ Comparaisons":
        create_comparisons(filtered_df, filters)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; background: linear-gradient(135deg, {SPOTIFY_WHITE}, #f8f9fa); 
                border: 2px solid {SPOTIFY_GREEN}; border-radius: 15px; padding: 2rem; margin: 2rem 0;'>
        <h3 style='color: {SPOTIFY_BLACK};'>🎵 Spotify Premium Analytics</h3>
        <p style='color: {SPOTIFY_GRAY};'>Design cohérent • Charte graphique professionnelle • Expérience utilisateur optimale</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 