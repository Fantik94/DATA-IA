import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import joblib

# URL de l'API
API_URL = "http://localhost:5001"

def get_test_examples():
    """Récupère quelques exemples du test set pour vérifier les prédictions"""
    
    # Recharger les données et refaire le même split pour obtenir les mêmes exemples
    df = pd.read_csv('tumor_two_vars.csv')
    X = df[['size', 'p53_concentration']]
    y = df['is_cancerous']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Prendre 10 exemples du test set
    examples = []
    for i in range(10):
        examples.append({
            'size': float(X_test.iloc[i]['size']),
            'p53_concentration': float(X_test.iloc[i]['p53_concentration']),
            'true_label': int(y_test.iloc[i])
        })
    
    return examples

def test_single_predictions():
    """Test des prédictions individuelles"""
    print("🧪 Test des prédictions individuelles")
    print("=" * 50)
    
    examples = get_test_examples()
    correct_predictions = 0
    
    for i, example in enumerate(examples):
        print(f"\n📋 Exemple {i+1}:")
        print(f"  Size: {example['size']:.6f}")
        print(f"  P53 concentration: {example['p53_concentration']:.6f}")
        print(f"  Vraie étiquette: {'Cancéreux' if example['true_label'] == 1 else 'Non cancéreux'}")
        
        # Envoi de la requête à l'API
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json={
                    'size': example['size'],
                    'p53_concentration': example['p53_concentration']
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                prediction = data['prediction']
                
                print(f"  Prédiction API: {prediction['is_cancerous_text']}")
                print(f"  Probabilité cancéreux: {prediction['probability_cancerous']:.3f}")
                print(f"  Confiance: {prediction['confidence']:.3f}")
                
                # Vérification si la prédiction est correcte
                is_correct = prediction['is_cancerous'] == example['true_label']
                print(f"  ✅ Correct: {'Oui' if is_correct else '❌ NON'}")
                
                if is_correct:
                    correct_predictions += 1
                    
            else:
                print(f"  ❌ Erreur API: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    accuracy = correct_predictions / len(examples)
    print(f"\n📊 Résultats du test:")
    print(f"  Prédictions correctes: {correct_predictions}/{len(examples)}")
    print(f"  Accuracy: {accuracy:.2%}")
    
    return accuracy

def test_batch_predictions():
    """Test des prédictions par lot"""
    print("\n🧪 Test des prédictions par lot")
    print("=" * 50)
    
    examples = get_test_examples()
    
    # Préparer les données pour le batch
    tumors = []
    true_labels = []
    for example in examples:
        tumors.append({
            'size': example['size'],
            'p53_concentration': example['p53_concentration']
        })
        true_labels.append(example['true_label'])
    
    try:
        response = requests.post(
            f"{API_URL}/predict_batch",
            json={'tumors': tumors}
        )
        
        if response.status_code == 200:
            data = response.json()
            predictions = data['predictions']
            
            correct_predictions = 0
            print(f"\n📊 Résultats des {len(predictions)} prédictions:")
            
            for i, (pred, true_label) in enumerate(zip(predictions, true_labels)):
                is_correct = pred['is_cancerous'] == true_label
                status = "✅" if is_correct else "❌"
                
                print(f"  {i+1}. {pred['is_cancerous_text']} (prob: {pred['probability_cancerous']:.3f}) {status}")
                
                if is_correct:
                    correct_predictions += 1
            
            accuracy = correct_predictions / len(predictions)
            print(f"\n  Accuracy batch: {accuracy:.2%}")
            
        else:
            print(f"❌ Erreur API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def compare_with_correct_model():
    """Compare avec les prédictions correctes du modèle"""
    print("\n🔍 Comparaison avec le modèle correct (avec scaler)")
    print("=" * 60)
    
    # Charger le modèle et le scaler
    model = joblib.load("tumor_model.joblib")
    scaler = joblib.load("tumor_scaler.joblib")
    
    examples = get_test_examples()
    
    print("Comparaison API vs Modèle correct:")
    for i, example in enumerate(examples):
        # Prédiction correcte avec scaler
        features = np.array([[example['size'], example['p53_concentration']]])
        features_scaled = scaler.transform(features)
        correct_pred = model.predict(features_scaled)[0]
        correct_prob = model.predict_proba(features_scaled)[0][1]
        
        # Prédiction de l'API
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json={
                    'size': example['size'],
                    'p53_concentration': example['p53_concentration']
                }
            )
            
            if response.status_code == 200:
                api_data = response.json()
                api_pred = api_data['prediction']['is_cancerous']
                api_prob = api_data['prediction']['probability_cancerous']
                
                print(f"\n  Exemple {i+1}:")
                print(f"    Réalité: {'Cancéreux' if example['true_label'] == 1 else 'Non cancéreux'}")
                print(f"    Modèle correct: {'Cancéreux' if correct_pred == 1 else 'Non cancéreux'} (prob: {correct_prob:.3f})")
                print(f"    API: {'Cancéreux' if api_pred == 1 else 'Non cancéreux'} (prob: {api_prob:.3f})")
                print(f"    Même prédiction: {'Oui' if correct_pred == api_pred else '❌ NON'}")
                
        except Exception as e:
            print(f"    ❌ Erreur API: {e}")

if __name__ == "__main__":
    print("🚀 Test de l'API de prédiction de tumeurs")
    print("=" * 60)
    
    # Vérifier que l'API est accessible
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            print("✅ API accessible")
        else:
            print("❌ API non accessible")
            exit(1)
    except:
        print("❌ API non accessible - Assurez-vous qu'elle est lancée sur le port 5001")
        exit(1)
    
    # Lancer les tests
    accuracy = test_single_predictions()
    test_batch_predictions()
    compare_with_correct_model()
    
    print(f"\n🎯 Conclusion:")
    if accuracy < 0.8:
        print("❌ Les prédictions ne sont PAS correctes !")
        print("🔍 Raison probable: L'API n'applique pas le même preprocessing (MinMaxScaler) que lors de l'entraînement.")
    else:
        print("✅ Les prédictions semblent correctes.") 