from pydantic import BaseModel, Field
from typing import Optional

class ProductCreateDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category_id: Optional[int] = None
    brand: str
    quantity: int = 0

class ProductResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category_id: Optional[int] = None
    brand: str
    quantity: int = 0
    
    class Config:
        from_attributes = True  # Allow reading directly from ORM objects