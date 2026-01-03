from fastapi import APIRouter, Depends, Response, status
from typing import List

from app.domain.models import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
)
from app.domain.errors import item_not_found, owner_not_found

from app.db.postgres.session import get_db
from app.db.mongo.session import mongo_db
from psycopg import Connection

from app.utils.converter import itemTupleToDic
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/items", tags=["items"])



@router.get("", status_code=status.HTTP_200_OK)
async def all_items():
    cursor = mongo_db.items_read.find({})
    items = await cursor.to_list(length=100)

    for item in items:
        item["id"] = item.pop("_id")

    return items

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemResponse,
)
async def create_item(
    item: ItemCreate,
    db: Connection = Depends(get_db),
):

    user = await mongo_db.users_read.find_one({"_id": item.owner_id})

    with db.cursor() as cur:
    
        if not user:
            owner_not_found(item.owner_id)

        cur.execute(
            """
            INSERT INTO items (name, sell_in, quality, owner_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id, name, sell_in, quality
            """,
            (item.name, item.sell_in, item.quality, item.owner_id),
        )
        row = cur.fetchone()
        item_dict = itemTupleToDic(row)

        for tag_name in item.tags:
            cur.execute(
                """
                INSERT INTO tags (name, item_id)
                VALUES (%s, %s)
                """,
                (tag_name, item_dict["id"]),
            )

        db.commit()

    owner_dict = {
        "id": user["_id"],
        "name": user["name"],
        "email": user["email"]
    }

    read_model = {
        "_id": item_dict["id"],
        "name": item_dict["name"],
        "sell_in": item_dict["sell_in"],
        "quality": item_dict["quality"],
        "owner": owner_dict,
        "tags": item.tags,
    }

    await mongo_db.items_read.insert_one(read_model)

    read_model["id"] = read_model.pop("_id")

    logger.info("item.create", item=read_model)
    return read_model


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    item = await mongo_db.items_read.find_one({"_id": item_id})

    if not item:
        item_not_found(item_id)

    item["id"] = item.pop("_id")
    return item



@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    payload: ItemUpdate,
    db: Connection = Depends(get_db),
):
    with db.cursor() as cur:

        item = await mongo_db.items_read.find_one({"_id": item_id})

        if not item:
            item_not_found(item_id)

        owner_id = item["owner"]["id"]

        if payload.tags is not None:
            cur.execute("DELETE FROM tags WHERE item_id = %s", (item_id,))
            for tag in payload.tags:
                cur.execute("INSERT INTO tags (name, item_id) VALUES (%s, %s)", (tag, item_id))

        cur.execute(
            """
            UPDATE items
            SET
                name = COALESCE(%s, name),
                sell_in = COALESCE(%s, sell_in),
                quality = COALESCE(%s, quality)
            WHERE id = %s
            RETURNING id, name, sell_in, quality
            """,
            (payload.name, payload.sell_in, payload.quality, item_id)
        )
        updated_row = cur.fetchone()
        db.commit()

    owner = await mongo_db.users_read.find_one({"_id": owner_id})
    if owner:
        owner_dict = {"id": owner["_id"], "name": owner["name"], "email": owner["email"]}
    else:
        owner_dict = {"id": owner_id, "name": "unknown", "email": "unknown"}

    update_fields = {}
    if payload.name is not None:
        update_fields["name"] = payload.name
    if payload.sell_in is not None:
        update_fields["sell_in"] = payload.sell_in
    if payload.quality is not None:
        update_fields["quality"] = payload.quality
    if payload.tags is not None:
        update_fields["tags"] = payload.tags

    await mongo_db.items_read.update_one(
        {"_id": item_id},
        {"$set": update_fields},
        upsert=True 
    )

    updated_item = await mongo_db.items_read.find_one({"_id": item_id})
    updated_item["id"] = updated_item.pop("_id")
    updated_item["owner"] = owner_dict

    logger.info("item.update", item=updated_item)
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_item(
    item_id: int,
    db: Connection = Depends(get_db),
):
    with db.cursor() as cur:
        cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
        if cur.rowcount == 0:
            item_not_found(item_id)
        
        cur.execute("DELETE FROM tags WHERE item_id = %s", (item_id,))
        db.commit()

    await mongo_db.items_read.delete_one({"_id": item_id})

    logger.info("item.delete", item_id=item_id)

    return {"detail": f"Item with id {item_id} has been deleted"}
