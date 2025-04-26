import os
import mariadb

class Config:
    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    
    # Database config
    DB_HOST = os.environ.get('DB_HOST', 'bioed-new.bu.edu')
    DB_USER = os.environ.get('DB_USER', 'jriya186')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mushky1864')
    DB_NAME = os.environ.get('DB_NAME', 'Team14')
    DB_PORT = int(os.environ.get('DB_PORT', 4253))

# Функция для подключения к MariaDB
def get_db_connection():
    try:
        print(f"Connecting to MariaDB: {Config.DB_HOST}:{Config.DB_PORT} as {Config.DB_USER}")
        conn = mariadb.connect(
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            port=Config.DB_PORT
        )
        print("Database connection established successfully")
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None
