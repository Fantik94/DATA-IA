import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import joblib

def demonstrate_problem():
    """Démontre le problème des prédictions incorrectes sans le bon preprocessing"""
    
    print("🧪 DÉMONSTRATION DU PROBLÈME DE PREPROCESSING")
    print("=" * 60)
    
    # 1. Charger les données et faire le même split
    df = pd.read_csv('tumor_two_vars.csv')
    X = df[['size', 'p53_concentration']]
    y = df['is_cancerous']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 2. Charger le modèle et le scaler
    model = joblib.load("tumor_model.joblib")
    scaler = joblib.load("tumor_scaler.joblib")
    
    print("📊 Test sur 10 exemples du test set:")
    print()
    
    correct_predictions = 0
    incorrect_predictions = 0
    
    for i in range(10):
        size = X_test.iloc[i]['size']
        p53_conc = X_test.iloc[i]['p53_concentration']
        true_label = y_test.iloc[i]
        
        print(f"🔬 Exemple {i+1}:")
        print(f"  Size: {size:.6f}")
        print(f"  P53 concentration: {p53_conc:.6f}")
        print(f"  Vraie étiquette: {'Cancéreux' if true_label == 1 else 'Non cancéreux'}")
        
        # PRÉDICTION CORRECTE (avec scaler)
        features_scaled = scaler.transform([[size, p53_conc]])
        correct_pred = model.predict(features_scaled)[0]
        correct_prob = model.predict_proba(features_scaled)[0]
        
        # PRÉDICTION INCORRECTE (sans scaler - comme l'API défaillante)
        features_raw = np.array([[size, p53_conc]])
        incorrect_pred = model.predict(features_raw)[0]
        incorrect_prob = model.predict_proba(features_raw)[0]
        
        print(f"  ✅ Prédiction CORRECTE (avec scaler): {'Cancéreux' if correct_pred == 1 else 'Non cancéreux'} (prob: {correct_prob[1]:.3f})")
        print(f"  ❌ Prédiction INCORRECTE (sans scaler): {'Cancéreux' if incorrect_pred == 1 else 'Non cancéreux'} (prob: {incorrect_prob[1]:.3f})")
        
        correct_match = correct_pred == true_label
        incorrect_match = incorrect_pred == true_label
        
        print(f"  🎯 Correct avec scaler: {'✅ OUI' if correct_match else '❌ NON'}")
        print(f"  🎯 Correct sans scaler: {'✅ OUI' if incorrect_match else '❌ NON'}")
        
        if correct_match:
            correct_predictions += 1
        if incorrect_match:
            incorrect_predictions += 1
            
        print()
    
    print("📈 RÉSULTATS FINAUX:")
    print(f"  Accuracy AVEC scaler (correct): {correct_predictions}/10 = {correct_predictions/10:.0%}")
    print(f"  Accuracy SANS scaler (incorrect): {incorrect_predictions}/10 = {incorrect_predictions/10:.0%}")
    print()
    
    print("🔍 EXPLICATION DU PROBLÈME:")
    print("  ❌ Le modèle a été entraîné sur des données normalisées avec MinMaxScaler")
    print("  ❌ Si on lui donne des données non-normalisées, les prédictions sont fausses")
    print("  ✅ Il FAUT appliquer le même preprocessing (scaler) en production")
    print()
    
    print("📦 DONNÉES AVANT/APRÈS SCALING:")
    # Montrer la différence d'échelle
    sample = X_test.head(3)
    sample_scaled = scaler.transform(sample)
    
    print("  Données originales:")
    for i, (idx, row) in enumerate(sample.iterrows()):
        print(f"    Exemple {i+1}: size={row['size']:.6f}, p53={row['p53_concentration']:.6f}")
    
    print("  Données après MinMaxScaler:")
    for i in range(len(sample_scaled)):
        print(f"    Exemple {i+1}: size={sample_scaled[i][0]:.6f}, p53={sample_scaled[i][1]:.6f}")

if __name__ == "__main__":
    demonstrate_problem() 