from pymongo import MongoClient

# Esto nos sirve para conectarnos a la base de datos en local.
db_client = MongoClient() # Si no le pasamos parametros se conecta por defecto a la url del local host
# db_client = MongoClient().local para no tener que estar poniendo .local.users todo el rato en otro lado.

