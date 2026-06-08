from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db_creds import DataBase

USERNAME = DataBase.DB_USER
PASSWORD = DataBase.DB_PASSWORD
HOST = DataBase.DB_HOST
PORT = DataBase.DB_PORT
DATABASE_NAME = DataBase.DB_NAME

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    return SessionLocal()