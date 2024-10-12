from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
# para arrancar el servidor uvicorn users:app --reload
# para pararlo ponemos debemos pulsar control+c en la consola de comandos
# API para usuarios.

router = APIRouter(prefix="/user", tags=["user"], responses={404: {"message":"No encontrado"}})

# Entidad Usuario:
class User(BaseModel): # La clase User hereda de BaseModel, nos da la capacidad de crear entidades
    id: int
    name: str # FastAPI nos pide tipar para hacerlo más rapido.
    surname: str
    age: int

# Esto va a ser por ahora mi array de memoria para guardar datos de prueba
users_list =    [User(id=1,name="Ramón",surname= "Gimenez González",age= 23),
                User(id=2,name="Marcelo",surname= "Gullo Garrido",age= 12),
                User(id=3,name="Francisco",surname= "Pérez Guirado",age= 23)] 

# operaciones para obtener usuarios

@router.get("/") # GET http://127.0.0.1:8000/user
async def user():
    return users_list

# Operacion con parametro XPATH 
@router.get("/{id}") # GET http://127.0.0.1:8000/user/1
async def user(id: int):
    # Filter es una funcion de orden superior, porque se encarga de hacer operaciones complejas devolviendo un resultado.
    users = filter(lambda user: user.id == id, users_list) # Este filter lo podemos aplicar a cualquier estrcutra con varios objetos
    try:
        return list(users)[0] # Es importante saber que esto devuelve un list, si no le ponemos list dará error 500. 
    except:
        raise HTTPException(status_code=404,detail=f"No se ha encontrado al Usuario con el id {id}")
    
@router.get("/iduser/") # GET http://127.0.0.1:8000/user/?id=1
async def user(id: int):
    users = filter(lambda user: user.id == id, users_list) 
    try:
        return list(users)[0]  
    except:
        raise HTTPException(status_code=404,detail=f"No se ha encontrado al Usuario con el id {id}")

# operacion para añadir usuarios
# Indicamos en el parametro del post el status_code a 201 codigo http de creacion.
@router.post("/",response_model=User,status_code=201) # Le indicamos la ruta que va a tener para poder crear usuarios. Tambien le pasamos respose_model para indicar que va a devolver si todo va bien.
async def user(user: User): # Tiene como parametro añadir es un usuarios.
        if len(list(filter(lambda usuario: usuario.id == user.id, users_list))) != 0: # Esto reemplaza al for each que busca ids.
            raise HTTPException(status_code=409, detail="El usuario ya existe.") # Creamos la excepción para que el servidor pille el error
        else:
            users_list.append(user) # Añadir a la lista el usuario.
            return {f"El usuario con ID: {user.id} se ha insertado correctamente."}

# operacion para actualizar usuarios

@router.put("/")
async def user(user: User):
    encontrado = False
    for index, tbchange in enumerate(users_list): # Enumerate devuelve por un lado la posicion y por otro el objeto en si 
        if tbchange.id == user.id:
            encontrado = True
            users_list[index] = user # le ponemos ese nuevo valor del user que nos pasan por parametro en esa posicion.
            return {f"El usuario con ID: {user.id} se ha actualizado correctamente."}
    if not encontrado:
        raise HTTPException(status_code=404,detail=f"No se ha encontrado al Usuario con el id {user.id}")
    
@router.delete("/{id}")
async def user(id: int):
    encontrado = False
    for index, tbdelete in enumerate(users_list):
        if tbdelete.id == id:
            encontrado=True
            del users_list[index]
            return {f"El usuario con ID: {id} se ha borrado correctamente."}
    if not encontrado:
        raise HTTPException(status_code=404,detail=f"No se ha encontrado al Usuario con el id {id}")

'''
@app.get("/usersclass")
async def usersclass():
    return User(name="José Antonio",surname= "Guirado González",age= 23)

# Si nos referimos a usuarios deberiamos empezar por /users
@app.get("/usersjson")
async def usersjson():  # Definimos en JSON el return.
    return [{"name":"José Antonio", "surname":"Guirado González", "age":23},
            {"name":"Marcelo", "surname":"Gullo Garrido", "age":13},
            {"name":"Francisco", "surname":"Pérez Guirado", "age":23}]
'''



