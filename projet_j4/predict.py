def predict(taille, nb_chambres, jardin):
    """
    Fonction de prédiction codée en dur pour le prix d'une maison
    
    Args:
        taille (float): Taille de la maison en m²
        nb_chambres (int): Nombre de chambres
        jardin (bool): Présence d'un jardin
    
    Returns:
        float: Prix prédit en euros
    """
    # Prédiction codée en dur basée sur des règles simples
    prix_base = 100000  # Prix de base
    prix_par_m2 = 1200  # Prix par m²
    bonus_chambre = 15000  # Bonus par chambre
    bonus_jardin = 25000  # Bonus si jardin
    
    prix_predit = prix_base + (taille * prix_par_m2) + (nb_chambres * bonus_chambre)
    
    if jardin:
        prix_predit += bonus_jardin
    
    return round(prix_predit, 2)

def predict_multiple(houses_data):
    """
    Fonction pour prédire les prix de plusieurs maisons
    
    Args:
        houses_data (list): Liste de dictionnaires contenant les caractéristiques des maisons
    
    Returns:
        list: Liste des prédictions
    """
    predictions = []
    for house in houses_data:
        prix = predict(house['taille'], house['nb_chambres'], house['jardin'])
        prediction = {
            "taille": house['taille'],
            "nb_chambres": house['nb_chambres'],
            "jardin": house['jardin'],
            "prix_predit": prix
        }
        predictions.append(prediction)
    
    return predictions 