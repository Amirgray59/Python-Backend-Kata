import os
import psycopg
from dotenv import load_dotenv

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


            # # INDEXES (access patterns)
            # cur.execute("CREATE INDEX IF NOT EXISTS ix_items_owner ON items(owner_id);")
            # cur.execute("CREATE INDEX IF NOT EXISTS ix_item_tags_item ON item_tags(item_id);")
            # cur.execute("CREATE INDEX IF NOT EXISTS ix_item_tags_tag ON item_tags(tag_id);")

            conn.commit()

    finally:
        conn.close()
