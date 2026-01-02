
def itemTupleToDic(item:tuple) : 
    item_dict = {
        "id": item[0],
        "name": item[1],
        "sell_in": item[2],
        "quality": item[3],
    }

    return item_dict