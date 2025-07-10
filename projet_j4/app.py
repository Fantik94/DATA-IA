from flask import Flask, jsonify, request
from predict import predict, predict_multiple

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({
        "message": "Bienvenue sur l'API de prédiction de prix de maisons!",
        "status": "API fonctionnelle"
    })

@app.route('/predictions', methods=['GET'])
def get_predictions():
    # Données d'exemple pour les prédictions
    houses_data = [
        {"taille": 150, "nb_chambres": 3, "jardin": True},
        {"taille": 120, "nb_chambres": 2, "jardin": False},
        {"taille": 200, "nb_chambres": 4, "jardin": True},
        {"taille": 80, "nb_chambres": 2, "jardin": False},
        {"taille": 180, "nb_chambres": 3, "jardin": True}
    ]
    
    # Utilisation de la fonction predict du fichier séparé
    predictions = predict_multiple(houses_data)
    
    return jsonify({
        "status": "success",
        "predictions": predictions,
        "total": len(predictions)
    })

@app.route('/predict', methods=['POST'])
def predict_single():
    """Route pour prédire le prix d'une seule maison"""
    try:
        data = request.json
        taille = data.get('taille')
        nb_chambres = data.get('nb_chambres')
        jardin = data.get('jardin', False)
        
        # Validation des données
        if taille is None or nb_chambres is None:
            return jsonify({
                "status": "error",
                "message": "Les paramètres 'taille' et 'nb_chambres' sont requis"
            }), 400
        
        # Prédiction
        prix_predit = predict(taille, nb_chambres, jardin)
        
        return jsonify({
            "status": "success",
            "prediction": {
                "taille": taille,
                "nb_chambres": nb_chambres,
                "jardin": jardin,
                "prix_predit": prix_predit
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erreur lors de la prédiction: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 