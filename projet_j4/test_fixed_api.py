import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import joblib

# URLs des APIs
BROKEN_API_URL = "http://localhost:5001"  # API sans scaler
FIXED_API_URL = "http://localhost:5002"   # API avec scaler

def get_test_examples():
    """Récupère les mêmes exemples que précédemment"""
    df = pd.read_csv('tumor_two_vars.csv')
    X = df[['size', 'p53_concentration']]
    y = df['is_cancerous']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    examples = []
    for i in range(10):
        examples.append({
            'size': float(X_test.iloc[i]['size']),
            'p53_concentration': float(X_test.iloc[i]['p53_concentration']),
            'true_label': int(y_test.iloc[i])
        })
    
    return examples

def test_api(api_url, api_name):
    """Teste une API et retourne l'accuracy"""
    print(f"\n🧪 Test de {api_name}")
    print("=" * 50)
    
    examples = get_test_examples()
    correct_predictions = 0
    
    for i, example in enumerate(examples):
        try:
            response = requests.post(
                f"{api_url}/predict",
                json={
                    'size': example['size'],
                    'p53_concentration': example['p53_concentration']
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                prediction = data['prediction']
                
                is_correct = prediction['is_cancerous'] == example['true_label']
                status = "✅" if is_correct else "❌"
                
                print(f"  {i+1}. Prédit: {prediction['is_cancerous_text']} | "
                      f"Réel: {'Cancéreux' if example['true_label'] == 1 else 'Non cancéreux'} | "
                      f"Prob: {prediction['probability_cancerous']:.3f} {status}")
                
                if is_correct:
                    correct_predictions += 1
                    
            else:
                print(f"  {i+1}. ❌ Erreur API: {response.status_code}")
                
        except Exception as e:
            print(f"  {i+1}. ❌ Erreur: {e}")
    
    accuracy = correct_predictions / len(examples)
    print(f"\n📊 Résultats {api_name}:")
    print(f"  Prédictions correctes: {correct_predictions}/{len(examples)}")
    print(f"  Accuracy: {accuracy:.0%}")
    
    return accuracy

def compare_apis():
    """Compare les deux APIs côte à côte"""
    print("\n🔍 COMPARAISON CÔTE À CÔTE")
    print("=" * 80)
    
    examples = get_test_examples()
    
    # Tester l'API cassée
    print("Vérification de l'API cassée...")
    try:
        response = requests.get(f"{BROKEN_API_URL}/")
        broken_available = response.status_code == 200
    except:
        broken_available = False
    
    # Tester l'API corrigée
    print("Vérification de l'API corrigée...")
    try:
        response = requests.get(f"{FIXED_API_URL}/")
        fixed_available = response.status_code == 200
    except:
        fixed_available = False
    
    print(f"\nAPI cassée (port 5001): {'✅ Disponible' if broken_available else '❌ Non disponible'}")
    print(f"API corrigée (port 5002): {'✅ Disponible' if fixed_available else '❌ Non disponible'}")
    
    if not fixed_available:
        print("\n❌ L'API corrigée n'est pas accessible. Lancez-la avec: python tumor_api_fixed.py")
        return
    
    print(f"\n{'Ex':>2} | {'Réalité':>12} | {'API Cassée':>12} | {'API Corrigée':>12} | {'Prob Cassée':>10} | {'Prob Corrigée':>12}")
    print("-" * 80)
    
    for i, example in enumerate(examples):
        real_label = "Cancéreux" if example['true_label'] == 1 else "Non cancéreux"
        
        # Test API cassée
        broken_pred = "N/A"
        broken_prob = "N/A"
        if broken_available:
            try:
                response = requests.post(f"{BROKEN_API_URL}/predict", json=example)
                if response.status_code == 200:
                    data = response.json()
                    broken_pred = data['prediction']['is_cancerous_text']
                    broken_prob = f"{data['prediction']['probability_cancerous']:.3f}"
            except:
                pass
        
        # Test API corrigée
        fixed_pred = "N/A"
        fixed_prob = "N/A"
        try:
            response = requests.post(f"{FIXED_API_URL}/predict", json=example)
            if response.status_code == 200:
                data = response.json()
                fixed_pred = data['prediction']['is_cancerous_text']
                fixed_prob = f"{data['prediction']['probability_cancerous']:.3f}"
        except:
            pass
        
        print(f"{i+1:>2} | {real_label:>12} | {broken_pred:>12} | {fixed_pred:>12} | {broken_prob:>10} | {fixed_prob:>12}")

def show_preprocessing_difference():
    """Montre la différence de preprocessing"""
    print("\n📦 DIFFÉRENCE DE PREPROCESSING")
    print("=" * 60)
    
    # Charger le scaler pour montrer la transformation
    scaler = joblib.load("tumor_scaler.joblib")
    
    # Prendre un exemple
    example = {
        'size': 0.015,
        'p53_concentration': 0.003
    }
    
    print(f"Exemple de données d'entrée:")
    print(f"  Size: {example['size']}")
    print(f"  P53 concentration: {example['p53_concentration']}")
    
    # Montrer la transformation
    features_raw = np.array([[example['size'], example['p53_concentration']]])
    features_scaled = scaler.transform(features_raw)
    
    print(f"\nAprès MinMaxScaler:")
    print(f"  Size normalisé: {features_scaled[0][0]:.6f}")
    print(f"  P53 normalisé: {features_scaled[0][1]:.6f}")
    
    # Tester avec l'API corrigée pour voir les valeurs
    try:
        response = requests.post(f"{FIXED_API_URL}/predict", json=example)
        if response.status_code == 200:
            data = response.json()
            pred = data['prediction']
            print(f"\nRéponse de l'API corrigée:")
            print(f"  Données brutes: size={pred['size']}, p53={pred['p53_concentration']}")
            print(f"  Données normalisées: size={pred['size_scaled']:.6f}, p53={pred['p53_scaled']:.6f}")
            print(f"  Prédiction: {pred['is_cancerous_text']} (prob: {pred['probability_cancerous']:.3f})")
    except Exception as e:
        print(f"\n❌ Erreur avec l'API corrigée: {e}")

if __name__ == "__main__":
    print("🚀 TEST COMPARATIF DES APIs - CASSÉE vs CORRIGÉE")
    print("=" * 80)
    
    # Test de l'API corrigée
    fixed_accuracy = test_api(FIXED_API_URL, "API CORRIGÉE (avec scaler)")
    
    # Comparaison côte à côte
    compare_apis()
    
    # Montrer la différence de preprocessing
    show_preprocessing_difference()
    
    print(f"\n🎯 CONCLUSION:")
    print(f"  API corrigée accuracy: {fixed_accuracy:.0%}")
    if fixed_accuracy >= 0.9:
        print("  ✅ Les prédictions sont maintenant CORRECTES !")
        print("  🔑 Raison: L'API applique maintenant le MinMaxScaler avant la prédiction")
    else:
        print("  ❌ Il y a encore un problème...")
    
    print(f"\n📚 LEÇON APPRISE:")
    print("  En production, il est CRUCIAL d'appliquer le même preprocessing")
    print("  qu'en entraînement. Sinon, le modèle reçoit des données dans")
    print("  une échelle différente et fait des prédictions incorrectes.") 