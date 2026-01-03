from fastapi import APIRouter, Depends, Response, status 

from app.domain.models import (
    UserResponse, 
    UserCreate
)

from app.domain.errors import email_already_exist 

from app.utils.converter import userTupleToDic

from app.db.postgres.session import get_db 
from app.db.mongo.session import mongo_db 
from psycopg import Connection 

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
    db: Connection = Depends(get_db),
) : 
    with db.cursor() as cur : 
        cur.execute(
            """
            INSERT INTO users (name, email)
            VALUES (%s, %s)
            RETURNING id, name, email 
            """,
            (user.name, user.email)
        )
        user = cur.fetchone()
        db.commit() 

    user_dict = userTupleToDic(user)

    read_model = {
        "_id": user_dict["id"],
        "name": user_dict["name"],
        "email": user_dict["email"]
    }
    
    await mongo_db.users_read.insert_one(read_model)

    logger.info("user.create", user_dict)

    return user_dict
