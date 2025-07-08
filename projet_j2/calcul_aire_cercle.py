import math

# Fonction pour calculer l'aire d'un cercle
def calculer_aire_cercle(rayon):
    return math.pi * rayon ** 2

# Exemple d'utilisation
rayon = 5
aire = calculer_aire_cercle(rayon)
print(f"L'aire du cercle de rayon {rayon} est {aire:.2f}")