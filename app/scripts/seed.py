import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

USERS = [
    {"name": "Amir", "email": "amir@test.com"},
    {"name": "test", "email": "test@test.com"},
]

TAGS = [
    "aged",
    "legendary",
    "conjured",
    "normal",
]

ITEMS = [
    {
        "name": "Aged Brie",
        "sell_in": 10,
        "quality": 20,
        "owner_email": "amir@test.com",
        "tags": ["aged"],
    },
    {
        "name": "Sulfuras",
        "sell_in": 0,
        "quality": 80,
        "owner_email": "test@test.com",
        "tags": ["legendary"],
    },
    {
        "name": "Conjured Mana Cake",
        "sell_in": 3,
        "quality": 6,
        "owner_email": "amir@test.com",
        "tags": ["conjured"],
    },
]


def get_conn():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def seed_users(cur):
    for u in USERS:
        cur.execute(
            """
            INSERT INTO users (name, email)
            VALUES (%s, %s)
            ON CONFLICT (email) DO NOTHING
            RETURNING id;
            """,
            (u["name"], u["email"]),
        )


def seed_tags(cur):
    for tag in TAGS:
        cur.execute(
            """
            INSERT INTO tags (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
            """,
            (tag,),
        )


def get_user_id(cur, email: str) -> int:
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    return cur.fetchone()[0]


def get_tag_id(cur, name: str) -> int:
    cur.execute("SELECT id FROM tags WHERE name = %s", (name,))
    return cur.fetchone()[0]


def seed_items(cur):
    for item in ITEMS:
        owner_id = get_user_id(cur, item["owner_email"])

        cur.execute(
            """
            INSERT INTO items (name, sell_in, quality, owner_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
            """,
            (item["name"], item["sell_in"], item["quality"], owner_id),
        )

        item_id = cur.fetchone()[0]

        for tag_name in item["tags"]:
            tag_id = get_tag_id(cur, tag_name)
            cur.execute(
                """
                INSERT INTO item_tags (item_id, tag_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (item_id, tag_id),
            )


def main():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            seed_users(cur)
            seed_tags(cur)
            seed_items(cur)
            conn.commit()
            print("Database seeded successfully")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
