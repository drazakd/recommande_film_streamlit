import streamlit as st  # Import de Streamlit pour créer l'interface utilisateur
import mysql.connector  # Import de mysql.connector pour interagir avec la base de données MySQL
import pandas as pd  # Import de pandas pour manipuler les données sous forme de DataFrame
from sklearn.metrics.pairwise import \
    cosine_similarity  # Import de cosine_similarity pour calculer la similarité entre les films
import pickle  # Import de pickle pour charger les modèles de similarité précédemment sauvegardés


# Configuration de la connexion à la base de données MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  # Nom d'hôte de la base de données
        user='root',  # Nom d'utilisateur de la base de données
        password='',  # Mot de passe de la base de données
        database='movie_db2'  # Nom de la base de données
    )
    return connection  # Retourne l'objet connexion


# Fonction pour récupérer les films depuis la base de données
def get_movies():
    connection = get_db_connection()  # Obtenir une connexion à la base de données
    cursor = connection.cursor(dictionary=True)  # Créer un curseur avec le mode dictionnaire
    cursor.execute('SELECT * FROM movies')  # Exécuter la commande SQL pour obtenir tous les films
    movies = cursor.fetchall()  # Récupérer tous les films
    cursor.close()  # Fermer le curseur
    connection.close()  # Fermer la connexion
    return pd.DataFrame(movies)  # Retourner les films sous forme de DataFrame pandas


# Fonction pour recommander des films basés sur la similarité
def recommend(movie_title, movies, similarity):
    if movie_title not in movies['title'].values:
        st.error("Le film sélectionné n'existe pas dans la base de données.")
        return [], []

    index = movies[movies['title'] == movie_title].index[0]  # Trouver l'index du film sélectionné
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1],
                       reverse=True)  # Calculer les distances et trier

    recommended_movies_name = []  # Liste pour les noms des films recommandés
    recommended_movies_poster = []  # Liste pour les posters des films recommandés

    for i in distances[1:6]:  # Pour les 5 films les plus similaires
        if i[0] < len(movies):
            movie = movies.iloc[i[0]]  # Obtenir les détails du film
            recommended_movies_poster.append(movie['poster_path'])  # Ajouter le chemin du poster à la liste
            recommended_movies_name.append(movie['title'])  # Ajouter le titre à la liste

    return recommended_movies_name, recommended_movies_poster  # Retourner les recommandations


# Charger les films depuis la base de données
movies = get_movies()  # Récupérer les films depuis la base de données
similarity = pickle.load(open('models/similarite.pkl', 'rb'))  # Charger le modèle de similarité

# Interface utilisateur Streamlit
st.header('Système de Recommandation de Films')  # Titre de l'application

# Ajouter une bannière en haut de l'application
st.image("assets/banner.jpg", use_column_width=True)

movie_list = movies['title'].values  # Obtenir la liste des titres de films

# Widget de sélection de film
selected_movie = st.selectbox(
    'Tape ou sélectionne un film pour avoir une recommandation',
    movie_list
)

# Bouton pour afficher les recommandations
if st.button('Montrer la recommandation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie, movies,
                                                                   similarity)  # Obtenir les recommandations
    if recommended_movies_name:
        cols = st.columns(5)  # Créer 5 colonnes pour afficher les recommandations
        for col, name, poster in zip(cols, recommended_movies_name,
                                     recommended_movies_poster):  # Pour chaque recommandation
            with col:  # Ajouter le texte et l'image dans la colonne correspondante
                st.text(name)
                st.image(f"https://image.tmdb.org/t/p/w500/{poster}")



# etape 3 trop lente et ralentit mon systeme donc j'ai divisé la partie chargement du systeme

# import streamlit as st  # Import de Streamlit pour créer l'interface utilisateur
# import requests  # Import de requests pour faire des requêtes HTTP
# import mysql.connector  # Import de mysql.connector pour interagir avec la base de données MySQL
# import pandas as pd  # Import de pandas pour manipuler les données sous forme de DataFrame
# from sklearn.metrics.pairwise import cosine_similarity  # Import de cosine_similarity pour calculer la similarité entre les films
# import pickle  # Import de pickle pour charger les modèles de similarité précédemment sauvegardés
#
# # Configuration de la connexion à la base de données MySQL
# def get_db_connection():
#     connection = mysql.connector.connect(
#         host='localhost',  # Nom d'hôte de la base de données
#         user='root',  # Nom d'utilisateur de la base de données
#         password='',  # Mot de passe de la base de données
#         database='movie_db2'  # Nom de la base de données
#     )
#     return connection  # Retourne l'objet connexion
#
# # Fonction pour créer les tables nécessaires dans la base de données
# def create_tables():
#     connection = get_db_connection()  # Obtenir une connexion à la base de données
#     cursor = connection.cursor()  # Créer un curseur pour exécuter les commandes SQL
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS movies (
#             id INT AUTO_INCREMENT PRIMARY KEY,  # Clé primaire avec auto-incrémentation
#             movie_id INT UNIQUE,  # ID unique du film (provenant de TMDB)
#             title VARCHAR(255),  # Titre du film
#             overview TEXT,  # Description du film
#             poster_path VARCHAR(255),  # Chemin du poster du film
#             release_date DATE,  # Date de sortie du film
#             vote_average FLOAT,  # Note moyenne du film
#             vote_count INT  # Nombre de votes du film
#         ) ENGINE=InnoDB
#     ''')
#     connection.commit()  # Valider la transaction
#     cursor.close()  # Fermer le curseur
#     connection.close()  # Fermer la connexion
#
# # Fonction pour vérifier le nombre de films dans la base de données
# def get_movie_count():
#     connection = get_db_connection()  # Obtenir une connexion à la base de données
#     cursor = connection.cursor()  # Créer un curseur pour exécuter les commandes SQL
#     cursor.execute('SELECT COUNT(*) FROM movies')  # Exécuter la commande SQL pour obtenir le nombre de films
#     count = cursor.fetchone()[0]  # Récupérer le résultat
#     cursor.close()  # Fermer le curseur
#     connection.close()  # Fermer la connexion
#     return count  # Retourner le nombre de films
#
# # Fonction pour récupérer les 5000 films les plus populaires depuis TMDB et les stocker dans la base de données
# def fetch_movies_from_tmdb():
#     API_KEY = '0d42ca23b61265745dde50c6866fb862'  # Clé API pour accéder à TMDB
#     page = 1  # Commencer à la première page
#     total_movies = get_movie_count()  # Obtenir le nombre de films actuels dans la base de données
#
#     if total_movies >= 5000:  # Si le nombre de films est déjà supérieur ou égal à 5000
#         return  # Ne rien faire
#
#     connection = get_db_connection()  # Obtenir une connexion à la base de données
#     cursor = connection.cursor()  # Créer un curseur pour exécuter les commandes SQL
#
#     while total_movies < 5000:
#         url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={page}'  # URL pour obtenir les films populaires paginés
#         response = requests.get(url)  # Faire une requête GET à l'URL
#         data = response.json()  # Convertir la réponse en JSON
#         movies = data['results']  # Extraire les résultats de la réponse JSON
#
#         if not movies:  # Arrêter si aucun film n'est retourné
#             break
#
#         for movie in movies:  # Pour chaque film dans les résultats
#             if total_movies >= 5000:  # Arrêter si le nombre maximum de films est atteint
#                 break
#
#             movie_details_url = f'https://api.themoviedb.org/3/movie/{movie["id"]}?api_key={API_KEY}'  # URL pour obtenir les détails complets du film
#             movie_details_response = requests.get(movie_details_url)  # Faire une requête GET pour les détails du film
#             movie_details = movie_details_response.json()  # Convertir la réponse en JSON
#
#             cursor.execute('''
#                 INSERT INTO movies (movie_id, title, overview, poster_path, release_date, vote_average, vote_count)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)
#                 ON DUPLICATE KEY UPDATE
#                 title = VALUES(title),
#                 overview = VALUES(overview),
#                 poster_path = VALUES(poster_path),
#                 release_date = VALUES(release_date),
#                 vote_average = VALUES(vote_average),
#                 vote_count = VALUES(vote_count)
#             ''', (movie_details['id'], movie_details['title'], movie_details['overview'], movie_details['poster_path'],
#                   movie_details['release_date'], movie_details['vote_average'], movie_details['vote_count']))  # Insérer ou mettre à jour les films
#             total_movies += 1  # Incrémenter le compteur de films
#
#         connection.commit()  # Valider la transaction
#         page += 1  # Passer à la page suivante
#
#     cursor.close()  # Fermer le curseur
#     connection.close()  # Fermer la connexion
#
# # Fonction pour récupérer les films depuis la base de données
# def get_movies():
#     connection = get_db_connection()  # Obtenir une connexion à la base de données
#     cursor = connection.cursor(dictionary=True)  # Créer un curseur avec le mode dictionnaire
#     cursor.execute('SELECT * FROM movies')  # Exécuter la commande SQL pour obtenir tous les films
#     movies = cursor.fetchall()  # Récupérer tous les films
#     cursor.close()  # Fermer le curseur
#     connection.close()  # Fermer la connexion
#     return pd.DataFrame(movies)  # Retourner les films sous forme de DataFrame pandas
#
# # Fonction pour obtenir l'URL du poster d'un film
# def fetch_poster(movie_id):
#     API_KEY = '0d42ca23b61265745dde50c6866fb862'  # Clé API pour accéder à TMDB
#     url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}'  # URL pour obtenir les détails du film
#     data = requests.get(url).json()  # Faire une requête GET à l'URL et convertir la réponse en JSON
#     poster_path = data.get('poster_path', '')  # Obtenir le chemin du poster
#     full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""  # Construire l'URL complète du poster
#     return full_path  # Retourner l'URL complète du poster
#
# # Fonction pour recommander des films basés sur la similarité
# def recommend(movie_title):
#     movies = get_movies()  # Récupérer les films depuis la base de données
#     index = movies[movies['title'] == movie_title].index[0]  # Trouver l'index du film sélectionné
#     similarity = pickle.load(open('models/similarite.pkl', 'rb'))  # Charger le modèle de similarité
#     distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)  # Calculer les distances et trier
#
#     recommended_movies_name = []  # Liste pour les noms des films recommandés
#     recommended_movies_poster = []  # Liste pour les posters des films recommandés
#
#     for i in distances[1:6]:  # Pour les 5 films les plus similaires
#         movie = movies.iloc[i[0]]  # Obtenir les détails du film
#         recommended_movies_poster.append(fetch_poster(movie['movie_id']))  # Ajouter le poster à la liste
#         recommended_movies_name.append(movie['title'])  # Ajouter le titre à la liste
#
#     return recommended_movies_name, recommended_movies_poster  # Retourner les recommandations
#
# # Créer les tables au démarrage de l'application
# create_tables()
#
# # Récupérer les films depuis TMDB et les stocker dans la base de données si le nombre est inférieur à 5000
# if get_movie_count() < 5000:
#     fetch_movies_from_tmdb()
#
# # Interface utilisateur Streamlit
# st.header('Système de Recommandation de Films')  # Titre de l'application
#
# movies = get_movies()  # Récupérer les films depuis la base de données
# movie_list = movies['title'].values  # Obtenir la liste des titres de films
#
# # Widget de sélection de film
# selected_movie = st.selectbox(
#     'Tape ou sélectionne un film pour avoir une recommandation',
#     movie_list
# )
#
# # Bouton pour afficher les recommandations
# if st.button('Montrer la recommandation'):
#     recommended_movies_name, recommended_movies_poster = recommend(selected_movie)  # Obtenir les recommandations
#     cols = st.columns(5)  # Créer 5 colonnes pour afficher les recommandations
#     for col, name, poster in zip(cols, recommended_movies_name, recommended_movies_poster):  # Pour chaque recommandation
#         with col:  # Ajouter le texte et l'image dans la colonne correspondante
#             st.text(name)
#             st.image(poster)









# etape 2 marche mais les jeux de donnée recupéré depasse largement le jeu de donnée prie pour l'entrainement du modele et ne correspond pas vraiment aux valeurs souhaité

# import streamlit as st  # Import de Streamlit pour créer l'interface utilisateur
# import requests  # Import de requests pour faire des requêtes HTTP
# import mysql.connector  # Import de mysql.connector pour interagir avec la base de données MySQL
# import pandas as pd  # Import de pandas pour manipuler les données sous forme de DataFrame
# from sklearn.metrics.pairwise import cosine_similarity  # Import de cosine_similarity pour calculer la similarité entre les films
# import pickle  # Import de pickle pour charger les modèles de similarité précédemment sauvegardés
#
# # Configuration de la connexion à la base de données MySQL
# def get_db_connection():
#     connection = mysql.connector.connect(
#         host='localhost',  # Nom d'hôte de la base de données
#         user='root',  # Nom d'utilisateur de la base de données
#         password='',  # Mot de passe de la base de données
#         database='movie_db'  # Nom de la base de données
#     )
#     return connection  # Retourne l'objet connexion
#
# # Fonction pour créer les tables nécessaires dans la base de données
# def create_tables():
#     connection = get_db_connection()  # Obtenir une connexion à la base de données
#     cursor = connection.cursor()  # Créer un curseur pour exécuter les commandes SQL
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS movies (
#             id INT AUTO_INCREMENT PRIMARY KEY,  # Clé primaire avec auto-incrémentation
#             movie_id INT UNIQUE,  # ID unique du film (provenant de TMDB)
#             title VARCHAR(255),  # Titre du film
#             overview TEXT,  # Description du film
#             poster_path VARCHAR(255)  # Chemin du poster du film
#         ) ENGINE=InnoDB
#     ''')
#     connection.commit()  # Valider la transaction
#     cursor.close()  # Fermer le curseur
#     connection.close()  # Fermer la connexion
#
# # Fonction pour vérifier le nombre de films dans la base de données
# def get_movie_count():
#     connection = get_db_connection()  # Obtenir une connexion à la base de données
#     cursor = connection.cursor()  # Créer un curseur pour exécuter les commandes SQL
#     cursor.execute('SELECT COUNT(*) FROM movies')  # Exécuter la commande SQL pour obtenir le nombre de films
#     count = cursor.fetchone()[0]  # Récupérer le résultat
#     cursor.close()  # Fermer le curseur
#     connection.close()  # Fermer la connexion
#     return count  # Retourner le nombre de films
#
# # Fonction pour récupérer les films depuis TMDB et les stocker dans la base de données
# def fetch_movies_from_tmdb(max_movies=20000):
#     API_KEY = '0d42ca23b61265745dde50c6866fb862'  # Clé API pour accéder à TMDB
#     page = 1  # Commencer à la première page
#     total_movies = get_movie_count()  # Obtenir le nombre actuel de films dans la base de données
#
#     connection = get_db_connection()  # Obtenir une connexion à la base de données
#     cursor = connection.cursor()  # Créer un curseur pour exécuter les commandes SQL
#
#     while total_movies < max_movies:
#         url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={page}'  # URL pour obtenir les films populaires paginés
#         response = requests.get(url)  # Faire une requête GET à l'URL
#         data = response.json()  # Convertir la réponse en JSON
#         movies = data['results']  # Extraire les résultats de la réponse JSON
#
#         if not movies:  # Arrêter si aucun film n'est retourné
#             break
#
#         for movie in movies:  # Pour chaque film dans les résultats
#             if total_movies >= max_movies:  # Arrêter si le nombre maximum de films est atteint
#                 break
#             cursor.execute('''
#                 INSERT INTO movies (movie_id, title, overview, poster_path)
#                 VALUES (%s, %s, %s, %s)
#                 ON DUPLICATE KEY UPDATE
#                 title = VALUES(title),
#                 overview = VALUES(overview),
#                 poster_path = VALUES(poster_path)
#             ''', (movie['id'], movie['title'], movie['overview'], movie['poster_path']))  # Insérer ou mettre à jour les films
#             total_movies += 1  # Incrémenter le compteur de films
#
#         connection.commit()  # Valider la transaction
#         page += 1  # Passer à la page suivante
#
#     cursor.close()  # Fermer le curseur
#     connection.close()  # Fermer la connexion
#
# # Fonction pour récupérer les films depuis la base de données
# def get_movies():
#     connection = get_db_connection()  # Obtenir une connexion à la base de données
#     cursor = connection.cursor(dictionary=True)  # Créer un curseur avec le mode dictionnaire
#     cursor.execute('SELECT * FROM movies')  # Exécuter la commande SQL pour obtenir tous les films
#     movies = cursor.fetchall()  # Récupérer tous les films
#     cursor.close()  # Fermer le curseur
#     connection.close()  # Fermer la connexion
#     return pd.DataFrame(movies)  # Retourner les films sous forme de DataFrame pandas
#
# # Fonction pour obtenir l'URL du poster d'un film
# def fetch_poster(movie_id):
#     API_KEY = '0d42ca23b61265745dde50c6866fb862'  # Clé API pour accéder à TMDB
#     url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}'  # URL pour obtenir les détails du film
#     data = requests.get(url).json()  # Faire une requête GET à l'URL et convertir la réponse en JSON
#     poster_path = data.get('poster_path', '')  # Obtenir le chemin du poster
#     full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""  # Construire l'URL complète du poster
#     return full_path  # Retourner l'URL complète du poster
#
# # Fonction pour recommander des films basés sur la similarité
# def recommend(movie_title):
#     movies = get_movies()  # Récupérer les films depuis la base de données
#     index = movies[movies['title'] == movie_title].index[0]  # Trouver l'index du film sélectionné
#     similarity = pickle.load(open('models/similarite.pkl', 'rb'))  # Charger le modèle de similarité
#     distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)  # Calculer les distances et trier
#
#     recommended_movies_name = []  # Liste pour les noms des films recommandés
#     recommended_movies_poster = []  # Liste pour les posters des films recommandés
#
#     for i in distances[1:6]:  # Pour les 5 films les plus similaires
#         movie = movies.iloc[i[0]]  # Obtenir les détails du film
#         recommended_movies_poster.append(fetch_poster(movie['movie_id']))  # Ajouter le poster à la liste
#         recommended_movies_name.append(movie['title'])  # Ajouter le titre à la liste
#
#     return recommended_movies_name, recommended_movies_poster  # Retourner les recommandations
#
# # Créer les tables au démarrage de l'application
# create_tables()
# # Récupérer les films depuis TMDB et les stocker dans la base de données si le nombre est inférieur à 5000
# if get_movie_count() < 5000:
#     fetch_movies_from_tmdb()
#
# # Interface utilisateur Streamlit
# st.header('Système de Recommandation de Films')  # Titre de l'application
#
# movies = get_movies()  # Récupérer les films depuis la base de données
# movie_list = movies['title'].values  # Obtenir la liste des titres de films
#
# # Widget de sélection de film
# selected_movie = st.selectbox(
#     'Tape ou sélectionne un film pour avoir une recommandation',
#     movie_list
# )
#
# # Bouton pour afficher les recommandations
# if st.button('Montrer la recommandation'):
#     recommended_movies_name, recommended_movies_poster = recommend(selected_movie)  # Obtenir les recommandations
#     cols = st.columns(5)  # Créer 5 colonnes pour afficher les recommandations
#     for col, name, poster in zip(cols, recommended_movies_name, recommended_movies_poster):  # Pour chaque recommandation
#         with col:  # Ajouter le texte et l'image dans la colonne correspondante
#             st.text(name)
#             st.image(poster)









# # import des packages
# import pickle # pour lire et utiliser le model
# import streamlit as st  # Pour créer l'interface utilisateur
# import requests  # Pour faire des requêtes HTTP
#
# # Fonction pour récupérer l'affiche d'un film à partir de l'API de The Movie Database (TMDb)
# def fetch_poster(movie_id):
#     # URL pour récupérer les détails du film à partir de l'API de TMDb
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=0d42ca23b61265745dde50c6866fb862".format(movie_id)
#     data = requests.get(url)  # Faire une requête GET à l'API
#     data = data.json()  # Convertir la réponse en JSON
#     poster_path = data['poster_path']  # Extraire le chemin de l'affiche
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path  # Construire l'URL complète de l'affiche
#
#     return full_path  # Retourner l'URL de l'affiche
#
# # Fonction pour recommander des films similaires à partir d'un film donné
# def recommend(movie):
#     # Trouver l'index du film dans le DataFrame
#     index = movies[movies['title'] == movie].index[0]
#     # Calculer les distances de similarité et les trier par ordre décroissant
#     distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)
#     recommended_movies_name = []  # Liste pour stocker les noms des films recommandés
#     recommended_movies_poster = []  # Liste pour stocker les affiches des films recommandés
#     # Parcourir les 5 premiers films similaires
#     for i in distances[1:6]:
#         movie_id = movies.iloc[i[0]].movie_id  # Récupérer l'ID du film
#         recommended_movies_poster.append(fetch_poster(movie_id))  # Ajouter l'affiche à la liste
#         recommended_movies_name.append(movies.iloc[i[0]].title)  # Ajouter le titre à la liste
#     return recommended_movies_name, recommended_movies_poster  # Retourner les listes des films recommandés et leurs affiches
#
# # Configuration de l'interface utilisateur avec Streamlit
# st.header('Systeme de Recommandation de Films')
# # Charger les données des films et les similarités à partir des fichiers pickle
# movies = pickle.load(open('models/movie_list.pkl', 'rb'))
# similarity = pickle.load(open('models/similarite.pkl', 'rb'))
#
# # Liste des titres de films pour le menu déroulant
# movie_list = movies['title'].values
# # Créer un menu déroulant pour sélectionner un film
# selected_movie = st.selectbox(
#     'Tape ou selectionne un film pour avoir une recommandation',
#     movie_list
# )
#
# # Bouton pour générer les recommandations
# if st.button('Montrer la recommandation'):
#     # Appeler la fonction de recommandation avec le film sélectionné
#     recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
#     # Créer une disposition en colonnes pour afficher les recommandations
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(recommended_movies_name[0])  # Afficher le titre du premier film recommandé
#         st.image(recommended_movies_poster[0])  # Afficher l'affiche du premier film recommandé
#
#     with col2:
#         st.text(recommended_movies_name[1])  # Afficher le titre du deuxième film recommandé
#         st.image(recommended_movies_poster[1])  # Afficher l'affiche du deuxième film recommandé
#
#     with col3:
#         st.text(recommended_movies_name[2])  # Afficher le titre du troisième film recommandé
#         st.image(recommended_movies_poster[2])  # Afficher l'affiche du troisième film recommandé
#
#     with col4:
#         st.text(recommended_movies_name[3])  # Afficher le titre du quatrième film recommandé
#         st.image(recommended_movies_poster[3])  # Afficher l'affiche du quatrième film recommandé
#
#     with col5:
#         st.text(recommended_movies_name[4])  # Afficher le titre du cinquième film recommandé
#         st.image(recommended_movies_poster[4])  # Afficher l'affiche du cinquième film recommandé
