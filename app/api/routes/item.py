from fastapi import APIRouter, Depends, Response, status
from typing import List

from sqlalchemy.orm import Session
from app.db.postgres.session import get_db
from app.db.postgres.models import Item, Tag, User as PgUser
from app.db.mongo.session import mongo_db

from app.domain.models import ItemCreate, ItemUpdate, ItemResponse
from app.domain.errors import item_not_found, owner_not_found
from app.utils.converter import itemTupleToDic
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", status_code=status.HTTP_200_OK)
async def all_items(limit: int = 100):
    cursor = mongo_db.items_read.find({})
    items = await cursor.to_list(length=limit)
    for item in items:
        item["id"] = item.pop("_id")
    return items

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):

    user = await mongo_db.users_read.find_one({"_id": item.owner_id})
    if not user:
        owner_not_found(item.owner_id)

    db_item = Item(
        name=item.name,
        sell_in=item.sell_in,
        quality=item.quality,
        owner_id=item.owner_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    tag_objs = [Tag(name=tag_name, item_id=db_item.id) for tag_name in item.tags]
    db.add_all(tag_objs)
    db.commit()

    read_model = {
        "_id": db_item.id,
        "name": db_item.name,
        "sell_in": db_item.sell_in,
        "quality": db_item.quality,
        "owner": {"id": user["_id"], "name": user["name"], "email": user["email"]},
        "tags": item.tags
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

    owner = item["owner"]
    try : 
        item["owner"] = {
            "id": owner["_id"],
            "name": owner["name"],
            "email": owner["email"],
        }
    except KeyError : 
        item["owner"] = {
            "id": owner["id"],
            "name": owner["name"],
            "email": owner["email"],
        }
    item["id"] = item.pop("_id")
    return item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):

    item = await mongo_db.items_read.find_one({"_id": item_id})
    if not item:
        item_not_found(item_id)

    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        item_not_found(item_id)

    if payload.name is not None:
        db_item.name = payload.name
    if payload.sell_in is not None:
        db_item.sell_in = payload.sell_in
    if payload.quality is not None:
        db_item.quality = payload.quality

    if payload.tags is not None:
        db.query(Tag).filter(Tag.item_id == item_id).delete()
        db.add_all([Tag(name=t, item_id=item_id) for t in payload.tags])

    db.commit()
    db.refresh(db_item)

    owner_id = db_item.owner_id
    owner = await mongo_db.users_read.find_one({"_id": owner_id})
    owner_dict = {"id": owner["_id"], "name": owner["name"], "email": owner["email"]} if owner else {"id": owner_id, "name": "unknown", "email": "unknown"}

    update_fields = {}
    if payload.name is not None:
        update_fields["name"] = payload.name
    if payload.sell_in is not None:
        update_fields["sell_in"] = payload.sell_in
    if payload.quality is not None:
        update_fields["quality"] = payload.quality
    if payload.tags is not None:
        update_fields["tags"] = payload.tags

    await mongo_db.items_read.update_one({"_id": item_id}, {"$set": update_fields}, upsert=True)

    updated_item = await mongo_db.items_read.find_one({"_id": item_id})
    updated_item["id"] = updated_item.pop("_id")
    updated_item["owner"] = owner_dict

    logger.info("item.update", item=updated_item)
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_item(item_id: int, db: Session = Depends(get_db)):

    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        item_not_found(item_id)

    db.query(Tag).filter(Tag.item_id == item_id).delete()
    db.delete(db_item)
    db.commit()

    await mongo_db.items_read.delete_one({"_id": item_id})

    logger.info("item.delete", item_id=item_id)
    return {"detail": f"Item with id {item_id} has been deleted"}
