def user_schema(user) -> dict:  #Con esto lo que hacemos es tipar el tipo de dato a devolver
    return {"id":str(user["_id"]),"username":user["username"], "email":user["email"]}

def users_schema(users) -> list:
    return [user_schema(user) for user in users]
        