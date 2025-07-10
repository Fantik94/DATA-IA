import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

def train_tumor_model():
    """Entraîne un modèle pour prédire si une tumeur est cancéreuse"""
    
    # 1. Chargement des données
    print("📊 Chargement des données...")
    df = pd.read_csv('tumor_two_vars.csv')
    print(f"Données chargées: {df.shape}")
    print(f"Colonnes: {df.columns.tolist()}")
    print(f"Répartition des classes: \n{df['is_cancerous'].value_counts()}")
    print()
    
    # Préparation des features et target
    X = df[['size', 'p53_concentration']]
    y = df['is_cancerous']
    
    # 2. Train test split
    print("🔄 Division des données (train/test split)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    print()
    
    # 3. MinMaxScaler sur les données d'entraînement
    print("⚙️ Application du MinMaxScaler...")
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)  # Important: transform, pas fit_transform
    
    print(f"Avant scaling - Train min/max: {X_train.min().min():.6f} / {X_train.max().max():.6f}")
    print(f"Après scaling - Train min/max: {X_train_scaled.min():.6f} / {X_train_scaled.max():.6f}")
    print()
    
    # 4. Entraînement du modèle
    print("🤖 Entraînement du modèle de régression logistique...")
    model = LogisticRegression(random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Évaluation du modèle
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    
    train_accuracy = accuracy_score(y_train, y_pred_train)
    test_accuracy = accuracy_score(y_test, y_pred_test)
    
    print(f"Accuracy sur train: {train_accuracy:.4f}")
    print(f"Accuracy sur test: {test_accuracy:.4f}")
    print()
    
    print("📈 Rapport de classification (test set):")
    print(classification_report(y_test, y_pred_test))
    
    # 5. Sauvegarde du modèle ET du scaler
    print("💾 Sauvegarde du modèle et du scaler...")
    joblib.dump(model, "tumor_model.joblib")
    joblib.dump(scaler, "tumor_scaler.joblib")  # TRÈS IMPORTANT !
    
    print("✅ Modèle sauvegardé dans 'tumor_model.joblib'")
    print("✅ Scaler sauvegardé dans 'tumor_scaler.joblib'")
    print()
    
    # Exemple de prédictions
    print("🔮 Exemples de prédictions:")
    exemples = X_test.head(10)
    exemples_scaled = scaler.transform(exemples)
    predictions = model.predict(exemples_scaled)
    probabilities = model.predict_proba(exemples_scaled)
    
    for i, (idx, row) in enumerate(exemples.iterrows()):
        pred = predictions[i]
        prob = probabilities[i][1]  # Probabilité d'être cancéreux
        real = y_test.iloc[i]
        print(f"Exemple {i+1}: size={row['size']:.6f}, p53={row['p53_concentration']:.6f}")
        print(f"  Prédiction: {'Cancéreux' if pred == 1 else 'Non cancéreux'} (prob: {prob:.3f})")
        print(f"  Réalité: {'Cancéreux' if real == 1 else 'Non cancéreux'}")
        print(f"  ✅ Correct: {'Oui' if pred == real else 'Non'}")
        print()

if __name__ == "__main__":
    train_tumor_model() 