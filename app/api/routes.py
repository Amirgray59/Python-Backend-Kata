from fastapi import APIRouter, Depends, Response, status
from typing import Dict
import uuid

from app.domain.models import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
)
from app.domain.errors import invalid_type, item_not_found

from app.db.postgres.session import get_db
from app.db.mongo.session import mongo_db
from psycopg import Connection

from app.utils.converter import itemTupleToDic
import structlog


logger = structlog.get_logger()

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/tables")
def list_tables(db: Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public';
            """
        )
        tables = [row[0] for row in cur.fetchall()]

    return {
        "tables": tables
    }

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemResponse,
)
async def create_item(
    item: ItemCreate,
    response: Response,
    db: Connection = Depends(get_db),
):

    with db.cursor() as cur :     
        cur.execute(
            "INSERT INTO items (name, sell_in, quality) VALUES (%s, %s, %s) RETURNING id, name, sell_in, quality",
            (item.name, item.sell_in, item.quality)
        )
        item = cur.fetchone()
        db.commit()

    item_dict = itemTupleToDic(item)

    await mongo_db.items_read.insert_one(
    {
        "_id": item_dict["id"],
        "name": item_dict["name"],
        "sell_in": item_dict["sell_in"],
        "quality": item_dict["quality"]
    }
)
    
    logger.info(
        "item.create",
        item_dict
    )
    return item_dict 

@router.get(
    "/{item_id}",
    response_model=ItemResponse,
)
async def get_item(
    item_id: int,
    db: Connection = Depends(get_db),
):

    item = await mongo_db.items_read.find_one({"_id": item_id})

    if not item:
        item_not_found(item_id)

    item["id"] = item.pop("_id")

    logger.info(
        "item.get",
        item_id=item_id
    )
    
    return item


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
)
async def update_item(
    item_id: int,
    payload: ItemUpdate,
    db: Connection = Depends(get_db),
):  

    item = await mongo_db.items_read.find_one({"_id": item_id})

    if not item:
        item_not_found(item_id)

    with db.cursor() as cur :     
        cur.execute(
            "UPDATE items SET name=%s, sell_in=%s, quality=%s WHERE id=%s RETURNING id, name, sell_in, quality",
            (payload.name, payload.sell_in, payload.quality, item_id)
        )
        new_item = cur.fetchone()
        db.commit()

    new_item_dic = itemTupleToDic(new_item)

    logger.info(
        "item.update",
        new_item_dic
    )
    return new_item_dic



@router.delete(
    "/{item_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_item(
    item_id: int,
    db: Connection = Depends(get_db),
):
    item = await mongo_db.items_read.find_one({"_id": item_id})

    if not item:
        item_not_found(item_id)


    with db.cursor() as cur :     
        cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
        db.commit()

    await mongo_db.items_read.delete_one({"_id": item_id})

    logger.info(
        "item.delete",
        item_id=item_id
    )

    return {"detail": f"Item with id {item_id}, deleted"}
