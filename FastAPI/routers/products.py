from fastapi import APIRouter

router = APIRouter(prefix="/products", responses={404: {"message": "Not found"}}, tags=["products"])

product_list = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 499.99},
    {"id": 3, "name": "Tablet", "price": 299.99},
]

@router.get("/")
async def get_products():
    return product_list

@router.get("/{id}")
async def get_product(id: int):
    return product_list[id]