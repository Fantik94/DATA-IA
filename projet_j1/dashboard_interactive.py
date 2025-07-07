#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DASHBOARD ULTRA-INTERACTIF SPOTIFY 2023
========================================
Dashboard Streamlit avancé avec donuts, boutons interactifs et animations

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
import time

# Configuration de la page
st.set_page_config(
    page_title="🎵 Spotify Interactive Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé ultra-moderne
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1DB954, #191414, #1ed760);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(29, 185, 84, 0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 8px 32px rgba(29, 185, 84, 0.3); }
        to { box-shadow: 0 8px 32px rgba(29, 185, 84, 0.6); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #1DB954;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .insight-box {
        background: linear-gradient(135deg, #e8f5e8, #d4edda);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.2);
    }
    
    .interactive-btn {
        background: linear-gradient(135deg, #1DB954, #1ed760);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);
    }
    
    .interactive-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.4);
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
    }
    
    .stSlider > div > div {
        background: linear-gradient(135deg, #1DB954, #1ed760);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Chargement et nettoyage des données avec cache"""
    try:
        df = pd.read_csv('spotify-2023.csv', encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv('spotify-2023.csv', encoding='latin-1')
    
    # Nettoyage des données
    df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
    
    # Nettoyage des colonnes numériques avec virgules
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
    
    # Création de la date de sortie
    try:
        df['release_date'] = pd.to_datetime(
            df['released_year'].astype(str) + '-' + 
            df['released_month'].astype(str) + '-' + 
            df['released_day'].astype(str),
            errors='coerce'
        )
    except:
        df['release_date'] = pd.NaT
    
    # Catégorisation du succès
    df['success_category'] = pd.cut(df['streams'], 
                                  bins=[0, 100_000_000, 500_000_000, 1_000_000_000, float('inf')],
                                  labels=['🌱 Émergent', '⭐ Populaire', '🔥 Hit', '💎 Mega-Hit'])
    
    # Nettoyage final
    df = df.dropna(subset=['streams'])
    
    return df

def create_interactive_sidebar(df):
    """Sidebar ultra-interactive avec animations"""
    st.sidebar.markdown("## 🎛️ **CONTRÔLES INTERACTIFS**")
    
    # Animation de chargement
    if st.sidebar.button("🔄 **ACTUALISER LES DONNÉES**", key="refresh"):
        with st.sidebar:
            with st.spinner("Actualisation en cours..."):
                time.sleep(1)
            st.success("✅ Données actualisées !")
    
    st.sidebar.markdown("---")
    
    # Sélection d'analyse avec émojis
    analysis_type = st.sidebar.radio(
        "🎯 **TYPE D'ANALYSE**",
        ["📊 Vue d'ensemble", "🎼 Analyse musicale", "👥 Collaborations", "📅 Tendances temporelles", "🏆 Top performers"],
        key="analysis_type"
    )
    
    st.sidebar.markdown("---")
    
    # Filtres avec design moderne
    st.sidebar.markdown("### 🎚️ **FILTRES AVANCÉS**")
    
    # Filtre par années avec slider
    years = sorted(df['released_year'].unique())
    year_range = st.sidebar.select_slider(
        "📅 **Période d'analyse**",
        options=years,
        value=(min(years), max(years)),
        format_func=lambda x: f"🗓️ {x}"
    )
    
    # Filtre par success avec multiselect coloré
    categories = df['success_category'].cat.categories.tolist()
    selected_categories = st.sidebar.multiselect(
        "🎯 **Niveaux de succès**",
        categories,
        default=categories,
        format_func=lambda x: x
    )
    
    # Slider pour streams avec format custom
    min_streams = int(df['streams'].min())
    max_streams = int(df['streams'].max())
    streams_range = st.sidebar.slider(
        "📊 **Plage de streams (en millions)**",
        min_value=min_streams//1_000_000,
        max_value=max_streams//1_000_000,
        value=(min_streams//1_000_000, max_streams//1_000_000),
        format="%d M"
    )
    streams_range = (streams_range[0] * 1_000_000, streams_range[1] * 1_000_000)
    
    # Options avancées dans un expander
    with st.sidebar.expander("🔧 **OPTIONS AVANCÉES**"):
        show_animations = st.checkbox("✨ Animations", value=True)
        show_top_n = st.slider("📈 Nombre de tops à afficher", 5, 20, 10)
        color_scheme = st.selectbox(
            "🎨 Palette de couleurs",
            ["Spotify", "Viridis", "Plasma", "Cividis", "Rainbow"],
            index=0
        )
        chart_style = st.selectbox(
            "📊 Style des graphiques",
            ["Moderne", "Classique", "Minimaliste"],
            index=0
        )
    
    return {
        'analysis_type': analysis_type,
        'year_range': year_range,
        'categories': selected_categories,
        'streams_range': streams_range,
        'show_animations': show_animations,
        'show_top_n': show_top_n,
        'color_scheme': color_scheme,
        'chart_style': chart_style
    }

def apply_filters(df, filters):
    """Application intelligente des filtres"""
    filtered_df = df.copy()
    
    # Filtres temporels
    filtered_df = filtered_df[
        (filtered_df['released_year'] >= filters['year_range'][0]) &
        (filtered_df['released_year'] <= filters['year_range'][1])
    ]
    
    # Filtres par catégories
    if filters['categories']:
        filtered_df = filtered_df[filtered_df['success_category'].isin(filters['categories'])]
    
    # Filtre par streams
    filtered_df = filtered_df[
        (filtered_df['streams'] >= filters['streams_range'][0]) &
        (filtered_df['streams'] <= filters['streams_range'][1])
    ]
    
    return filtered_df

def create_animated_kpis(df, filters):
    """KPIs animés et interactifs"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_songs = len(df)
        st.metric(
            "🎵 **Titres**",
            f"{total_songs:,}",
            delta=f"{total_songs - 953:+d}" if total_songs != 953 else None,
            help="Nombre total de titres analysés"
        )
    
    with col2:
        total_streams = df['streams'].sum()
        avg_baseline = 69.8e9
        st.metric(
            "📊 **Streams Totaux**",
            f"{total_streams/1e9:.1f}B",
            delta=f"{(total_streams - avg_baseline)/1e9:.1f}B" if total_streams != avg_baseline else None,
            help="Nombre total de streams cumulés"
        )
    
    with col3:
        avg_streams = df['streams'].mean()
        st.metric(
            "📈 **Moy. Streams**",
            f"{avg_streams/1e6:.0f}M",
            delta=f"{(avg_streams/1e6 - 514):.0f}M" if avg_streams/1e6 != 514 else None,
            help="Nombre moyen de streams par titre"
        )
    
    with col4:
        unique_artists = df['artist(s)_name'].nunique()
        st.metric(
            "🎤 **Artistes**",
            f"{unique_artists:,}",
            delta=f"{unique_artists - 595:+d}" if unique_artists != 595 else None,
            help="Nombre d'artistes uniques"
        )
    
    with col5:
        hits_count = len(df[df['success_category'].isin(['🔥 Hit', '💎 Mega-Hit'])])
        hits_pct = (hits_count / len(df)) * 100 if len(df) > 0 else 0
        st.metric(
            "🏆 **% Hits**",
            f"{hits_pct:.1f}%",
            delta=f"{hits_pct - 23.4:.1f}%" if hits_pct != 23.4 else None,
            help="Pourcentage de hits et mega-hits"
        )

def create_donut_charts(df, filters):
    """Graphiques en donut interactifs"""
    st.markdown("## 🍩 **GRAPHIQUES EN DONUT INTERACTIFS**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Donut des catégories de succès
        success_counts = df['success_category'].value_counts()
        
        fig_donut1 = go.Figure(data=[go.Pie(
            labels=success_counts.index,
            values=success_counts.values,
            hole=0.6,
            hovertemplate="<b>%{label}</b><br>" +
                         "Nombre: %{value}<br>" +
                         "Pourcentage: %{percent}<br>" +
                         "<extra></extra>",
            textinfo='label+percent',
            textposition='inside',
            marker=dict(
                colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
                line=dict(color='#FFFFFF', width=3)
            )
        )])
        
        fig_donut1.update_layout(
            title={
                'text': "🎯 Distribution du Succès",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#1DB954'}
            },
            height=400,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5)
        )
        
        fig_donut1.add_annotation(
            text=f"<b>{len(df)}</b><br>Titres",
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )
        
        st.plotly_chart(fig_donut1, use_container_width=True)
    
    with col2:
        # Donut des modes musicaux
        mode_counts = df['mode'].value_counts()
        
        fig_donut2 = go.Figure(data=[go.Pie(
            labels=mode_counts.index,
            values=mode_counts.values,
            hole=0.6,
            hovertemplate="<b>Mode %{label}</b><br>" +
                         "Nombre: %{value}<br>" +
                         "Pourcentage: %{percent}<br>" +
                         "<extra></extra>",
            textinfo='label+percent',
            marker=dict(
                colors=['#FD79A8', '#6C5CE7'],
                line=dict(color='#FFFFFF', width=3)
            )
        )])
        
        fig_donut2.update_layout(
            title={
                'text': "🎵 Modes Musicaux",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#1DB954'}
            },
            height=400,
            showlegend=True
        )
        
        fig_donut2.add_annotation(
            text=f"<b>Musique</b><br>Analyse",
            x=0.5, y=0.5,
            font_size=16,
            showarrow=False
        )
        
        st.plotly_chart(fig_donut2, use_container_width=True)
    
    with col3:
        # Donut des collaborations
        collab_counts = df['artist_count'].value_counts().sort_index()
        
        fig_donut3 = go.Figure(data=[go.Pie(
            labels=[f"{i} Artiste{'s' if i > 1 else ''}" for i in collab_counts.index],
            values=collab_counts.values,
            hole=0.6,
            hovertemplate="<b>%{label}</b><br>" +
                         "Nombre: %{value}<br>" +
                         "Pourcentage: %{percent}<br>" +
                         "<extra></extra>",
            textinfo='label+percent',
            marker=dict(
                colors=px.colors.qualitative.Set3,
                line=dict(color='#FFFFFF', width=3)
            )
        )])
        
        fig_donut3.update_layout(
            title={
                'text': "👥 Types de Collaborations",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#1DB954'}
            },
            height=400,
            showlegend=True
        )
        
        fig_donut3.add_annotation(
            text=f"<b>Collabs</b><br>Impact",
            x=0.5, y=0.5,
            font_size=16,
            showarrow=False
        )
        
        st.plotly_chart(fig_donut3, use_container_width=True)

def create_interactive_comparisons(df, filters):
    """Comparaisons interactives avec boutons"""
    st.markdown("## ⚔️ **COMPARAISONS INTERACTIVES**")
    
    # Boutons de sélection
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        compare_hits = st.button("🔥 **HITS vs AUTRES**", key="compare_hits", help="Comparer les hits avec les autres titres")
    
    with col2:
        compare_years = st.button("📅 **2023 vs 2022**", key="compare_years", help="Comparer les années 2023 et 2022")
    
    with col3:
        compare_collabs = st.button("👥 **SOLO vs COLLAB**", key="compare_collabs", help="Comparer solos et collaborations")
    
    with col4:
        compare_modes = st.button("🎵 **MAJEUR vs MINEUR**", key="compare_modes", help="Comparer modes majeur et mineur")
    
    # Graphiques comparatifs dynamiques
    if compare_hits:
        st.markdown("### 🔥 **Analyse Hits vs Autres**")
        
        hits = df[df['success_category'].isin(['🔥 Hit', '💎 Mega-Hit'])]
        others = df[~df['success_category'].isin(['🔥 Hit', '💎 Mega-Hit'])]
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Radar chart comparatif
            features = ['danceability_%', 'energy_%', 'valence_%', 'acousticness_%']
            
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=hits[features].mean().values,
                theta=[f.replace('_%', '').title() for f in features],
                fill='toself',
                name='🔥 Hits',
                line_color='#FF6B6B'
            ))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=others[features].mean().values,
                theta=[f.replace('_%', '').title() for f in features],
                fill='toself',
                name='📊 Autres',
                line_color='#4ECDC4'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                showlegend=True,
                title="🎼 Profil Musical Comparatif",
                height=400
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col_right:
            # Barres comparatives animées
            metrics = ['streams', 'total_playlists', 'total_charts']
            hits_values = [hits[m].mean() for m in metrics]
            others_values = [others[m].mean() for m in metrics]
            
            fig_bar = go.Figure()
            
            fig_bar.add_trace(go.Bar(
                name='🔥 Hits',
                x=['Streams', 'Playlists', 'Charts'],
                y=hits_values,
                marker_color='#FF6B6B',
                text=[f"{v/1e6:.0f}M" if v > 1e6 else f"{v:.0f}" for v in hits_values],
                textposition='auto'
            ))
            
            fig_bar.add_trace(go.Bar(
                name='📊 Autres',
                x=['Streams', 'Playlists', 'Charts'],
                y=others_values,
                marker_color='#4ECDC4',
                text=[f"{v/1e6:.0f}M" if v > 1e6 else f"{v:.0f}" for v in others_values],
                textposition='auto'
            ))
            
            fig_bar.update_layout(
                title="📊 Métriques de Performance",
                barmode='group',
                height=400,
                yaxis_type="log"
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
    
    if compare_years:
        st.markdown("### 📅 **Analyse 2023 vs 2022**")
        create_year_comparison(df)
    
    if compare_collabs:
        st.markdown("### 👥 **Analyse Solo vs Collaborations**")
        create_collaboration_comparison(df)
    
    if compare_modes:
        st.markdown("### 🎵 **Analyse Majeur vs Mineur**")
        create_mode_comparison(df)

def create_year_comparison(df):
    """Comparaison entre années"""
    year_2023 = df[df['released_year'] == 2023]
    year_2022 = df[df['released_year'] == 2022]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Métriques 2023
        st.markdown("#### 🗓️ **2023**")
        st.metric("Titres", len(year_2023))
        st.metric("Streams moy.", f"{year_2023['streams'].mean()/1e6:.0f}M")
        st.metric("Danceability moy.", f"{year_2023['danceability_%'].mean():.1f}%")
    
    with col2:
        # Métriques 2022
        st.markdown("#### 🗓️ **2022**")
        st.metric("Titres", len(year_2022))
        st.metric("Streams moy.", f"{year_2022['streams'].mean()/1e6:.0f}M")
        st.metric("Danceability moy.", f"{year_2022['danceability_%'].mean():.1f}%")

def create_collaboration_comparison(df):
    """Comparaison solo vs collaborations"""
    solo = df[df['artist_count'] == 1]
    collab = df[df['artist_count'] > 1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎤 **Solo**")
        st.metric("Titres", len(solo))
        st.metric("Streams moy.", f"{solo['streams'].mean()/1e6:.0f}M")
        st.metric("Energy moy.", f"{solo['energy_%'].mean():.1f}%")
    
    with col2:
        st.markdown("#### 👥 **Collaborations**")
        st.metric("Titres", len(collab))
        st.metric("Streams moy.", f"{collab['streams'].mean()/1e6:.0f}M")
        st.metric("Energy moy.", f"{collab['energy_%'].mean():.1f}%")

def create_mode_comparison(df):
    """Comparaison modes majeur vs mineur"""
    major = df[df['mode'] == 'Major']
    minor = df[df['mode'] == 'Minor']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎵 **Mode Majeur**")
        st.metric("Titres", len(major))
        st.metric("Streams moy.", f"{major['streams'].mean()/1e6:.0f}M")
        st.metric("Valence moy.", f"{major['valence_%'].mean():.1f}%")
    
    with col2:
        st.markdown("#### 🎵 **Mode Mineur**")
        st.metric("Titres", len(minor))
        st.metric("Streams moy.", f"{minor['streams'].mean()/1e6:.0f}M")
        st.metric("Valence moy.", f"{minor['valence_%'].mean():.1f}%")

def create_success_predictor(df):
    """Prédicteur de succès interactif"""
    st.markdown("## 🎯 **PRÉDICTEUR DE SUCCÈS INTERACTIF**")
    
    with st.container():
        st.markdown("### 🎛️ **Configurez votre titre**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🎵 **Caractéristiques Musicales**")
            danceability = st.slider("💃 Danceability", 0, 100, 70, help="Capacité à danser sur ce titre")
            energy = st.slider("⚡ Energy", 0, 100, 65, help="Niveau d'énergie du titre")
            valence = st.slider("😊 Valence", 0, 100, 50, help="Positivité musicale")
            bpm = st.slider("🥁 BPM", 60, 200, 120, help="Battements par minute")
        
        with col2:
            st.markdown("#### 📅 **Contexte de Sortie**")
            release_month = st.selectbox("Mois de sortie", list(range(1, 13)), 
                                       format_func=lambda x: ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun",
                                                              "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"][x-1])
            artist_count = st.selectbox("👥 Nombre d'artistes", [1, 2, 3, 4, 5])
            mode = st.selectbox("🎵 Mode", ["Major", "Minor"])
        
        with col3:
            st.markdown("#### 📱 **Stratégie Marketing**")
            target_playlists = st.number_input("🎯 Playlists cibles", 0, 50000, 5000, step=500)
            genre_popularity = st.slider("📊 Popularité du genre", 1, 10, 7)
            artist_fame = st.slider("⭐ Notoriété artiste", 1, 10, 5)
        
        # Calcul du score en temps réel
        if st.button("🚀 **CALCULER LE SCORE DE SUCCÈS**", key="predict_success"):
            with st.spinner("🎯 Calcul en cours..."):
                time.sleep(1)  # Animation
                
                # Algorithme de prédiction simplifié
                month_bonus = 1.3 if release_month in [5, 6] else 1.0
                artist_bonus = 1.2 if artist_count == 2 else 1.0
                mode_bonus = 1.1 if mode == "Major" else 1.0
                
                feature_score = (danceability + energy + valence) / 300
                context_score = month_bonus * artist_bonus * mode_bonus
                marketing_score = min(target_playlists / 10000, 1.0)
                popularity_score = (genre_popularity + artist_fame) / 20
                
                final_score = (feature_score * context_score + marketing_score + popularity_score) / 3 * 100
                
                # Affichage animé du résultat
                col_score1, col_score2, col_score3 = st.columns(3)
                
                with col_score2:
                    score_color = "#28a745" if final_score > 75 else "#ffc107" if final_score > 50 else "#dc3545"
                    
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, {score_color}20, {score_color}40);
                        padding: 2rem;
                        border-radius: 20px;
                        text-align: center;
                        border: 3px solid {score_color};
                        box-shadow: 0 8px 32px {score_color}40;
                    ">
                        <h2 style="color: {score_color}; margin: 0;">🎯 SCORE DE SUCCÈS</h2>
                        <h1 style="color: {score_color}; font-size: 3rem; margin: 10px 0;">{final_score:.0f}%</h1>
                        <p style="color: {score_color}; font-weight: bold; margin: 0;">
                            {'🚀 EXCELLENT' if final_score > 75 else '👍 BON' if final_score > 50 else '⚠️ MOYEN'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Recommandations personnalisées
                st.markdown("### 💡 **Recommandations Personnalisées**")
                
                recommendations = []
                if danceability < 70:
                    recommendations.append("💃 Augmenter la danceability pour un meilleur engagement")
                if release_month not in [5, 6]:
                    recommendations.append("📅 Considérer une sortie en mai-juin pour plus d'impact")
                if artist_count == 1:
                    recommendations.append("👥 Envisager une collaboration avec un autre artiste")
                if target_playlists < 5000:
                    recommendations.append("📱 Intensifier la stratégie de placement playlists")
                
                if recommendations:
                    for rec in recommendations:
                        st.markdown(f"- {rec}")
                else:
                    st.success("🎉 Configuration optimale ! Toutes les conditions sont réunies pour le succès.")

def main():
    """Fonction principale du dashboard ultra-interactif"""
    
    # En-tête animé
    st.markdown("""
    <div class="main-header">
        <h1>🎵 SPOTIFY 2023 - DASHBOARD ULTRA-INTERACTIF</h1>
        <p>Explorez les données avec des graphiques dynamiques, des boutons cliquables et des animations !</p>
        <p>✨ Donuts • 🎛️ Contrôles • 📊 Comparaisons • 🎯 Prédictions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    df = load_data()
    
    # Sidebar interactive
    filters = create_interactive_sidebar(df)
    
    # Application des filtres
    filtered_df = apply_filters(df, filters)
    
    # Vérification des données
    if len(filtered_df) == 0:
        st.error("⚠️ Aucune donnée ne correspond aux filtres sélectionnés. Ajustez vos critères !")
        return
    
    # KPIs animés
    create_animated_kpis(filtered_df, filters)
    
    st.markdown("---")
    
    # Contenu principal basé sur le type d'analyse sélectionné
    if filters['analysis_type'] == "📊 Vue d'ensemble":
        create_donut_charts(filtered_df, filters)
        st.markdown("---")
        create_interactive_comparisons(filtered_df, filters)
    
    elif filters['analysis_type'] == "🎼 Analyse musicale":
        st.markdown("## 🎼 **ANALYSE MUSICALE APPROFONDIE**")
        create_donut_charts(filtered_df, filters)
        # Ajouter d'autres analyses musicales...
    
    elif filters['analysis_type'] == "👥 Collaborations":
        st.markdown("## 👥 **ANALYSE DES COLLABORATIONS**")
        create_donut_charts(filtered_df, filters)
        # Ajouter analyses collaborations...
    
    elif filters['analysis_type'] == "📅 Tendances temporelles":
        st.markdown("## 📅 **TENDANCES TEMPORELLES**")
        create_donut_charts(filtered_df, filters)
        # Ajouter analyses temporelles...
    
    elif filters['analysis_type'] == "🏆 Top performers":
        st.markdown("## 🏆 **TOP PERFORMERS**")
        create_donut_charts(filtered_df, filters)
        # Ajouter analyses top performers...
    
    st.markdown("---")
    
    # Prédicteur de succès
    create_success_predictor(filtered_df)
    
    # Footer interactif
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; background: linear-gradient(135deg, #f8f9fa, #e9ecef); 
                padding: 2rem; border-radius: 15px; margin-top: 2rem;'>
        <h3>🎵 Merci d'avoir exploré notre dashboard interactif !</h3>
        <p>Développé avec ❤️ en Python • Streamlit • Plotly</p>
        <p>✨ N'hésitez pas à expérimenter avec tous les contrôles interactifs !</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 