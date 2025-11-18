from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title= "API DE PRODUCTOS")

class Products(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
    
list_products = []

@app.get("/products")
async def get_products():
    if not list_products:
        return "La lista esta vacía, agrega productos"
    return list_products

@app.get("/products/{id}", response_model = Products)
async def get_products(id: int):
    existing = search_id(id)
    if existing is None:
        raise HTTPException(status_code= 404, detail= "ID NO ENCONTRADO")
    return existing

@app.post("/products")
async def post_products(product : Products):
    for products in list_products:
        if products.id == product.id:
            raise HTTPException(status_code= 409, detail= "YA EXISTE EL ID")
    list_products.append(product)
    return product

@app.put("/products/{id}")
async def put_products(id: int, product: Products):
    
    found = False
    
    for index, value in enumerate(list_products):
        if value.id == id:
            list_products[index] = product
            found = True
    
    if not found:
        raise HTTPException(status_code= 404, detail= "NO SE ENCONTRO EL PRODUCTO")

@app.delete("/products/{id}")
async def delete_products(id: int):
    
    found = False
    
    for index, value in enumerate(list_products):
        if value.id == id:
            del list_products[index]
            found = True
    
    if not found:
        raise HTTPException(status_code= 404, detail= "NO SE ENCONTRO EL PRODUCTO")
    
    return {"message": "Producto eliminado correctamente"}


def search_id(id: int):
    for product in list_products:
        if product.id == id:
            return product
    return None
