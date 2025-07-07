#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANCEUR DE DASHBOARD SPOTIFY 2023
=================================
Script pour choisir et lancer le dashboard souhaité

Auteur : Expert Data Scientist  
Date : 2024
"""

import os
import subprocess
import sys

def clear_screen():
    """Nettoie l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    """Affiche le menu des dashboards"""
    clear_screen()
    print("🎵" + "=" * 60 + "🎵")
    print("         SPOTIFY 2023 - SÉLECTEUR DE DASHBOARD")
    print("🎵" + "=" * 60 + "🎵")
    print()
    print("Choisissez votre dashboard :")
    print()
    print("1. 📊 Dashboard Standard")
    print("   • Analyse complète des données")
    print("   • Graphiques interactifs")
    print("   • Filtres dynamiques")
    print()
    print("2. 🚀 Dashboard Ultra-Interactif")  
    print("   • Boutons cliquables")
    print("   • Comparaisons dynamiques")
    print("   • Animations CSS")
    print("   • Design Spotify-inspired")
    print()
    print("3. 💎 Dashboard Premium")
    print("   • Charte graphique cohérente")
    print("   • Top 10 des artistes/titres")
    print("   • Design professionnel unifié")
    print("   • Palette Spotify exclusive")
    print()
    print("4. 📈 Analyse Python (script)")
    print("   • Analyses statistiques complètes")
    print("   • Visualisations matplotlib")
    print("   • Insights business")
    print()
    print("0. ❌ Quitter")
    print()
    print("=" * 66)

def launch_dashboard(choice):
    """Lance le dashboard sélectionné"""
    if choice == "1":
        print("🚀 Lancement du Dashboard Standard...")
        print("📍 URL : http://localhost:8501")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard_spotify.py"])
        
    elif choice == "2":
        print("🚀 Lancement du Dashboard Ultra-Interactif...")
        print("📍 URL : http://localhost:8501")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard_interactive.py"])
        
    elif choice == "3":
        print("🚀 Lancement du Dashboard Premium...")
        print("📍 URL : http://localhost:8501")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard_premium.py"])
        
    elif choice == "4":
        print("🚀 Exécution de l'analyse Python...")
        subprocess.run([sys.executable, "spotify-2023.py"])
        input("\n✅ Analyse terminée. Appuyez sur Entrée pour continuer...")
        
    elif choice == "0":
        print("👋 Au revoir !")
        sys.exit(0)
        
    else:
        print("❌ Choix invalide !")
        input("Appuyez sur Entrée pour continuer...")

def check_files():
    """Vérifie la présence des fichiers nécessaires"""
    required_files = [
        "spotify-2023.csv",
        "dashboard_spotify.py", 
        "dashboard_interactive.py",
        "dashboard_premium.py",
        "spotify-2023.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("⚠️ Fichiers manquants :")
        for file in missing_files:
            print(f"   • {file}")
        print("\nVeuillez vous assurer que tous les fichiers sont présents.")
        input("Appuyez sur Entrée pour continuer...")
        return False
    return True

def main():
    """Fonction principale"""
    if not check_files():
        return
    
    while True:
        show_menu()
        choice = input("👉 Votre choix (0-4) : ").strip()
        
        if choice in ["0", "1", "2", "3", "4"]:
            launch_dashboard(choice)
        else:
            print("❌ Veuillez entrer un nombre entre 0 et 4.")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interruption par l'utilisateur. Au revoir !")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        input("Appuyez sur Entrée pour quitter...") 