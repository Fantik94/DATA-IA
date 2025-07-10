import streamlit as st
import joblib
import numpy as np

# Charger le modèle
model = joblib.load("regression.joblib")

# Titre de l'application
st.title("🏠 Prédicteur de Prix de Maisons")
st.write("Cette application prédit le prix d'une maison basé sur ses caractéristiques.")

# Créer les champs de formulaire
st.header("Caractéristiques de la maison")

# Champ pour la taille
taille = st.number_input(
    "Taille de la maison (m²)",
    min_value=0.0,
    max_value=500.0,
    value=150.0,
    step=1.0,
    help="Entrez la taille de la maison en mètres carrés"
)

# Champ pour le nombre de chambres
nb_chambres = st.number_input(
    "Nombre de chambres",
    min_value=1,
    max_value=10,
    value=2,
    step=1,
    help="Entrez le nombre de chambres"
)

# Champ pour le jardin (checkbox)
jardin = st.checkbox(
    "La maison a-t-elle un jardin ?",
    help="Cochez si la maison possède un jardin"
)

# Convertir le checkbox en valeur numérique (0 ou 1)
jardin_valeur = 1 if jardin else 0

# Bouton pour faire la prédiction
if st.button("🔮 Prédire le prix", type="primary"):
    # Préparer les données pour la prédiction
    features = np.array([[taille, nb_chambres, jardin_valeur]])
    
    # Faire la prédiction
    prediction = model.predict(features)[0]
    
    # Afficher le résultat
    st.success("Prédiction réalisée avec succès !")
    st.write(f"**Prix prédit : {prediction:,.2f} €**")
    
    # Afficher les détails
    st.subheader("Détails de la prédiction")
    st.write(f"- Taille : {taille} m²")
    st.write(f"- Nombre de chambres : {nb_chambres}")
    st.write(f"- Jardin : {'Oui' if jardin else 'Non'}")

# Afficher des informations sur le modèle
st.sidebar.header("ℹ️ Informations sur le modèle")
st.sidebar.write("Ce modèle utilise une régression linéaire pour prédire le prix des maisons.")
st.sidebar.write("Les caractéristiques utilisées sont :")
st.sidebar.write("- Taille (m²)")
st.sidebar.write("- Nombre de chambres")
st.sidebar.write("- Présence d'un jardin") 