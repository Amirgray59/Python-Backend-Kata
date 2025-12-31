from typing import Union 
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException

def report_error(
    *,
    status_code:int, 
    type_: str,
    title:str, 
    detail: Union[None, str]) : 

    body = {
        "type": type_,
        "title": title, 
        "status": status_code
    }

    if detail : 
        body["detail"] = detail 

    return JSONResponse(
        status_code=status_code,
        content=body,
        media_type="application/problem+json"
    )


def invalid_type(detail:str) : 
    return report_error(status_code=status.HTTP_400_BAD_REQUEST,
    type_="https://example.com/problems/invalid-input",
    title="Invalid input",
    detail=detail
    )

def item_not_found(item_id: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "type": "https://example.com/problems/item-not-found",
            "title": "Item not found",
            "status": 404,
            "detail": f"Item with id '{item_id}' was not found",
        },
    )