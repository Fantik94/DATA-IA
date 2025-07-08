# Jeu MMO simple en terminal

import random
import time
from colorama import Fore, Back, Style, init

# Initialisation de colorama
init()

# Classes de personnages
class Personnage:
    def __init__(self, nom, classe):
        self.nom = nom
        self.classe = classe
        self.pv = 100
        self.attaque = 10
        self.defense = 5
        self.inventaire = []
        self.equipement = {
            "arme": "Poing",
            "armure": "Vêtements",
            "accessoire": None
        }

    def afficher_stats(self):
        print(f"{Fore.YELLOW}{self.nom} (Classe: {self.classe}){Style.RESET_ALL}")
        print(f"PV: {self.pv}")
        print(f"Attaque: {self.attaque}")
        print(f"Défense: {self.defense}")
        print(f"Équipement: {self.equipement}")

    def attaquer(self, cible):
        degats = max(1, self.attaque - cible.defense // 2)
        cible.pv -= degats
        print(f"{self.nom} attaque {cible.nom} et inflige {degats} dégâts!")

    def loot(self, item):
        self.inventaire.append(item)
        print(f"{self.nom} a récupéré {item}!")

# Création de monstres
class Monstre:
    def __init__(self, nom, pv, attaque, defense, loot):
        self.nom = nom
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.loot = loot

    def attaquer(self, cible):
        degats = max(1, self.attaque - cible.defense // 2)
        cible.pv -= degats
        print(f"{self.nom} attaque {cible.nom} et inflige {degats} dégâts!")

# Création du monde
class Monde:
    def __init__(self):
        self.zones = {
            "forêt": [Monstre("Loup", 30, 8, 3, "Peau de loup"),
                   Monstre("Orc", 50, 12, 5, "Hache rouillée")],
            "désert": [Monstre("Scorpion", 25, 10, 2, "Dard empoisonné"),
                     Monstre("Sphinx", 60, 15, 8, "Épée ancienne")],
            "dungeon": [Monstre("Squelette", 40, 10, 4, "Bouclier en os"),
                      Monstre("Dragon", 100, 20, 10, "Écailles de dragon")]
        }

    def explorer(self, personnage, zone):
        if zone in self.zones:
            print(f"{personnage.nom} explore la {zone}...")
            monstre = random.choice(self.zones[zone])
            print(f"Un {monstre.nom} apparaît!")
            return monstre
        else:
            print(f"{personnage.nom} ne trouve rien d'intéressant dans cette zone.")
            return None

# Fonction principale
def jeu():
    print(f"{Fore.CYAN}Bienvenue dans le jeu MMO en terminal!{Style.RESET_ALL}")
    nom = input("Entrez votre nom: ")
    print("Choisissez votre classe:")
    print("1. Guerrier")
    print("2. Mage")
    print("3. Voleur")
    choix = input("Choix: ")

    if choix == "1":
        classe = "Guerrier"
        personnage = Personnage(nom, classe)
        personnage.attaque = 15
        personnage.defense = 8
    elif choix == "2":
        classe = "Mage"
        personnage = Personnage(nom, classe)
        personnage.attaque = 20
        personnage.defense = 3
    elif choix == "3":
        classe = "Voleur"
        personnage = Personnage(nom, classe)
        personnage.attaque = 12
        personnage.defense = 6
    else:
        print("Classe par défaut: Guerrier")
        personnage = Personnage(nom, "Guerrier")

    monde = Monde()

    while personnage.pv > 0:
        print("\nQue voulez-vous faire?")
        print("1. Explorer une zone")
        print("2. Voir mes stats")
        print("3. Quitter")
        choix = input("Choix: ")

        if choix == "1":
            print("Zones disponibles:")
            print("1. Forêt")
            print("2. Désert")
            print("3. Donjon")
            zone_choix = input("Choix: ")

            if zone_choix == "1":
                zone = "forêt"
            elif zone_choix == "2":
                zone = "désert"
            elif zone_choix == "3":
                zone = "dungeon"
            else:
                print("Zone par défaut: forêt")
                zone = "forêt"

            monstre = monde.explorer(personnage, zone)
            if monstre:
                combat(personnage, monstre)
        elif choix == "2":
            personnage.afficher_stats()
        elif choix == "3":
            print("Au revoir!")
            break
        else:
            print("Choix invalide")

    if personnage.pv <= 0:
        print(f"{Fore.RED}{personnage.nom} est mort... Game Over!{Style.RESET_ALL}")


def combat(personnage, monstre):
    while personnage.pv > 0 and monstre.pv > 0:
        print(f"\n{personnage.nom} (PV: {personnage.pv}) vs {monstre.nom} (PV: {monstre.pv})")
        print("1. Attaquer")
        print("2. Fuir")
        choix = input("Choix: ")

        if choix == "1":
            personnage.attaquer(monstre)
            if monstre.pv <= 0:
                print(f"{monstre.nom} est vaincu!")
                if monstre.loot:
                    personnage.loot(monstre.loot)
                break

            monstre.attaquer(personnage)
            if personnage.pv <= 0:
                print(f"{personnage.nom} est vaincu par {monstre.nom}...")
                break
        elif choix == "2":
            print(f"{personnage.nom} fuit!")
            break
        else:
            print("Choix invalide")

# Lancement du jeu
if __name__ == "__main__":
    jeu()