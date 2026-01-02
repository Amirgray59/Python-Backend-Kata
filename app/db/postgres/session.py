import os
import psycopg
from dotenv import load_dotenv
from contextlib import contextmanager
from fastapi import Depends

load_dotenv()


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
