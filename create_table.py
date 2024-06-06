import mysql.connector
from db_config import get_db_connection

connection = get_db_connection()
cursor = connection.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INT AUTO_INCREMENT PRIMARY KEY,  # Clé primaire avec auto-incrémentation
            movie_id INT UNIQUE,  # ID unique du film (provenant de TMDB)
            title VARCHAR(255),  # Titre du film
            overview TEXT,  # Description du film
            poster_path VARCHAR(255)  # Chemin du poster du film
        ) ENGINE=InnoDB
    ''')

connection.commit()
cursor.close()
connection.close()

