from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config


DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)
session = Session()


def get_session():
    return session
