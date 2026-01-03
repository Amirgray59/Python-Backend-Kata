import asyncio
import random
import psycopg
from psycopg.rows import tuple_row

from app.db.mongo.session import mongo_db
from app.db.postgres.session import get_db

ITEM_NAMES = ["Aged Brie", "Sulfuras", "Conjured Mana Cake", "Backstage"]

USERS = [
    {"name": "Amir", "email": "amir@test.com"},
    {"name": "test", "email": "test@test.com"},
    {"name": "test1", "email": "test1@test.com"},
    {"name": "test2", "email": "test2@test.com"},
    {"name": "test4", "email": "test4@test.com"},
]

TAGS = ["food", "legendary", "magic", "concert", "daily", "rare"]


def seed_users(conn):
    users = []

    with conn.cursor(row_factory=tuple_row) as cur:
        for u in USERS:
            cur.execute(
                """
                INSERT INTO users (name, email)
                VALUES (%s, %s)
                ON CONFLICT (email) DO NOTHING
                RETURNING id, name, email
                """,
                (u["name"], u["email"]),
            )
            row = cur.fetchone()

            if row:
                users.append({"_id": row[0], "name": row[1], "email": row[2]})
            else:
                cur.execute("SELECT id, name, email FROM users WHERE email = %s", (u["email"],))
                row = cur.fetchone()
                users.append({"_id": row[0], "name": row[1], "email": row[2]})

        conn.commit()

    return users

async def seed_mongo_users(users):
    tasks = []
    for u in users:
        tasks.append(
            mongo_db.users_read.update_one({"_id": u["_id"]}, {"$set": u}, upsert=True)
        )
    await asyncio.gather(*tasks)


async def seed_mongo_items(items):
    tasks = []
    for i in items:
        tasks.append(
            mongo_db.items_read.update_one({"_id": i["_id"]}, {"$set": i}, upsert=True)
        )
    await asyncio.gather(*tasks)


def seed_items(conn, users, count=2000):
    items = []

    with conn.cursor(row_factory=tuple_row) as cur:
        for _ in range(count):
            owner = random.choice(users)  

            name = random.choice(ITEM_NAMES)
            sell_in = random.randint(1, 30)
            quality = random.randint(0, 50)

            cur.execute(
                """
                INSERT INTO items (name, sell_in, quality, owner_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id, name, sell_in, quality
                """,
                (name, sell_in, quality, owner["_id"]),
            )

            row = cur.fetchone()
            item_id = row[0]

            tag_count = random.randint(1, 3)
            item_tags = random.sample(TAGS, tag_count)

            for tag in item_tags:
                cur.execute(
                    "INSERT INTO tags (name, item_id) VALUES (%s, %s)",
                    (tag, item_id),
                )

            items.append({
                "_id": item_id,
                "name": row[1],
                "sell_in": row[2],
                "quality": row[3],
                "owner": owner, 
                "tags": item_tags,
            })

        conn.commit()
    return items


async def seed_mongo(items):
    for item in items:
        doc = {
            "_id": item["_id"],  
            "name": item["name"],
            "sell_in": item["sell_in"],
            "quality": item["quality"],
            "owner": item["owner"],
            "tags": item["tags"],
        }

        await mongo_db.items_read.update_one(
            {"_id": doc["_id"]},
            {"$set": doc},
            upsert=True,
        )


# -----------------------
# Main
# -----------------------

async def main():
    print("Seeding started...")

    db_gen = get_db()
    conn = next(db_gen)

    try:
        users = seed_users(conn)
        items = seed_items(conn, users, count=10000)
    finally:
        conn.close()

    await seed_mongo(items)
    await seed_mongo_users(users)
    await seed_mongo_items(items)

    print(f"Seed completed: {len(users)} users, {len(items)} items")


if __name__ == "__main__":
    asyncio.run(main())
