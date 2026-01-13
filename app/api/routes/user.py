from fastapi import APIRouter, Depends, Response, status 

from app.domain.models import (
    UserResponse, 
    UserCreate
)

from app.domain.errors import email_already_exist 
from app.db.postgres.models import Item, Tag, User as PgUser


from app.utils.converter import userTupleToDic
from sqlalchemy.orm import Session
from app.db.postgres.session import get_db 
from app.db.mongo.session import mongo_db 


import structlog


logger = structlog.get_logger() 

router = APIRouter(prefix="/users", tags=["users"])


# READ 
@router.get("", status_code=status.HTTP_200_OK)
async def all_user() : 
    cursor = mongo_db.users_read.find({})
    users = await cursor.to_list(length=100)
    for user in users:
        user["id"] = user.pop("_id")


    return users

# CREATE 
@router.post(
    "", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
) : 
    user_body = PgUser(
        name=user.name,
        email=user.email
    )
    db.add(user_body)
    db.commit()
    db.refresh(user_body)

    user_dict = {"id": user_body.id, "name": user_body.name, "email": user_body.email}


    read_model = {
        "_id": user_body.id,
        "name": user_body.name,
        "email": user_body.email
    }
    
    await mongo_db.users_read.insert_one(read_model)

    logger.info("user.create", user_dict)

    return user_dict
