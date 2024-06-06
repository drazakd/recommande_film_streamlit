import streamlit as st
import requests
import mysql.connector
from mysql.connector import Error
import time


# Configuration de la connexion à la base de données MySQL
def get_db_connection():
    try:
        # Connexion à la base de données MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Remplacez par votre nom d'utilisateur MySQL
            password='',  # Remplacez par votre mot de passe MySQL
            database='movie_db2'  # Remplacez par le nom de votre base de données
        )
        return connection
    except Error as e:
        # Affichage d'une erreur si la connexion échoue
        st.error(f"Erreur de connexion à la base de données : {e}")
        return None


# Fonction pour créer les tables nécessaires dans la base de données
def create_tables():
    connection = get_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    # Création de la table 'movies' si elle n'existe pas déjà
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            movie_id INT UNIQUE,
            title VARCHAR(255),
            overview TEXT,
            poster_path VARCHAR(255),
            release_date DATE,
            vote_average FLOAT,
            vote_count INT
        ) ENGINE=InnoDB
    ''')
    connection.commit()
    cursor.close()
    connection.close()


# Fonction pour vérifier le nombre de films dans la base de données
def get_movie_count():
    connection = get_db_connection()
    if connection is None:
        return 0
    cursor = connection.cursor()
    # Requête pour compter le nombre de films dans la table 'movies'
    cursor.execute('SELECT COUNT(*) FROM movies')
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count


# Fonction pour récupérer les 5000 films les plus populaires depuis TMDB et les stocker dans la base de données
def fetch_movies_from_tmdb(progress_bar, status_text):
    API_KEY = '0d42ca23b61265745dde50c6866fb862'  # Remplacez par votre clé API TMDB
    page = 1
    total_movies = get_movie_count()

    # Vérifier si la base de données contient déjà 5000 films
    if total_movies >= 5000:
        status_text.text("La base de données contient déjà 5000 films.")
        return

    connection = get_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()

    # Boucle pour récupérer les films tant que le nombre total de films est inférieur à 5000
    while total_movies < 5000:
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={page}'
        response = requests.get(url)
        data = response.json()
        movies = data['results']

        if not movies:
            break

        for movie in movies:
            if total_movies >= 5000:
                break

            # Récupérer les détails complets de chaque film
            movie_details_url = f'https://api.themoviedb.org/3/movie/{movie["id"]}?api_key={API_KEY}'
            movie_details_response = requests.get(movie_details_url)
            movie_details = movie_details_response.json()

            # Insérer le film dans la base de données
            cursor.execute('''
                INSERT INTO movies (movie_id, title, overview, poster_path, release_date, vote_average, vote_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                title = VALUES(title),
                overview = VALUES(overview),
                poster_path = VALUES(poster_path),
                release_date = VALUES(release_date),
                vote_average = VALUES(vote_average),
                vote_count = VALUES(vote_count)
            ''', (movie_details['id'], movie_details['title'], movie_details['overview'], movie_details['poster_path'],
                  movie_details['release_date'], movie_details['vote_average'], movie_details['vote_count']))
            total_movies += 1
            # Mettre à jour la barre de progression et le texte de statut
            progress = total_movies / 5000
            progress_bar.progress(progress)
            status_text.text(f"Chargement des films : {total_movies} / 5000")

        connection.commit()
        page += 1

    cursor.close()
    connection.close()
    status_text.text("Chargement des films terminé !")


# Créer les tables au démarrage
create_tables()

# Interface Streamlit
st.title("Chargement des Films dans la Base de Données")
st.write("Cliquez sur le bouton ci-dessous pour commencer le chargement des films dans la base de données.")

if st.button('Commencer le chargement'):
    progress_bar = st.progress(0)  # Initialisation de la barre de progression
    status_text = st.empty()  # Initialisation du texte de statut
    fetch_movies_from_tmdb(progress_bar, status_text)  # Appel de la fonction pour charger les films
