from pydantic import BaseModel, EmailStr
from typing import List, Optional


# -------------------------
# User
# -------------------------
class UserResponse(BaseModel):
    id: int
    name: str
    email: str 

class UserCreate(BaseModel) : 
    name: str 
    email: str


# -------------------------
# Item – Create
# -------------------------
class ItemCreate(BaseModel):
    name: str
    sell_in: int
    quality: int
    owner_id: int
    tags: List[str] = []


# -------------------------
# Item – Update
# -------------------------
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    sell_in: Optional[int] = None
    quality: Optional[int] = None
    tags: Optional[List[str]] = None


# -------------------------
# Item – Response
# -------------------------
class ItemResponse(BaseModel):
    id: int | str
    name: str
    sell_in: int
    quality: int
    owner: UserResponse
    tags: List[str]
