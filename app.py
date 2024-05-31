# import des packages
import pickle # pour lire et utiliser le model
import streamlit as st  # Pour créer l'interface utilisateur
import requests  # Pour faire des requêtes HTTP

# Fonction pour récupérer l'affiche d'un film à partir de l'API de The Movie Database (TMDb)
def fetch_poster(movie_id):
    # URL pour récupérer les détails du film à partir de l'API de TMDb
    url = "https://api.themoviedb.org/3/movie/{}?api_key=0d42ca23b61265745dde50c6866fb862".format(movie_id)
    data = requests.get(url)  # Faire une requête GET à l'API
    data = data.json()  # Convertir la réponse en JSON
    poster_path = data['poster_path']  # Extraire le chemin de l'affiche
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path  # Construire l'URL complète de l'affiche

    return full_path  # Retourner l'URL de l'affiche

# Fonction pour recommander des films similaires à partir d'un film donné
def recommend(movie):
    # Trouver l'index du film dans le DataFrame
    index = movies[movies['title'] == movie].index[0]
    # Calculer les distances de similarité et les trier par ordre décroissant
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)
    recommended_movies_name = []  # Liste pour stocker les noms des films recommandés
    recommended_movies_poster = []  # Liste pour stocker les affiches des films recommandés
    # Parcourir les 5 premiers films similaires
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id  # Récupérer l'ID du film
        recommended_movies_poster.append(fetch_poster(movie_id))  # Ajouter l'affiche à la liste
        recommended_movies_name.append(movies.iloc[i[0]].title)  # Ajouter le titre à la liste
    return recommended_movies_name, recommended_movies_poster  # Retourner les listes des films recommandés et leurs affiches

# Configuration de l'interface utilisateur avec Streamlit
st.header('Systeme de Recommandation de Films')
# Charger les données des films et les similarités à partir des fichiers pickle
movies = pickle.load(open('models/movie_list.pkl', 'rb'))
similarity = pickle.load(open('models/similarite.pkl', 'rb'))

# Liste des titres de films pour le menu déroulant
movie_list = movies['title'].values
# Créer un menu déroulant pour sélectionner un film
selected_movie = st.selectbox(
    'Tape ou selectionne un film pour avoir une recommandation',
    movie_list
)

# Bouton pour générer les recommandations
if st.button('Montrer la recommandation'):
    # Appeler la fonction de recommandation avec le film sélectionné
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    # Créer une disposition en colonnes pour afficher les recommandations
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])  # Afficher le titre du premier film recommandé
        st.image(recommended_movies_poster[0])  # Afficher l'affiche du premier film recommandé

    with col2:
        st.text(recommended_movies_name[1])  # Afficher le titre du deuxième film recommandé
        st.image(recommended_movies_poster[1])  # Afficher l'affiche du deuxième film recommandé

    with col3:
        st.text(recommended_movies_name[2])  # Afficher le titre du troisième film recommandé
        st.image(recommended_movies_poster[2])  # Afficher l'affiche du troisième film recommandé

    with col4:
        st.text(recommended_movies_name[3])  # Afficher le titre du quatrième film recommandé
        st.image(recommended_movies_poster[3])  # Afficher l'affiche du quatrième film recommandé

    with col5:
        st.text(recommended_movies_name[4])  # Afficher le titre du cinquième film recommandé
        st.image(recommended_movies_poster[4])  # Afficher l'affiche du cinquième film recommandé
