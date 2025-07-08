import random

# Fonction pour jouer un tour
def jouer_tour():
    choix_utilisateur = input("Choisissez pierre, papier ou ciseaux: ").lower()
    choix_ordinateur = random.choice(["pierre", "papier", "ciseaux"])
    
    print(f"Vous avez choisi: {choix_utilisateur}")
    print(f"L'ordinateur a choisi: {choix_ordinateur}")
    
    # Déterminer le gagnant
    if choix_utilisateur == choix_ordinateur:
        print("Égalité!")
    elif (choix_utilisateur == "pierre" and choix_ordinateur == "ciseaux") or \
         (choix_utilisateur == "papier" and choix_ordinateur == "pierre") or \
         (choix_utilisateur == "ciseaux" and choix_ordinateur == "papier"):
        print("Vous avez gagné!")
    else:
        print("Vous avez perdu!")

# Lancer le jeu
def main():
    print("Bienvenue au jeu Pierre-Papier-Ciseaux!")
    jouer_tour()

if __name__ == "__main__":
    main()