from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# El bearer es la clase que se encarga de gestionar la autenticacion el usuario y contraseña
# el requestform es la forma que se envia a nuestra backend estos criterios de autenticacion, la forma en la que nosotros vamos a enviar el
# usuario y contraseña y la forma de capturar si ese usuario y contraseña es correcta.

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login") # El tokenUrl es basicamente la url que se encarga de gestionar la autenticacion.

class User(BaseModel): # Este sera el usuario que trabajaremos por red, por lo que no lleva su contraseña
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User): # Este será el usuario en base de datos que si incorpora su contraseña
    password: str

# Imaginemos que tenemos base de datos (NoSQL).
# Al final una base de datos no relacional es como JSon más o menos.
users_db = {
    "ramon":{
        "username":"ramon",
        "full_name":"Ramon Gimenez González",
        "email":"ramon@gmail.com",
        "disabled":False, # Esto es muy tipico para cuando se trabaja en base de datos. Para saber rapidamente si el usuario esta o no habilitado.
        "password":"12345" # En base de datos por lo menos la contraseña debe estar Hasheada y encriptada.
    },
    "fern":{
        "username":"fern",
        "full_name":"Fernando Gimenez Lopez",
        "email":"fernando@gmail.com",
        "disabled":True, #En este caso si ponemos disabled la cuenta. 
        "password":"54321" 
    }
}

def search_user_db(username: str):
    if username in users_db: # Esto confirma si esta en el listado
        return UserDB(**users_db[username]) # Esto devuelve el objeto en si en la lista. 
        # NOTA IMPORTANTE: Se debe poner los ** en el UserDB que representa que habra mas parametros a la hora de crear el UserDB(Al ser clase hija sin construccion real de la misma)

def search_user(username: str): # Hemos diferenciado la operacion db y no db para que devuelva o no la contraseña.
    if username in users_db: 
        return User(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No estás autorizado", headers={"WWW-Authenticate":"Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario Inactivo", headers={"WWW-Authenticate":"Bearer"})
    return user

# Operacion para autenticacion:

@router.post("/login") 
async def login(form: OAuth2PasswordRequestForm = Depends()): # Vamos a intentar capturar la forma en la que se logea
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto.")
    user = search_user_db(form.username) # Hacemos esto para que nos devuelva ya objeto tipo UserDB no User, para poder meterle pass
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="La contraseña no es correcta.")
    # Normalmente si el usuario se ha autenticado correctamente lo que se suele devolver es un access token.
    # El access_token deberia ser algo encriptado, y de alguna manera hay que crear algo que devuelva al backend una confirmacion de que ya esta logeado.
    # Vamos a poner con este ejemplo el propio username para el access token, el tipo es bearer.
    return {"access_token":user.username, "token_type":"bearer"} 

# Le vamos a pasar Depends, esto significa que Dependera de si el user está autenticado
# El criterio de dependencia básicamente lo que nos permite validar la firma
@router.get("/users/me")
async def me(user: User = Depends(current_user)): # Devolvemos el que no tiene contraseña con User
    return user