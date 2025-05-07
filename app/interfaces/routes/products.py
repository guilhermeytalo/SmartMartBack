from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ProductDTO(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: str
    brand: str

@router.post("/products")
def create_product(product: ProductDTO):
    profit = product.price - product.cost
    return {"msg": "Produto criado", "profit": profit}
