from flask import Flask, jsonify, request
import joblib
import numpy as np

app = Flask(__name__)

# Chargement du modèle (ATTENTION: on ne charge PAS le scaler pour l'instant)
model = joblib.load("tumor_model.joblib")

@app.route('/')
def home():
    return jsonify({
        "message": "🏥 API de prédiction de tumeurs cancéreuses",
        "status": "API fonctionnelle",
        "endpoints": {
            "/predict": "POST - Prédire si une tumeur est cancéreuse",
            "/predict_batch": "POST - Prédictions multiples"
        }
    })

@app.route('/predict', methods=['POST'])
def predict_tumor():
    """Prédire si une tumeur est cancéreuse (VERSION INCORRECTE - sans scaler)"""
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
        
        # Prédiction SANS preprocessing (c'est le problème !)
        features = np.array([[size, p53_concentration]])
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        return jsonify({
            "status": "success",
            "prediction": {
                "size": size,
                "p53_concentration": p53_concentration,
                "is_cancerous": int(prediction),
                "is_cancerous_text": "Cancéreux" if prediction == 1 else "Non cancéreux",
                "probability_cancerous": float(probability[1]),
                "confidence": float(max(probability))
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erreur lors de la prédiction: {str(e)}"
        }), 500

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """Prédictions multiples (VERSION INCORRECTE)"""
    try:
        data = request.json
        tumors = data.get('tumors', [])
        
        if not tumors:
            return jsonify({
                "status": "error",
                "message": "Le paramètre 'tumors' est requis et doit être une liste"
            }), 400
        
        predictions = []
        for tumor in tumors:
            size = tumor.get('size')
            p53_concentration = tumor.get('p53_concentration')
            
            if size is None or p53_concentration is None:
                predictions.append({
                    "error": "Paramètres manquants",
                    "tumor": tumor
                })
                continue
            
            # Prédiction SANS preprocessing
            features = np.array([[size, p53_concentration]])
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0]
            
            predictions.append({
                "size": size,
                "p53_concentration": p53_concentration,
                "is_cancerous": int(prediction),
                "is_cancerous_text": "Cancéreux" if prediction == 1 else "Non cancéreux",
                "probability_cancerous": float(probability[1])
            })
        
        return jsonify({
            "status": "success",
            "predictions": predictions,
            "total": len(predictions)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erreur lors des prédictions: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Port différent pour éviter les conflits 