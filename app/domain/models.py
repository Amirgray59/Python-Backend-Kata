from pydantic import BaseModel, Field
from typing import Union

class ItemCreate(BaseModel) : 
    name:str
    sell_in: int 
    quality: int 

class ItemUpdate(BaseModel):
    name: str | None = None
    sell_in: int | None = None
    quality: int | None = None


class ItemResponse(BaseModel):
    id: str = Field()
    name: str
    sell_in: int
    quality: int