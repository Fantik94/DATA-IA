from flask import Flask, jsonify, request
import joblib
import numpy as np

app = Flask(__name__)

# Chargement du modèle ET du scaler (CORRECTION !)
model = joblib.load("tumor_model.joblib")
scaler = joblib.load("tumor_scaler.joblib")  # ✅ Maintenant on charge le scaler !

@app.route('/')
def home():
    return jsonify({
        "message": "🏥 API de prédiction de tumeurs cancéreuses (VERSION CORRIGÉE)",
        "status": "API fonctionnelle avec preprocessing correct",
        "preprocessing": "MinMaxScaler appliqué avant prédiction",
        "endpoints": {
            "/predict": "POST - Prédire si une tumeur est cancéreuse",
            "/predict_batch": "POST - Prédictions multiples"
        }
    })

@app.route('/predict', methods=['POST'])
def predict_tumor():
    """Prédire si une tumeur est cancéreuse (VERSION CORRIGÉE - avec scaler)"""
    try:
        data = request.json
        size = data.get('size')
        p53_concentration = data.get('p53_concentration')
        
        # Validation des données
        if size is None or p53_concentration is None:
            return jsonify({
                "status": "error",
                "message": "Les paramètres 'size' et 'p53_concentration' sont requis"
            }), 400
        
        # ✅ CORRECTION: Appliquer le preprocessing (scaler) AVANT la prédiction
        features_raw = np.array([[size, p53_concentration]])
        features_scaled = scaler.transform(features_raw)  # 🔑 ÉTAPE CRUCIALE !
        
        # Prédiction avec les données normalisées
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        return jsonify({
            "status": "success",
            "prediction": {
                "size": size,
                "p53_concentration": p53_concentration,
                "size_scaled": float(features_scaled[0][0]),  # Montrer la donnée transformée
                "p53_scaled": float(features_scaled[0][1]),   # Montrer la donnée transformée
                "is_cancerous": int(prediction),
                "is_cancerous_text": "Cancéreux" if prediction == 1 else "Non cancéreux",
                "probability_cancerous": float(probability[1]),
                "confidence": float(max(probability)),
                "preprocessing_applied": "MinMaxScaler"
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erreur lors de la prédiction: {str(e)}"
        }), 500

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """Prédictions multiples (VERSION CORRIGÉE)"""
    try:
        data = request.json
        tumors = data.get('tumors', [])
        
        if not tumors:
            return jsonify({
                "status": "error",
                "message": "Le paramètre 'tumors' est requis et doit être une liste"
            }), 400
        
        predictions = []
        
        # Préparer toutes les features pour un scaling en lot (plus efficace)
        features_list = []
        for tumor in tumors:
            size = tumor.get('size')
            p53_concentration = tumor.get('p53_concentration')
            
            if size is None or p53_concentration is None:
                predictions.append({
                    "error": "Paramètres manquants",
                    "tumor": tumor
                })
                features_list.append(None)
                continue
            
            features_list.append([size, p53_concentration])
        
        # Filtrer les features valides et appliquer le scaler
        valid_features = [f for f in features_list if f is not None]
        if valid_features:
            features_array = np.array(valid_features)
            features_scaled = scaler.transform(features_array)  # ✅ Scaling en lot
            
            # Faire les prédictions
            predictions_array = model.predict(features_scaled)
            probabilities_array = model.predict_proba(features_scaled)
            
            # Associer les résultats
            valid_idx = 0
            for i, (tumor, features) in enumerate(zip(tumors, features_list)):
                if features is None:
                    continue  # Déjà ajouté l'erreur
                
                prediction = predictions_array[valid_idx]
                probability = probabilities_array[valid_idx]
                
                predictions.append({
                    "size": tumor['size'],
                    "p53_concentration": tumor['p53_concentration'],
                    "is_cancerous": int(prediction),
                    "is_cancerous_text": "Cancéreux" if prediction == 1 else "Non cancéreux",
                    "probability_cancerous": float(probability[1]),
                    "preprocessing_applied": "MinMaxScaler"
                })
                
                valid_idx += 1
        
        return jsonify({
            "status": "success",
            "predictions": predictions,
            "total": len(predictions),
            "preprocessing": "MinMaxScaler appliqué sur tous les échantillons"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erreur lors des prédictions: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Vérification de la santé de l'API avec test de prédiction"""
    try:
        # Test simple avec des données connues
        test_features = np.array([[0.01, 0.002]])
        test_scaled = scaler.transform(test_features)
        test_prediction = model.predict(test_scaled)[0]
        
        return jsonify({
            "status": "healthy",
            "model_loaded": True,
            "scaler_loaded": True,
            "test_prediction": int(test_prediction),
            "preprocessing_working": True
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Problème de santé: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("🚀 Démarrage de l'API corrigée avec preprocessing MinMaxScaler")
    print("📊 Modèle chargé:", "tumor_model.joblib")
    print("⚙️ Scaler chargé:", "tumor_scaler.joblib")
    app.run(debug=True, host='0.0.0.0', port=5002)  # Port 5002 pour la version corrigée 