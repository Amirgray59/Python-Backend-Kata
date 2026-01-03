from fastapi import HTTPException, status


def item_not_found(item_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found",
    )

def email_already_exist(email: str) :  
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Email already exist: {email}"
    )

def invalid_type(message: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )

def owner_not_found(owner_id:int) : 
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Owner with id {owner_id} not found"
    )

