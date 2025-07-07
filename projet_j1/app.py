#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APPLICATION SPOTIFY ANALYTICS
==============================
Point d'entrée principal pour le déploiement cloud

Auteur : Expert Data Scientist
Date : 2024
"""

import streamlit as st
import sys
import os

# Ajout du répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration de la page
st.set_page_config(
    page_title="🎵 Spotify Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import et exécution du dashboard premium
try:
    from dashboard_premium import main
    main()
except ImportError as e:
    st.error(f"❌ Erreur d'import : {e}")
    st.info("💡 Assurez-vous que tous les fichiers sont présents dans le répertoire.")
except Exception as e:
    st.error(f"❌ Erreur d'exécution : {e}")
    st.info("💡 Veuillez vérifier la configuration et les dépendances.") 