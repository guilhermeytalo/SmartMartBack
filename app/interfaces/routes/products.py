from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ProductDTO(BaseModel):
    name: str
    price: float
    cost: float
    category: str

@router.post("/products")
def create_product(product: ProductDTO):
    profit = product.price - product.cost
    return {"msg": "Produto criado", "profit": profit}
