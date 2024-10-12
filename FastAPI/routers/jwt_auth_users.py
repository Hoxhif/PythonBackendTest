from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256" # Esto viene de la página web de JWT, se puede consultar, es el algoritmo que vamos a usar para encriptar.
ACCESS_TOKEN_DURATION = 1 # 1 minuto de duracion del token de acceso.
SECRET = "77fb8ee2d7b43c002fb6a983f682251114df6b2696549eeff0de5eb8e2d56bf5" # Nuestra secret generada con https://www.browserling.com/tools/random-hex
# Usamos para el secret base 64 digitos.

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes="bcrypt")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User): 
    password: str

# Usamos una página como por ejemplo https://bcrypt-generator.com/ para encriptar con bcryp nuestra contraseña
users_db = {
    "ramon":{
        "username":"ramon",
        "full_name":"Ramón Gimenez González",
        "email":"ramon@gmail.com",
        "disabled":False,
        "password":"$2a$12$xWWzp7TpUj6BLoY0mSWJ7usgbK.Yk/OcIy/ce1zAMMAarMiBi.sGq" # 12345
    },
    "fern":{
        "username":"fern",
        "full_name":"Fernando Gimenez Lopez",
        "email":"fernando@gmail.com",
        "disabled":True,
        "password":"$2a$12$4TftXO0FrEt5KZwTt6RcK.yCxGbHfvXvtIIIE6W0W6t9djr8NeOvO" # 54321
    }
}

def search_user_db(username: str):
    if username in users_db: # Esto confirma si esta en el listado
        return UserDB(**users_db[username])
    
def search_user(username: str): 
    if username in users_db: 
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No estás autorizado", headers={"WWW-Authenticate":"Bearer"})
    try:
        # Esto puede producir un error de tipo JWTError
        user_name = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub") # Con esto podemos obtener el nombre de usuario
        if user_name is None:
            raise exception
    except JWTError: 
        raise exception
    return search_user(user_name)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario Inactivo", headers={"WWW-Authenticate":"Bearer"})
    return user

@router.post("/login") 
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto.")
    user = search_user_db(form.username) 

    if not crypt.verify(form.password,user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta.")
    
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expiration
    access_token = {"sub":user.username, "exp":expire}
    access_token = jwt.encode(access_token, SECRET ,algorithm=ALGORITHM)
    return {"access_token":access_token, "token_type":"bearer"} 

@router.get("/users/me")
async def me(user: User = Depends(current_user)): # Devolvemos el que no tiene contraseña con User
    return user



