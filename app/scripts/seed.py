import asyncio
import random
import psycopg
from psycopg.rows import tuple_row

from app.db.mongo.session import mongo_db
from app.db.postgres.session import get_db

from app.db.postgres.models import Item, Tag, User as PgUser


from sqlalchemy.orm import Session


ITEM_NAMES = ["Aged Brie", "Sulfuras", "Conjured Mana Cake", "Backstage"]

USERS = [
    {"name": "Amir", "email": "amir@test.com"},
    {"name": "test", "email": "test@test.com"},
    {"name": "test1", "email": "test1@test.com"},
    {"name": "test2", "email": "test2@test.com"},
    {"name": "test4", "email": "test4@test.com"},
]

TAGS = ["food", "legendary", "magic", "concert", "daily", "rare"]


def seed_users(db:Session):
    users = []

    for u in USERS:

        user_body = PgUser(
            name=u["name"],
            email=u["email"]
        )

        db.add(user_body)
        db.commit()
        db.refresh(user_body)

        if user_body:
            users.append({"_id": user_body.id, "name": user_body.name, "email": user_body.email})
        else:
            user_body = PgUser(
                name=u["name"],
                email=u["email"]
            )
            
            users.append({"_id": user_body.id, "name": user_body.name, "email": user_body.email})

            db.commit()

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


def seed_items(db:Session, users, count=2000):
    items = []

    for _ in range(count):
        owner = random.choice(users)  

        name = random.choice(ITEM_NAMES)
        sell_in = random.randint(1, 30)
        quality = random.randint(0, 50)

        item_body = Item(
            name=name, 
            sell_in=sell_in,
            quality=quality,
            owner_id=owner["_id"]
        )

        db.add(item_body)
        db.commit() 
        db.refresh(item_body)


        item_id = item_body.id

        tag_count = random.randint(1, 3)
        item_tags = random.sample(TAGS, tag_count)

        tag_objs = [Tag(name=tag_name, item_id=item_id) for tag_name in item_tags]
        db.add_all(tag_objs)
        db.commit()
    

        items.append({
            "_id": item_id,
            "name": item_body.name,
            "sell_in": item_body.sell_in,
            "quality": item_body.quality,
            "owner": owner, 
            "tags": item_tags,
        })

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
    db = next(db_gen)

    try:
        users = seed_users(db)
        items = seed_items(db, users, count=10000)
    finally:
        db.close()

    await seed_mongo(items)
    await seed_mongo_users(users)
    await seed_mongo_items(items)

    print(f"Seed completed: {len(users)} users, {len(items)} items")

if __name__ == "__main__":
    asyncio.run(main())
