
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

def userTupleToDic(user:tuple) : 
    user_dic = {
        "id" : user[0],
        "name": user[1],
        "email": user[2]
    }

    return user_dic
    
    