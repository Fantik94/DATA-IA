# 🚀 GUIDE DE DÉPLOIEMENT CLOUD

## 📋 Résumé du Problème

Lors du déploiement sur Streamlit Cloud, le fichier `spotify-2023.csv` n'est pas trouvé car il se trouve dans le répertoire racine alors que l'application s'exécute depuis le dossier `projet_j1/`.

## 🔧 Solutions Implémentées

### 1. 📁 Gestion Automatique des Chemins

Le dashboard premium (`dashboard_premium.py`) cherche maintenant automatiquement le fichier CSV dans plusieurs emplacements :

- `spotify-2023.csv` (répertoire courant)
- `projet_j1/spotify-2023.csv` 
- `../spotify-2023.csv` (répertoire parent)
- Répertoire du script
- Répertoire parent du script

### 2. 📤 Upload de Fichier Intégré

Si le fichier n'est pas trouvé, l'application propose :
- Un lien vers le dépôt GitHub
- Un uploader de fichier intégré

### 3. 🎯 Fichiers de Déploiement

**app.py** - Point d'entrée principal pour le cloud
```bash
streamlit run projet_j1/app.py
```

**debug_paths.py** - Script de debug pour vérifier l'environnement
```bash
streamlit run projet_j1/debug_paths.py
```

## 🔍 Déploiement sur Streamlit Cloud

### Option 1 : Utiliser app.py
1. Dans Streamlit Cloud, configurer :
   - **Main file path:** `projet_j1/app.py`
   - **Python version:** 3.9+

### Option 2 : Utiliser dashboard_premium.py directement  
1. Dans Streamlit Cloud, configurer :
   - **Main file path:** `projet_j1/dashboard_premium.py`
   - **Python version:** 3.9+

### Option 3 : Copier le fichier CSV
1. Copier `spotify-2023.csv` dans le dossier `projet_j1/`
2. Utiliser le chemin : `projet_j1/dashboard_premium.py`

## 🛠️ Configuration Cloud

### Variables d'environnement (optionnel)
```
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Secrets Streamlit (si nécessaire)
```toml
[general]
data_source = "github"
```

## 🔄 Workflow de Debug

1. **Exécuter debug_paths.py** pour vérifier l'environnement
2. **Vérifier les logs** de déploiement  
3. **Utiliser l'uploader** si le fichier n'est pas trouvé
4. **Tester en local** avant déploiement

## 📊 Structure Recommandée

```
DATA-IA/
├── spotify-2023.csv          # Fichier de données
├── projet_j1/
│   ├── app.py               # Point d'entrée cloud
│   ├── dashboard_premium.py  # Dashboard principal
│   ├── debug_paths.py       # Script de debug
│   ├── requirements.txt     # Dépendances
│   └── .streamlit/
│       └── config.toml      # Configuration
```

## ✅ Vérifications Finales

- [ ] Fichier CSV accessible
- [ ] Dependencies installées
- [ ] Configuration Streamlit valide
- [ ] Tests en local réussis
- [ ] Logs de déploiement propres

## 🆘 En Cas de Problème

1. **Exécuter debug_paths.py** pour diagnostiquer
2. **Vérifier les logs** de la console cloud
3. **Utiliser l'uploader** comme solution de secours
4. **Contacter le support** Streamlit si nécessaire 