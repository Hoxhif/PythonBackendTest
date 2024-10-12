from fastapi import APIRouter, HTTPException, status
from db.models.user import User # Importamos la clase user 
from db.client import db_client # Nos traemos la conexion de la base de datos.
from db.schemas.user import user_schema, users_schema
from bson import ObjectId
router = APIRouter(prefix="/userdb", tags=["userdb"], responses={404: {"message":"No encontrado"}})

# Ya no vamos a trabajar con Listas.
users_list = [] 



@router.get("/", response_model=list[User]) 
async def user(): # Devuelve todos los users.
        return users_schema(db_client.local.users.find())
    

# Operacion con parametro XPATH 
@router.get("/{id}", response_model=User) 
async def user(id: str):
    try:
        return search_user("_id",ObjectId(id)) # Esto lo hacemos porque en MongoDB el _id se guardaba bajo otro objeto llamado oid (Objectid)
    except:
        raise HTTPException(status_code=404, detail="El usuario no se ha encontrado.")
    
@router.get("/iduser/") 
async def user(id: str):
    try:
        return search_user("_id",ObjectId(id))
    except:
        raise HTTPException(status_code=404, detail="El usuario no se ha encontrado.")
# operacion para añadir usuarios
# Indicamos en el parametro del post el status_code a 201 codigo http de creacion.
@router.post("/",response_model=User,status_code=201) # Le indicamos la ruta que va a tener para poder crear usuarios. Tambien le pasamos respose_model para indicar que va a devolver si todo va bien.
async def user(user: User): # Tiene como parametro añadir es un usuarios.
        if db_client.local.users.find_one({"email":user.email}) != None:
            raise HTTPException(status_code=409, detail="El usuario ya existe.")
        else:
            user_dict = dict(user) # Pasamos de user a dict usando Pydantic es muy facil que es nuestra BaseModel.
            del user_dict["id"] # Esto lo hacemos para que seas el propio Mongo el que tenga que meterle un ID 
            user_insertado = db_client.local.users.insert_one(user_dict) # Pydantic permite gestionar modelos a nivel de entidad, es decir para transformar rapidamente objetos a JSON y cosas asi...
            id = user_insertado.inserted_id # Obtenemos el id puesto por Mongo.

            new_user = user_schema(db_client.local.users.find_one({"_id":id})) # Para buscar el usuario en nuestra base de datos. Tenemos que usar _id. 
            # new_user retorna un JSON, habria que volver a transformarlo a User.
            return User(**new_user)
            #return {f"El usuario con ID: {user.id} se ha insertado correctamente."}

# operacion para actualizar usuarios

@router.put("/", status_code=201)
async def user(user: User):
        # Como tenemos un user, pero en base de datos tiene que estar en otro formato lo pasamos a dict.
        user_dict = dict(user)
        del user_dict["id"] # le borramos el id otra vez.
        try:
            # Debemos usar el replace por que put realmente reemplazar un item, no lo updatea como tal. Para eso esta el patch.
            db_client.local.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict) # Usamos el dict para reemplazarlo.
            return {"resultado":"Usuario actualizado correctamente."}
        except:
            raise HTTPException(status_code=404,detail=f"No se ha encontrado al Usuario con el id {user.id}")
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    encontrado= db_client.local.users.find_one_and_delete({"_id":ObjectId(id)}) # Podemos usar delete normal o este que es find and delete.
    if not encontrado: # Si no existe el usuario encontrado no tendra valor de haber encontrado nada.
        raise HTTPException(status_code=404,detail=f"No se ha encontrado al Usuario con el id {id}")

def search_user(key: str, value):
    try:
        user= db_client.local.users.find_one({key:value})
        return User(**user_schema(user))
    except:
        {"error":"No se encontró al usuario"}



