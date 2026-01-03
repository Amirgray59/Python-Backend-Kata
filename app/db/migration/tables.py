import os
import psycopg
from dotenv import load_dotenv
from app.db.mongo.session import mongo_db

load_dotenv()


def create_tables():
    conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    email VARCHAR(200) UNIQUE NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    sell_in INTEGER NOT NULL,
                    quality INTEGER NOT NULL,
                    owner_id INTEGER NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    item_id INTEGER NOT NULL
                        REFERENCES items(id)
                        ON DELETE CASCADE
                );
            """)


            conn.commit()

    finally:
        conn.close()
