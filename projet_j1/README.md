# 🎵 PROJET SPOTIFY 2023 - ANALYSE DES FACTEURS DE SUCCÈS MUSICAL

## 📋 Contexte du Projet

Ce projet d'analyse de données a été réalisé dans le cadre d'un devoir de Data Science. L'objectif est d'analyser le dataset Spotify 2023 pour identifier les facteurs clés de succès dans l'industrie musicale.

**Entreprise fictive** : Maison de disques moderne cherchant à optimiser ses investissements et stratégies marketing.

## 🎯 Problématique

**"Quels sont les facteurs musicaux et temporels qui déterminent le succès d'un titre sur les plateformes de streaming en 2023, et comment peut-on les exploiter pour maximiser les chances de succès commercial ?"**

### Objectifs spécifiques :
- ✅ Identifier les caractéristiques musicales qui prédisent le succès
- ✅ Analyser les tendances temporelles optimales pour les sorties
- ✅ Comprendre l'impact des collaborations d'artistes
- ✅ Optimiser les stratégies de playlist et de promotion

## 📊 Dataset

**Source** : Spotify 2023 - Titres les plus populaires
- **Taille** : 953 titres avec 24 variables
- **Période** : Principalement 2023 avec données historiques
- **Variables clés** :
  - Streams, playlists (Spotify, Apple, Deezer)
  - Caractéristiques musicales (danceability, energy, valence, etc.)
  - Métadonnées (artistes, dates de sortie, BPM, tonalité)

## 🛠️ Technologies Utilisées

- **Python 3.8+**
- **Pandas** - Manipulation de données
- **Matplotlib & Seaborn** - Visualisations statiques
- **Plotly** - Graphiques interactifs
- **Streamlit** - Dashboard web interactif
- **NumPy** - Calculs numériques
- **Scikit-learn** - Analyses statistiques

## 🚀 Installation et Lancement

### 1. Prérequis
```bash
# Vérifier Python
python --version  # Doit être 3.8+

# Cloner le projet (si applicable)
cd projet_j1
```

### 2. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancement de l'analyse principale
```bash
python spotify-2023.py
```

### 4. Lancement des dashboards interactifs

**Option A : Lanceur automatique (recommandé)**
```bash
python lancer_dashboard.py
```

**Option B : Lancement manuel**
```bash
# Dashboard standard
streamlit run dashboard_spotify.py

# Dashboard ultra-interactif (avec donuts et animations)
streamlit run dashboard_interactive.py
```

Les dashboards seront accessibles à l'adresse : `http://localhost:8501`

## 📈 Fonctionnalités

### 🔍 Analyse Principal (spotify-2023.py)
- **Exploration des données** complète avec nettoyage
- **Analyses statistiques** descriptives et corrélationnelles
- **Analyses temporelles** (mois/années optimaux)
- **Profils musicaux** hits vs émergents
- **Impact des collaborations**
- **Visualisations complètes** (6 graphiques principaux)
- **Rapport d'insights** avec recommandations business

### 🎛️ Dashboard Standard (dashboard_spotify.py)
- **Filtres dynamiques** :
  - Années de sortie
  - Catégories de succès
  - Nombre d'artistes
  - Plage de streams
  - Caractéristiques musicales (danceability, energy, valence)

- **5 Onglets d'analyse** :
  1. 📅 **Analyse Temporelle** - Tendances saisonnières et annuelles
  2. 🎼 **Caractéristiques Musicales** - Profils radar et corrélations
  3. 🤝 **Collaborations** - Impact du nombre d'artistes
  4. 📱 **Plateformes** - Performance cross-platform
  5. 🎯 **Insights** - Recommandations + Prédicteur de succès

### 🎯 Dashboard Ultra-Interactif (dashboard_interactive.py)
- **Graphiques en donut animés** avec effets visuels
- **Boutons cliquables** pour comparaisons dynamiques
- **Animations CSS** et effets de survol
- **Prédicteur de succès avancé** avec recommandations personnalisées
- **Sidebar ultra-moderne** avec contrôles gestuels
- **Comparaisons interactives** :
  - 🔥 Hits vs Autres
  - 📅 2023 vs 2022
  - 👥 Solo vs Collaborations
  - 🎵 Majeur vs Mineur
- **Design Spotify-inspired** avec dégradés et ombres
- **KPIs en temps réel** avec métriques comparatives

## 🎯 Principaux Insights Découverts

### 💡 Facteurs Clés de Succès
1. **📅 TIMING** : Sortir en mai-juin maximise l'exposition
2. **🎵 PROFIL MUSICAL** : Danceability élevée (>70%) crucial
3. **🤝 COLLABORATIONS** : 2 artistes = sweet spot optimal
4. **📱 PLAYLISTS** : Corrélation forte avec succès (r>0.8)
5. **⚡ ÉNERGIE** : Titres énergiques (>65%) performent mieux

### 🚀 Recommandations Stratégiques
- ✅ **PRODUCTION** : Cibler BPM 120-140 avec forte danceability
- ✅ **MARKETING** : Investir massivement dans placements playlists
- ✅ **CALENDRIER** : Planifier sorties majeures mai-juin
- ✅ **COLLABS** : Encourager duos d'artistes complémentaires
- ✅ **A&R** : Prioriser profils énergiques et dansants

## 📊 Résultats Quantifiés

- **Multiplier de succès** : x6.8 entre hits et autres catégories
- **ROI playlists** : +1 playlist = +0.8 correlation avec streams
- **Timing optimal** : Mai (+25% streams vs moyenne)
- **Sweet spot collaborations** : 2 artistes (+15% performance)

## 🗂️ Structure du Projet

```
projet_j1/
├── spotify-2023.csv              # Dataset principal
├── spotify-2023.py               # Script d'analyse principal
├── dashboard_spotify.py          # Dashboard Streamlit standard
├── dashboard_interactive.py      # Dashboard ultra-interactif avec donuts
├── lancer_dashboard.py           # Lanceur avec menu de choix
├── requirements.txt              # Dépendances Python
├── README.md                    # Documentation complète
└── spotify_analysis_complete.png # Visualisations générées
```

## 🎨 Aperçu du Dashboard

Le dashboard Streamlit offre une expérience utilisateur moderne avec :
- **Design Spotify-inspired** (vert/noir)
- **Navigation par onglets** intuitive
- **Filtres en sidebar** pour exploration personnalisée
- **Graphiques Plotly** interactifs et responsifs
- **KPIs dynamiques** avec comparaisons
- **Prédicteur de succès** en temps réel

## 🔧 Personnalisation

### Ajouter de nouvelles analyses
1. Modifier `SpotifyAnalyzer` dans `spotify-2023.py`
2. Ajouter de nouvelles fonctions d'analyse
3. Créer onglets correspondants dans le dashboard

### Modifier les filtres
1. Éditer `create_sidebar_filters()` dans `dashboard_spotify.py`
2. Ajuster `apply_filters()` en conséquence

## 📝 Notes Techniques

- **Gestion d'encodage** automatique (UTF-8/Latin-1)
- **Nettoyage robuste** des données numériques avec virgules
- **Cache Streamlit** pour performance optimale
- **Responsive design** adaptatif toutes tailles d'écran
- **Échantillonnage intelligent** pour graphiques lourds

## 🎵 Conclusion

Ce projet démontre une approche complète d'analyse de données appliquée à l'industrie musicale, combinant :
- **Rigueur statistique** et validation des hypothèses
- **Visualisations impactantes** pour communication business
- **Interface interactive** pour exploration autonome
- **Recommandations actionables** basées sur les données

Les insights générés peuvent directement informer les décisions stratégiques d'une maison de disques moderne dans l'écosystème streaming actuel.

---

**Auteurs** : RINGLER Baptiste, RAUNIER Damien  
**Date** : 2025 
**Technologies** : Python, Streamlit, Plotly, Pandas 