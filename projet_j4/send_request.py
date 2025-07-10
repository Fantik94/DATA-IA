import requests
import json

# URL de base de l'API
BASE_URL = "http://localhost:5000"

def test_api_home():
    """Test de la route de base de l'API"""
    print("=== Test de la route de base ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        
        # Utilisation de la méthode json() pour obtenir le dictionnaire
        data = response.json()
        print(f"Réponse JSON: {data}")
        print(f"Message: {data['message']}")
        print()
        
    except Exception as e:
        print(f"Erreur lors du test de la route de base: {e}")
        print()

def test_predictions_list():
    """Test de la route des prédictions multiples"""
    print("=== Test des prédictions multiples ===")
    try:
        response = requests.get(f"{BASE_URL}/predictions")
        print(f"Status Code: {response.status_code}")
        
        # Utilisation de la méthode json() pour obtenir le dictionnaire
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Nombre de prédictions: {data['total']}")
        
        # Affichage des prédictions
        for i, prediction in enumerate(data['predictions']):
            print(f"Prédiction {i+1}:")
            print(f"  - Taille: {prediction['taille']} m²")
            print(f"  - Nombre de chambres: {prediction['nb_chambres']}")
            print(f"  - Jardin: {'Oui' if prediction['jardin'] else 'Non'}")
            print(f"  - Prix prédit: {prediction['prix_predit']:,.2f} €")
            print()
        
    except Exception as e:
        print(f"Erreur lors du test des prédictions: {e}")
        print()

def test_single_prediction():
    """Test de la prédiction d'une seule maison"""
    print("=== Test de prédiction unique ===")
    
    # Données de test pour une maison
    house_data = {
        "taille": 140,
        "nb_chambres": 3,
        "jardin": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=house_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        
        # Utilisation de la méthode json() pour obtenir le dictionnaire
        data = response.json()
        print(f"Status: {data['status']}")
        
        # Affichage de la prédiction
        prediction = data['prediction']
        print("Prédiction:")
        print(f"  - Taille: {prediction['taille']} m²")
        print(f"  - Nombre de chambres: {prediction['nb_chambres']}")
        print(f"  - Jardin: {'Oui' if prediction['jardin'] else 'Non'}")
        print(f"  - Prix prédit: {prediction['prix_predit']:,.2f} €")
        print()
        
    except Exception as e:
        print(f"Erreur lors de la prédiction unique: {e}")
        print()

def test_multiple_houses():
    """Test avec plusieurs maisons différentes"""
    print("=== Test avec plusieurs maisons personnalisées ===")
    
    # Différentes maisons à tester
    houses_to_test = [
        {"taille": 100, "nb_chambres": 2, "jardin": False},
        {"taille": 250, "nb_chambres": 5, "jardin": True},
        {"taille": 75, "nb_chambres": 1, "jardin": False},
        {"taille": 180, "nb_chambres": 4, "jardin": True}
    ]
    
    for i, house in enumerate(houses_to_test):
        print(f"Test maison {i+1}:")
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=house,
                headers={'Content-Type': 'application/json'}
            )
            
            # Utilisation de la méthode json() pour obtenir le dictionnaire
            data = response.json()
            
            if data['status'] == 'success':
                prediction = data['prediction']
                print(f"  Maison de {prediction['taille']} m², {prediction['nb_chambres']} chambres")
                print(f"  Jardin: {'Oui' if prediction['jardin'] else 'Non'}")
                print(f"  📈 Prix prédit: {prediction['prix_predit']:,.2f} €")
            else:
                print(f"  Erreur: {data['message']}")
                
        except Exception as e:
            print(f"  Erreur: {e}")
        
        print()

if __name__ == "__main__":
    print("🚀 Test de l'API de prédiction de prix de maisons")
    print("=" * 50)
    
    # Lancement de tous les tests
    test_api_home()
    test_predictions_list()
    test_single_prediction()
    test_multiple_houses()
    
    print("✅ Tests terminés!") 