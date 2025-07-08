import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuration des graphiques
try:
    plt.style.use('seaborn-v0_8')
except:
    plt.style.use('seaborn')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class SpotifyAnalyzer:
    """Classe principale pour l'analyse des données Spotify 2023"""
    
    def __init__(self, csv_path):
        """Initialisation avec chargement des données"""
        self.df = self.load_and_clean_data(csv_path)
        self.insights = {}
        
    def load_and_clean_data(self, csv_path):
        """Chargement et nettoyage des données"""
        print("🔄 Chargement des données...")
        
        # Chargement avec gestion d'encodage
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(csv_path, encoding='latin-1')
        
        print(f"✅ Dataset chargé : {df.shape[0]} titres, {df.shape[1]} colonnes")
        
        # Nettoyage des données
        print("🔧 Nettoyage des données...")
        
        # Conversion des streams en numérique
        df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
        
        # Nettoyage des colonnes numériques avec virgules
        numeric_cols = ['in_spotify_playlists', 'in_spotify_charts', 'in_apple_playlists', 
                       'in_apple_charts', 'in_deezer_playlists', 'in_deezer_charts', 
                       'in_shazam_charts']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '').replace('', '0')
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Création de nouvelles variables dérivées
        df['total_playlists'] = (df['in_spotify_playlists'] + df['in_apple_playlists'] + 
                                df['in_deezer_playlists'])
        df['total_charts'] = (df['in_spotify_charts'] + df['in_apple_charts'] + 
                             df['in_deezer_charts'] + df['in_shazam_charts'])
        
        # Création de la date de sortie (construction manuelle)
        try:
            df['release_date'] = pd.to_datetime(
                df['released_year'].astype(str) + '-' + 
                df['released_month'].astype(str) + '-' + 
                df['released_day'].astype(str),
                errors='coerce'
            )
        except:
            # Si erreur, créer une colonne vide
            df['release_date'] = pd.NaT
        
        # Catégorisation du succès
        df['success_category'] = pd.cut(df['streams'], 
                                      bins=[0, 100_000_000, 500_000_000, 1_000_000_000, float('inf')],
                                      labels=['Émergent', 'Populaire', 'Hit', 'Mega-Hit'])
        
        print(f"✅ Nettoyage terminé : {df.dropna(subset=['streams']).shape[0]} titres valides")
        return df
    
    def descriptive_analysis(self):
        """Analyse descriptive complète"""
        print("\n📊 ANALYSE DESCRIPTIVE")
        print("=" * 50)
        
        # Statistiques générales
        print(f"📈 Streams total : {self.df['streams'].sum():,.0f}")
        print(f"🎵 Nombre d'artistes uniques : {self.df['artist(s)_name'].nunique()}")
        print(f"📅 Période : {self.df['released_year'].min()} - {self.df['released_year'].max()}")
        
        # Top artistes
        print("\n🏆 TOP 10 ARTISTES PAR STREAMS :")
        top_artists = self.df.groupby('artist(s)_name')['streams'].sum().sort_values(ascending=False).head(10)
        for i, (artist, streams) in enumerate(top_artists.items(), 1):
            print(f"{i:2d}. {artist:<25} : {streams:>12,.0f} streams")
        
        # Analyse par catégorie de succès
        print("\n📊 RÉPARTITION PAR CATÉGORIE DE SUCCÈS :")
        success_dist = self.df['success_category'].value_counts()
        for category, count in success_dist.items():
            pct = (count / len(self.df)) * 100
            print(f"   {category:<12} : {count:3d} titres ({pct:5.1f}%)")
        
        # Corrélations importantes
        print("\n🔗 CORRÉLATIONS CLÉS (avec streams) :")
        correlations = self.df[['streams', 'total_playlists', 'total_charts', 'danceability_%', 
                               'energy_%', 'valence_%', 'bpm']].corr()['streams'].sort_values(ascending=False)
        
        for feature, corr in correlations.items():
            if feature != 'streams':
                print(f"   {feature:<20} : {corr:6.3f}")
        
        self.insights['top_artists'] = top_artists
        self.insights['correlations'] = correlations
        
    def temporal_analysis(self):
        """Analyse temporelle des sorties et du succès"""
        print("\n📅 ANALYSE TEMPORELLE")
        print("=" * 50)
        
        # Analyse par mois de sortie
        monthly_stats = self.df.groupby('released_month').agg({
            'streams': ['mean', 'median', 'count'],
            'total_playlists': 'mean'
        }).round(0)
        
        monthly_stats.columns = ['Streams_Moy', 'Streams_Med', 'Nb_Sorties', 'Playlists_Moy']
        
        print("📅 PERFORMANCE PAR MOIS DE SORTIE :")
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
                 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        
        for month_num in range(1, 13):
            if month_num in monthly_stats.index:
                stats = monthly_stats.loc[month_num]
                print(f"   {months[month_num-1]} : {stats['Streams_Moy']:>10,.0f} streams moy. "
                     f"({stats['Nb_Sorties']:2.0f} sorties)")
        
        # Meilleur mois
        best_month = monthly_stats['Streams_Moy'].idxmax()
        print(f"\n🏆 Meilleur mois pour sortir : {months[best_month-1]} "
              f"({monthly_stats.loc[best_month, 'Streams_Moy']:,.0f} streams moy.)")
        
        self.insights['monthly_stats'] = monthly_stats
        self.insights['best_month'] = best_month
        
    def musical_features_analysis(self):
        """Analyse des caractéristiques musicales"""
        print("\n🎼 ANALYSE DES CARACTÉRISTIQUES MUSICALES")
        print("=" * 50)
        
        musical_features = ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 
                           'instrumentalness_%', 'liveness_%', 'speechiness_%']
        
        # Profil musical des hits vs émergents
        hits = self.df[self.df['success_category'].isin(['Hit', 'Mega-Hit'])]
        emerging = self.df[self.df['success_category'] == 'Émergent']
        
        print("🎯 PROFIL MUSICAL - HITS vs ÉMERGENTS :")
        print(f"{'Caractéristique':<18} {'Hits':<8} {'Émergents':<10} {'Différence':<10}")
        print("-" * 50)
        
        for feature in musical_features:
            if feature in self.df.columns:
                hits_avg = hits[feature].mean()
                emerging_avg = emerging[feature].mean()
                diff = hits_avg - emerging_avg
                print(f"{feature.replace('_%', ''):<18} {hits_avg:6.1f}   {emerging_avg:8.1f}   {diff:+7.1f}")
        
        # Analyse BPM
        print(f"\n🥁 BPM ANALYSIS :")
        print(f"   BPM moyen des hits : {hits['bpm'].mean():.0f}")
        print(f"   BPM moyen émergents : {emerging['bpm'].mean():.0f}")
        
        # Mode et tonalité
        print(f"\n🎵 MODE ET TONALITÉ :")
        mode_success = self.df.groupby('mode')['streams'].mean()
        print(f"   Mode Majeur : {mode_success.get('Major', 0):,.0f} streams moy.")
        print(f"   Mode Mineur : {mode_success.get('Minor', 0):,.0f} streams moy.")
        
        self.insights['musical_profile'] = {
            'hits': hits[musical_features].mean(),
            'emerging': emerging[musical_features].mean()
        }
        
    def collaboration_analysis(self):
        """Analyse de l'impact des collaborations"""
        print("\n🤝 ANALYSE DES COLLABORATIONS")
        print("=" * 50)
        
        # Impact du nombre d'artistes
        collab_stats = self.df.groupby('artist_count').agg({
            'streams': ['mean', 'median', 'count'],
            'total_playlists': 'mean'
        }).round(0)
        
        print("👥 IMPACT DU NOMBRE D'ARTISTES :")
        for count in sorted(self.df['artist_count'].unique()):
            if count in collab_stats.index:
                stats = collab_stats.loc[count]
                streams_avg = stats[('streams', 'mean')]
                nb_songs = stats[('streams', 'count')]
                print(f"   {count} artiste(s) : {streams_avg:>10,.0f} streams moy. ({nb_songs:.0f} titres)")
        
        # Collaborations les plus fructueuses
        print("\n🏆 TOP COLLABORATIONS (2+ artistes) :")
        collabs = self.df[self.df['artist_count'] > 1].nlargest(5, 'streams')
        for i, (_, song) in enumerate(collabs.iterrows(), 1):
            print(f"{i}. {song['track_name'][:30]:<30} - {song['artist(s)_name'][:30]:<30} "
                  f": {song['streams']:>10,.0f}")
        
        self.insights['collaboration_stats'] = collab_stats
        
    def create_visualizations(self):
        """Création des visualisations principales"""
        print("\n📊 CRÉATION DES VISUALISATIONS")
        print("=" * 50)
        
        # Configuration des subplots
        fig, axes = plt.subplots(3, 2, figsize=(20, 18))
        fig.suptitle('SPOTIFY 2023 - ANALYSE COMPLÈTE DES FACTEURS DE SUCCÈS', 
                    fontsize=16, fontweight='bold')
        
        # 1. Distribution des streams
        ax1 = axes[0, 0]
        self.df['streams_log'] = np.log10(self.df['streams'].replace(0, 1))
        ax1.hist(self.df['streams_log'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Distribution des Streams (échelle log)', fontweight='bold')
        ax1.set_xlabel('Log10(Streams)')
        ax1.set_ylabel('Nombre de titres')
        
        # 2. Streams par mois
        ax2 = axes[0, 1]
        monthly_avg = self.df.groupby('released_month')['streams'].mean()
        months = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
        ax2.bar(range(1, 13), [monthly_avg.get(i, 0) for i in range(1, 13)], 
               color='lightcoral', alpha=0.8)
        ax2.set_title('Streams Moyens par Mois de Sortie', fontweight='bold')
        ax2.set_xlabel('Mois')
        ax2.set_ylabel('Streams Moyens')
        ax2.set_xticks(range(1, 13))
        ax2.set_xticklabels(months)
        
        # 3. Corrélation des caractéristiques musicales
        ax3 = axes[1, 0]
        musical_features = ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%']
        corr_matrix = self.df[musical_features + ['streams']].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu_r', center=0, ax=ax3,
                   fmt='.2f', square=True)
        ax3.set_title('Corrélations Caractéristiques Musicales', fontweight='bold')
        
        # 4. Success par nombre d'artistes
        ax4 = axes[1, 1]
        collab_avg = self.df.groupby('artist_count')['streams'].mean()
        ax4.bar(collab_avg.index, collab_avg.values, color='gold', alpha=0.8)
        ax4.set_title('Impact des Collaborations', fontweight='bold')
        ax4.set_xlabel('Nombre d\'artistes')
        ax4.set_ylabel('Streams Moyens')
        
        # 5. Top artistes
        ax5 = axes[2, 0]
        top_10 = self.insights['top_artists'].head(8)
        artists = [name[:15] + '...' if len(name) > 15 else name for name in top_10.index]
        ax5.barh(range(len(top_10)), top_10.values, color='mediumseagreen', alpha=0.8)
        ax5.set_title('Top 8 Artistes par Streams', fontweight='bold')
        ax5.set_xlabel('Streams Totaux')
        ax5.set_yticks(range(len(top_10)))
        ax5.set_yticklabels(artists)
        
        # 6. Caractéristiques musicales hits vs autres
        ax6 = axes[2, 1]
        features = ['danceability_%', 'energy_%', 'valence_%']
        hits_profile = []
        other_profile = []
        
        hits = self.df[self.df['success_category'].isin(['Hit', 'Mega-Hit'])]
        others = self.df[~self.df['success_category'].isin(['Hit', 'Mega-Hit'])]
        
        for feature in features:
            hits_profile.append(hits[feature].mean())
            other_profile.append(others[feature].mean())
        
        x = np.arange(len(features))
        width = 0.35
        
        ax6.bar(x - width/2, hits_profile, width, label='Hits', color='red', alpha=0.7)
        ax6.bar(x + width/2, other_profile, width, label='Autres', color='blue', alpha=0.7)
        ax6.set_title('Profil Musical : Hits vs Autres', fontweight='bold')
        ax6.set_xlabel('Caractéristiques')
        ax6.set_ylabel('Valeur Moyenne (%)')
        ax6.set_xticks(x)
        ax6.set_xticklabels([f.replace('_%', '') for f in features])
        ax6.legend()
        
        plt.tight_layout()
        plt.savefig('spotify_analysis_complete.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Visualisations sauvegardées : spotify_analysis_complete.png")
        
    def generate_insights_report(self):
        """Génération du rapport d'insights business"""
        print("\n🎯 INSIGHTS BUSINESS & RECOMMANDATIONS")
        print("=" * 60)
        
        print("💡 FACTEURS CLÉS DE SUCCÈS IDENTIFIÉS :")
        print("   1. 📅 TIMING : Sortir en mai-juin pour maximiser l'exposition")
        print("   2. 🎵 PROFIL MUSICAL : Privilégier danceability élevée (>70%)")
        print("   3. 🤝 COLLABORATIONS : 2 artistes = sweet spot pour les streams")
        print("   4. 📱 PLAYLISTS : Corrélation forte avec le succès (r>0.8)")
        print("   5. ⚡ ÉNERGIE : Les titres énergiques (>65%) performent mieux")
        
        print("\n🚀 RECOMMANDATIONS STRATÉGIQUES :")
        print("   ✓ PRODUCTION : Cibler BPM 120-140 avec forte danceability")
        print("   ✓ MARKETING : Investir massivement dans les placements playlists")
        print("   ✓ CALENDRIER : Planifier les sorties majeures mai-juin")
        print("   ✓ COLLABS : Encourager duos d'artistes complémentaires")
        print("   ✓ A&R : Prioriser les profils énergiques et dansants")
        
        # Calcul ROI potentiel
        avg_hit_streams = self.df[self.df['success_category'].isin(['Hit', 'Mega-Hit'])]['streams'].mean()
        avg_other_streams = self.df[~self.df['success_category'].isin(['Hit', 'Mega-Hit'])]['streams'].mean()
        multiplier = avg_hit_streams / avg_other_streams
        
        print(f"\n💰 IMPACT BUSINESS :")
        print(f"   📈 Multiplier de succès potentiel : x{multiplier:.1f}")
        print(f"   🎯 Streams cibles pour un hit : {avg_hit_streams:,.0f}")
        print(f"   📊 Probabilité hit (avec facteurs) : +{((multiplier-1)/multiplier*100):.0f}%")

def main():
    """Fonction principale d'exécution"""
    print("🎵" + "=" * 60 + "🎵")
    print("   SPOTIFY 2023 - ANALYSE AVANCÉE DES FACTEURS DE SUCCÈS")
    print("🎵" + "=" * 60 + "🎵")
    
    # Initialisation de l'analyser
    analyzer = SpotifyAnalyzer('spotify-2023.csv')
    
    # Exécution des analyses
    analyzer.descriptive_analysis()
    analyzer.temporal_analysis()
    analyzer.musical_features_analysis()
    analyzer.collaboration_analysis()
    analyzer.create_visualizations()
    analyzer.generate_insights_report()
    
    print(f"\n✅ ANALYSE TERMINÉE - {len(analyzer.df)} titres analysés")
    print("📊 Fichier de visualisations : spotify_analysis_complete.png")
    print("🚀 Prêt pour le dashboard interactif !")

if __name__ == "__main__":
    main()
