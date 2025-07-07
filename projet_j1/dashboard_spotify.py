#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DASHBOARD INTERACTIF SPOTIFY 2023
==================================
Dashboard Streamlit pour l'analyse interactive des facteurs de succès musical

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
    page_title="🎵 Spotify 2023 Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1DB954, #191414);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1DB954;
    }
    .insight-box {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
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
    
    # Création de la date de sortie (si nécessaire)
    if 'release_date' not in df.columns:
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
                                  labels=['Émergent', 'Populaire', 'Hit', 'Mega-Hit'])
    
    # Nettoyage final
    df = df.dropna(subset=['streams'])
    
    return df

def create_sidebar_filters(df):
    """Création des filtres dans la sidebar"""
    st.sidebar.markdown("## 🎛️ Filtres Interactifs")
    
    # Filtre par année
    years = sorted(df['released_year'].unique())
    selected_years = st.sidebar.multiselect(
        "📅 Années de sortie",
        years,
        default=[2023, 2022, 2021]
    )
    
    # Filtre par catégorie de succès
    categories = df['success_category'].cat.categories.tolist()
    selected_categories = st.sidebar.multiselect(
        "🎯 Catégories de succès",
        categories,
        default=categories
    )
    
    # Filtre par nombre d'artistes
    max_artists = int(df['artist_count'].max())
    artist_range = st.sidebar.slider(
        "👥 Nombre d'artistes",
        1, max_artists, (1, max_artists)
    )
    
    # Filtre par streams
    min_streams = int(df['streams'].min())
    max_streams = int(df['streams'].max())
    streams_range = st.sidebar.slider(
        "📊 Plage de streams",
        min_streams, max_streams, 
        (min_streams, max_streams),
        format="%d"
    )
    
    # Filtre par caractéristiques musicales
    st.sidebar.markdown("### 🎵 Caractéristiques Musicales")
    
    danceability_range = st.sidebar.slider(
        "💃 Danceability (%)", 0, 100, (0, 100)
    )
    
    energy_range = st.sidebar.slider(
        "⚡ Energy (%)", 0, 100, (0, 100)
    )
    
    valence_range = st.sidebar.slider(
        "😊 Valence (%)", 0, 100, (0, 100)
    )
    
    return {
        'years': selected_years,
        'categories': selected_categories,
        'artist_range': artist_range,
        'streams_range': streams_range,
        'danceability_range': danceability_range,
        'energy_range': energy_range,
        'valence_range': valence_range
    }

def apply_filters(df, filters):
    """Application des filtres au dataframe"""
    filtered_df = df.copy()
    
    # Filtre par années
    if filters['years']:
        filtered_df = filtered_df[filtered_df['released_year'].isin(filters['years'])]
    
    # Filtre par catégories
    if filters['categories']:
        filtered_df = filtered_df[filtered_df['success_category'].isin(filters['categories'])]
    
    # Filtre par nombre d'artistes
    filtered_df = filtered_df[
        (filtered_df['artist_count'] >= filters['artist_range'][0]) &
        (filtered_df['artist_count'] <= filters['artist_range'][1])
    ]
    
    # Filtre par streams
    filtered_df = filtered_df[
        (filtered_df['streams'] >= filters['streams_range'][0]) &
        (filtered_df['streams'] <= filters['streams_range'][1])
    ]
    
    # Filtres caractéristiques musicales
    filtered_df = filtered_df[
        (filtered_df['danceability_%'] >= filters['danceability_range'][0]) &
        (filtered_df['danceability_%'] <= filters['danceability_range'][1]) &
        (filtered_df['energy_%'] >= filters['energy_range'][0]) &
        (filtered_df['energy_%'] <= filters['energy_range'][1]) &
        (filtered_df['valence_%'] >= filters['valence_range'][0]) &
        (filtered_df['valence_%'] <= filters['valence_range'][1])
    ]
    
    return filtered_df

def display_kpis(df):
    """Affichage des KPIs principaux"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🎵 Titres Analysés",
            f"{len(df):,}",
            delta=f"{len(df) - 953:+d}" if len(df) != 953 else None
        )
    
    with col2:
        total_streams = df['streams'].sum()
        st.metric(
            "📊 Streams Totaux",
            f"{total_streams/1e9:.1f}B",
            delta=f"{(total_streams/1e9 - 69.8):.1f}B" if total_streams/1e9 != 69.8 else None
        )
    
    with col3:
        avg_streams = df['streams'].mean()
        st.metric(
            "📈 Streams Moyens",
            f"{avg_streams/1e6:.0f}M",
            delta=f"{(avg_streams/1e6 - 514):.0f}M" if avg_streams/1e6 != 514 else None
        )
    
    with col4:
        unique_artists = df['artist(s)_name'].nunique()
        st.metric(
            "🎤 Artistes Uniques",
            f"{unique_artists:,}",
            delta=f"{unique_artists - 595:+d}" if unique_artists != 595 else None
        )
    
    with col5:
        hits_count = len(df[df['success_category'].isin(['Hit', 'Mega-Hit'])])
        hits_pct = (hits_count / len(df)) * 100 if len(df) > 0 else 0
        st.metric(
            "🏆 % Hits",
            f"{hits_pct:.1f}%",
            delta=f"{hits_pct - 23.4:.1f}%" if hits_pct != 23.4 else None
        )

def create_temporal_analysis(df):
    """Analyse temporelle interactive"""
    st.markdown("## 📅 Analyse Temporelle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Streams par mois
        monthly_stats = df.groupby('released_month').agg({
            'streams': 'mean',
            'track_name': 'count'
        }).reset_index()
        
        fig = px.bar(
            monthly_stats,
            x='released_month',
            y='streams',
            title="Streams Moyens par Mois de Sortie",
            labels={'released_month': 'Mois', 'streams': 'Streams Moyens'},
            color='streams',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Nombre de sorties par mois
        fig2 = px.line(
            monthly_stats,
            x='released_month',
            y='track_name',
            title="Nombre de Sorties par Mois",
            labels={'released_month': 'Mois', 'track_name': 'Nombre de Sorties'},
            markers=True
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Analyse par année
    yearly_stats = df.groupby('released_year').agg({
        'streams': ['mean', 'sum', 'count']
    }).reset_index()
    yearly_stats.columns = ['year', 'avg_streams', 'total_streams', 'count']
    
    st.markdown("### 📊 Évolution Annuelle")
    
    col3, col4 = st.columns(2)
    
    with col3:
        fig3 = px.bar(
            yearly_stats,
            x='year',
            y='avg_streams',
            title="Streams Moyens par Année",
            color='avg_streams',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        fig4 = px.scatter(
            yearly_stats,
            x='count',
            y='avg_streams',
            size='total_streams',
            title="Relation Volume vs Performance",
            labels={'count': 'Nombre de Sorties', 'avg_streams': 'Streams Moyens'},
            hover_data=['year']
        )
        st.plotly_chart(fig4, use_container_width=True)

def create_musical_features_analysis(df):
    """Analyse des caractéristiques musicales"""
    st.markdown("## 🎼 Analyse des Caractéristiques Musicales")
    
    musical_features = ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 
                       'instrumentalness_%', 'liveness_%', 'speechiness_%']
    
    # Profil par catégorie de succès
    feature_by_success = df.groupby('success_category')[musical_features].mean().reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart pour profils musicaux
        categories = feature_by_success['success_category'].unique()
        
        fig = go.Figure()
        
        for category in categories:
            category_data = feature_by_success[feature_by_success['success_category'] == category]
            values = category_data[musical_features].iloc[0].tolist()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=[f.replace('_%', '') for f in musical_features],
                fill='toself',
                name=category
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Profil Musical par Catégorie de Succès",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Correlation heatmap
        corr_features = musical_features + ['streams', 'total_playlists']
        correlation_matrix = df[corr_features].corr()
        
        fig = px.imshow(
            correlation_matrix,
            title="Matrice de Corrélations",
            color_continuous_scale='RdBu_r',
            aspect="auto"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Analyse détaillée par feature
    st.markdown("### 🔍 Analyse Détaillée par Caractéristique")
    
    selected_feature = st.selectbox(
        "Sélectionnez une caractéristique à analyser:",
        musical_features,
        format_func=lambda x: x.replace('_%', '').title()
    )
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Distribution de la feature sélectionnée
        fig = px.histogram(
            df,
            x=selected_feature,
            color='success_category',
            title=f"Distribution - {selected_feature.replace('_%', '').title()}",
            marginal="violin",
            nbins=30
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        # Relation avec les streams
        fig = px.scatter(
            df.sample(min(1000, len(df))),  # Échantillon pour performance
            x=selected_feature,
            y='streams',
            color='success_category',
            title=f"{selected_feature.replace('_%', '').title()} vs Streams",
            trendline="ols",
            log_y=True
        )
        st.plotly_chart(fig, use_container_width=True)

def create_collaboration_analysis(df):
    """Analyse des collaborations"""
    st.markdown("## 🤝 Analyse des Collaborations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Impact nombre d'artistes
        collab_stats = df.groupby('artist_count').agg({
            'streams': ['mean', 'count'],
            'total_playlists': 'mean'
        }).reset_index()
        collab_stats.columns = ['artist_count', 'avg_streams', 'song_count', 'avg_playlists']
        
        fig = px.bar(
            collab_stats,
            x='artist_count',
            y='avg_streams',
            title="Streams Moyens par Nombre d'Artistes",
            text='song_count',
            labels={'artist_count': 'Nombre d\'Artistes', 'avg_streams': 'Streams Moyens'}
        )
        fig.update_traces(texttemplate='%{text} titres', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Success rate par nombre d'artistes
        success_rate = df.groupby('artist_count').apply(
            lambda x: (x['success_category'].isin(['Hit', 'Mega-Hit']).sum() / len(x)) * 100
        ).reset_index()
        success_rate.columns = ['artist_count', 'success_rate']
        
        fig = px.line(
            success_rate,
            x='artist_count',
            y='success_rate',
            title="Taux de Succès par Nombre d'Artistes",
            markers=True,
            labels={'artist_count': 'Nombre d\'Artistes', 'success_rate': 'Taux de Succès (%)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top collaborations
    st.markdown("### 🏆 Top Collaborations")
    
    top_collabs = df[df['artist_count'] > 1].nlargest(10, 'streams')[
        ['track_name', 'artist(s)_name', 'streams', 'artist_count', 'success_category']
    ]
    
    # Formatage pour affichage
    top_collabs['streams_formatted'] = top_collabs['streams'].apply(lambda x: f"{x/1e6:.0f}M")
    top_collabs_display = top_collabs[['track_name', 'artist(s)_name', 'streams_formatted', 'artist_count', 'success_category']]
    top_collabs_display.columns = ['Titre', 'Artistes', 'Streams', 'Nb Artistes', 'Catégorie']
    
    st.dataframe(top_collabs_display, use_container_width=True)

def create_platform_analysis(df):
    """Analyse par plateforme"""
    st.markdown("## 📱 Analyse par Plateforme")
    
    platform_cols = ['in_spotify_playlists', 'in_apple_playlists', 'in_deezer_playlists']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance par plateforme
        platform_stats = df[platform_cols + ['streams']].corr()['streams'].drop('streams')
        
        fig = px.bar(
            x=platform_stats.index,
            y=platform_stats.values,
            title="Corrélation Plateforme vs Streams",
            labels={'x': 'Plateforme', 'y': 'Corrélation avec Streams'},
            color=platform_stats.values,
            color_continuous_scale='Viridis'
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distribution des playlists
        df_melted = df.melt(
            value_vars=platform_cols,
            var_name='Platform',
            value_name='Playlists'
        )
        
        fig = px.box(
            df_melted,
            x='Platform',
            y='Playlists',
            title="Distribution des Playlists par Plateforme",
            log_y=True
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Analyse croisée plateformes
    st.markdown("### 🔄 Analyse Croisée des Plateformes")
    
    # Matrice de corrélation des plateformes
    platform_corr = df[platform_cols].corr()
    
    fig = px.imshow(
        platform_corr,
        title="Corrélations entre Plateformes",
        color_continuous_scale='RdBu_r'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def generate_insights(df):
    """Génération d'insights automatiques"""
    st.markdown("## 🎯 Insights & Recommandations")
    
    # Calculs pour insights
    best_month = df.groupby('released_month')['streams'].mean().idxmax()
    months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
             'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
    
    optimal_artists = df.groupby('artist_count')['streams'].mean().idxmax()
    
    # Caractéristiques des hits
    hits = df[df['success_category'].isin(['Hit', 'Mega-Hit'])]
    avg_danceability = hits['danceability_%'].mean()
    avg_energy = hits['energy_%'].mean()
    
    # Corrélation playlists
    playlist_corr = df[['total_playlists', 'streams']].corr().iloc[0, 1]
    
    # Affichage des insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h4>💡 Insights Clés Découverts</h4>
        <ul>
        <li><strong>Meilleur mois pour sortir :</strong> {}</li>
        <li><strong>Nombre optimal d'artistes :</strong> {}</li>
        <li><strong>Danceability moyenne des hits :</strong> {:.0f}%</li>
        <li><strong>Energy moyenne des hits :</strong> {:.0f}%</li>
        <li><strong>Corrélation playlists-succès :</strong> {:.2f}</li>
        </ul>
        </div>
        """.format(
            months[best_month-1],
            optimal_artists,
            avg_danceability,
            avg_energy,
            playlist_corr
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
        <h4>🚀 Recommandations Stratégiques</h4>
        <ul>
        <li><strong>Production :</strong> Cibler 70%+ danceability</li>
        <li><strong>Timing :</strong> Privilégier sorties mai-juin</li>
        <li><strong>Collaborations :</strong> Duos d'artistes performent mieux</li>
        <li><strong>Marketing :</strong> Focus placement playlists</li>
        <li><strong>A&R :</strong> Prioriser profils énergiques</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Prédicteur de succès
    st.markdown("### 🎯 Prédicteur de Succès")
    
    predictor_col1, predictor_col2, predictor_col3 = st.columns(3)
    
    with predictor_col1:
        pred_danceability = st.slider("Danceability prédite", 0, 100, 70)
        pred_energy = st.slider("Energy prédite", 0, 100, 65)
    
    with predictor_col2:
        pred_artists = st.selectbox("Nombre d'artistes", [1, 2, 3, 4, 5])
        pred_month = st.selectbox("Mois de sortie", list(range(1, 13)), index=4)
    
    with predictor_col3:
        pred_playlists = st.number_input("Playlists cibles", min_value=0, max_value=50000, value=5000)
    
    # Calcul score de succès simplifié
    month_bonus = 1.2 if pred_month in [5, 6] else 1.0
    artist_bonus = 1.15 if pred_artists == 2 else 1.0
    feature_score = (pred_danceability + pred_energy) / 200
    playlist_score = min(pred_playlists / 10000, 1.0)
    
    success_score = (feature_score * month_bonus * artist_bonus + playlist_score) / 2 * 100
    
    st.metric(
        "🎯 Score de Succès Prédit",
        f"{success_score:.0f}%",
        delta=f"{'Excellent' if success_score > 80 else 'Bon' if success_score > 60 else 'Moyen'}"
    )

def main():
    """Fonction principale du dashboard"""
    
    # En-tête principal
    st.markdown("""
    <div class="main-header">
        <h1>🎵 SPOTIFY 2023 - ANALYTICS DASHBOARD</h1>
        <p>Analyse interactive des facteurs de succès musical</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    df = load_data()
    
    # Sidebar avec filtres
    filters = create_sidebar_filters(df)
    
    # Application des filtres
    filtered_df = apply_filters(df, filters)
    
    # Message si pas de données après filtrage
    if len(filtered_df) == 0:
        st.error("⚠️ Aucune donnée ne correspond aux filtres sélectionnés. Veuillez ajuster vos critères.")
        return
    
    # Affichage des KPIs
    display_kpis(filtered_df)
    
    # Onglets pour différentes analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Analyse Temporelle", 
        "🎼 Caractéristiques Musicales", 
        "🤝 Collaborations", 
        "📱 Plateformes",
        "🎯 Insights"
    ])
    
    with tab1:
        create_temporal_analysis(filtered_df)
    
    with tab2:
        create_musical_features_analysis(filtered_df)
    
    with tab3:
        create_collaboration_analysis(filtered_df)
    
    with tab4:
        create_platform_analysis(filtered_df)
    
    with tab5:
        generate_insights(filtered_df)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🎵 Dashboard créé avec Streamlit • Data Science Project 2024</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 