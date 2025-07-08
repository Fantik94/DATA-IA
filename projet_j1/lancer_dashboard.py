#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPOTIFY ANALYTICS - LANCEUR DE DASHBOARD SIMPLIFIÉ
=================================================
Sélecteur entre le dashboard principal et le lancement en ligne de commande
"""

import subprocess
import sys
import os

def clear_screen():
    """Nettoie l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    """Affiche le menu simplifié"""
    clear_screen()
    print("🎵" + "=" * 60 + "🎵")
    print("       SPOTIFY ANALYTICS 2023 - DASHBOARD SELECTOR")
    print("🎵" + "=" * 60 + "🎵")
    print()
    print("📊 DASHBOARDS DISPONIBLES :")
    print()
    print("1️⃣  Dashboard Principal (Recommandé)")
    print("    └─ Interface complète avec analyses et visualisations")
    print()
    print("2️⃣  Analyse en Ligne de Commande")
    print("    └─ Script d'analyse complet avec visualisations PNG")
    print()
    print("0️⃣  Quitter")
    print()
    print("🎯 Choisissez une option (1-2 ou 0) :")

def run_dashboard(choice):
    """Lance le dashboard sélectionné"""
    if choice == "1":
        print("\n🚀 Lancement du Dashboard Principal...")
        print("📱 Votre navigateur va s'ouvrir automatiquement")
        print("🔗 URL locale : http://localhost:8501")
        print("\n⏳ Chargement en cours...")
        
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard_premium.py"], 
                         check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors du lancement : {e}")
        except KeyboardInterrupt:
            print("\n🛑 Dashboard arrêté par l'utilisateur")
            
    elif choice == "2":
        print("\n🔍 Lancement de l'analyse en ligne de commande...")
        print("📊 Génération des analyses et visualisations...")
        
        try:
            subprocess.run([sys.executable, "spotify-2023.py"], check=True)
            print("\n✅ Analyse terminée !")
            print("📁 Fichier généré : spotify_analysis_complete.png")
            input("\nAppuyez sur Entrée pour revenir au menu...")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'analyse : {e}")
            input("\nAppuyez sur Entrée pour revenir au menu...")
        except KeyboardInterrupt:
            print("\n🛑 Analyse interrompue par l'utilisateur")
            input("\nAppuyez sur Entrée pour revenir au menu...")

def main():
    """Fonction principale"""
    while True:
        show_menu()
        
        try:
            choice = input().strip()
            
            if choice == "0":
                print("\n👋 Au revoir ! Merci d'avoir utilisé Spotify Analytics 2023")
                break
            elif choice in ["1", "2"]:
                run_dashboard(choice)
            else:
                print(f"\n❌ Option '{choice}' non valide. Choisissez 1, 2 ou 0.")
                input("Appuyez sur Entrée pour continuer...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir ! Merci d'avoir utilisé Spotify Analytics 2023")
            break
        except Exception as e:
            print(f"\n❌ Erreur inattendue : {e}")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main() 