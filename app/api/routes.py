from fastapi import APIRouter, Depends, Response, status
from typing import Dict
import uuid

from app.domain.models import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
)
from app.domain.errors import invalid_type, item_not_found
from app.api.deps import get_db, FakeDB
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemResponse,
)
def create_item(
    item: ItemCreate,
    response: Response,
    db: FakeDB = Depends(get_db),
):
    item_id = str(uuid.uuid4())

    created = {
        "id": item_id,
        "name": item.name,
        "sell_in": item.sell_in,
        "quality": item.quality,
    }

    db[item_id] = created
    response.headers["Location"] = f"/items/{item_id}"
    logger.info(
        "item.create",
        created
    )
    return created



@router.get(
    "/{item_id}",
    response_model=ItemResponse,
)
def get_item(
    item_id: str,
    db: FakeDB = Depends(get_db),
):
    item = db.get(item_id)
    if not item:
        item_not_found(item_id)

    logger.info(
        "item.get",
        item_id=item_id
    )
    return item


@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
)
def update_item(
    item_id: str,
    payload: ItemUpdate,
    db: FakeDB = Depends(get_db),
):
    item = db.get(item_id)
    if not item:
        item_not_found(item_id)

    data = item.copy()

    updates = payload.model_dump(exclude_unset=True)
    data.update(updates)

    db[item_id] = data

    logger.info(
        "item.update",
        data
    )
    return data



@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item(
    item_id: str,
    db: FakeDB = Depends(get_db),
):
    if item_id not in db:
        item_not_found(item_id)

    logger.info(
        "item.delete",
        item_id=item_id
    )
    del db[item_id]
