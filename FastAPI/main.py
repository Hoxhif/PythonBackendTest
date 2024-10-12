from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles # Necesario para importar archivos estaticos como imagenes o documentos.

app = FastAPI() # Contexto inicial de como se comportará el servidor.

# Routers:

app.include_router(products.router)
app.include_router(users.router)
#app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static") # http://127.0.0.1:8000/static/images/rey.png

# A medida que vamos avanzando intentado hacer cosas concretas o seguir convenciones tendremos que ir metiendo cosas al constructor

# para arrancar el servidor uvicorn main:app --reload
# para pararlo ponemos debemos pulsar control+c en la consola de comandos

# HOLA MUNDO:

# Una funcion de la API es una funcion que vamos a llamar para nuestro servidor y que el servidor retorna lo que deba.
# Debemos indicar la llamada del servidor, la direccion de nuestro servidor. 
# @app accedemos al contexto de FastAPI, con una funcion llamada get
#Siempre que llamamos al servidor, la funcion que se ejecuta tiene que ser asincrona.
# De esta manera el servidor sigue funcionando mientras que eso se ejecuta 
@app.get("/")
async def root():  
    return "Hola FastAPI"

# Lo correcto es devolver un JSON usando los estandares para las peticiones
# Tenemos que desplegar en una nueva ruta, 1 ruta por metodo get
@app.get("/url")
async def url():  # Aunque se puede dejar el mismo nombre, obligatorio cambiar el nombre de la funcion
    return {"url_youtube":"https://www.youtube.com/"}