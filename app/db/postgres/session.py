import os
import psycopg
from dotenv import load_dotenv
from contextlib import contextmanager
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



load_dotenv()

# DATABASE_URL = (
#     f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:"
#     f"{os.getenv('POSTGRES_PASSWORD')}@"
#     f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/"
#     f"{os.getenv('POSTGRES_DB')}"
# )

# engine = create_engine(DATABASE_URL, echo=False, future=True, pool_pre_ping=True)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



def get_db():
    conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    try:
        yield conn
    finally:
        conn.close()
