#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE DEBUG - CHEMINS ET FICHIERS
=====================================
Script pour vérifier la structure des fichiers lors du déploiement

Auteur : Expert Data Scientist
Date : 2024
"""

import os
import streamlit as st

def debug_environment():
    """Affiche les informations de debug de l'environnement"""
    
    st.title("🔍 Debug - Environnement et Fichiers")
    
    # Répertoire courant
    current_dir = os.getcwd()
    st.write(f"📁 **Répertoire courant:** `{current_dir}`")
    
    # Répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    st.write(f"📄 **Répertoire du script:** `{script_dir}`")
    
    # Liste des fichiers dans le répertoire courant
    st.subheader("📋 Fichiers dans le répertoire courant:")
    try:
        files = os.listdir(current_dir)
        for file in sorted(files):
            file_path = os.path.join(current_dir, file)
            if os.path.isdir(file_path):
                st.write(f"📁 {file}/")
            else:
                st.write(f"📄 {file}")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du répertoire: {e}")
    
    # Vérification des fichiers importants
    st.subheader("🎯 Vérification des fichiers importants:")
    important_files = [
        'spotify-2023.csv',
        'dashboard_premium.py',
        'requirements.txt',
        '../spotify-2023.csv',
        'projet_j1/spotify-2023.csv'
    ]
    
    for file in important_files:
        if os.path.exists(file):
            st.success(f"✅ {file} - TROUVÉ")
        else:
            st.error(f"❌ {file} - NON TROUVÉ")
    
    # Variables d'environnement Python
    st.subheader("🐍 Informations Python:")
    import sys
    st.write(f"**Version Python:** {sys.version}")
    st.write(f"**Répertoires dans sys.path:**")
    for path in sys.path:
        st.write(f"- `{path}`")

if __name__ == "__main__":
    debug_environment() 