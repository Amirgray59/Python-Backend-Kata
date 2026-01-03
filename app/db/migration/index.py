import os
import psycopg
from dotenv import load_dotenv
from app.db.mongo.session import mongo_db

load_dotenv()


def create_indexes():
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
                CREATE INDEX IF NOT EXISTS ix_items_owner_id
                ON items(owner_id);
            """)

            cur.execute("""
                CREATE INDEX IF NOT EXISTS ix_tags_item_id
                ON tags(item_id);
            """)

            conn.commit()
    finally:
        conn.close()

async def create_index_mongo() : 

    await mongo_db.items_read.create_index(
        [("tags", 1)],
        name="ix_items_tags"
    )

    await mongo_db.items_read.create_index(
        [("owner.id", 1)],
        name="ix_items_owner"
    )

