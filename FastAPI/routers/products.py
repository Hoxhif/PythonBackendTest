from fastapi import APIRouter
# tags para la documentacion. 
router = APIRouter(prefix="/products", responses={404: {"message":"No encontrado"}}, tags=["products"])

product_list = ["Producto1", "Producto2", "Producto3", "Producto4", "Producto5"]

@router.get("/")
async def products():
    return product_list

@router.get("/{id}")
async def products(id: int):
    return product_list[id]