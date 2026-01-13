from typing import Tuple, Any, Dict

def itemTupleToDic(item:tuple) : 
    item_dict = {
        "id": item[0],
        "name": item[1],
        "sell_in": item[2],
        "quality": item[3],
    }

    return item_dict

def tagTupleToDic(tag:tuple) : 
    tag_dic = {
        "id" : tag[0],
        "name": tag[1],
        "item_id": tag[2]
    }

    return tag_dic


def userTupleToDic(row: Tuple[Any, ...]) -> Dict[str, Any]:
    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
    }
