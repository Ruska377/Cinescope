import psycopg2
from config.db_creds import DataBase


connection = psycopg2.connect(
        dbname=DataBase.DB_NAME,
        user=DataBase.DB_USER,
        password=DataBase.DB_PASSWORD,
        host=DataBase.DB_HOST,
        port=DataBase.DB_PORT
)

cursor = connection.cursor()
print(connection.get_dsn_parameters(), "\n")

cursor.close()
