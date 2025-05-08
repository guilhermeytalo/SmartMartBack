from pydantic import BaseModel, Field
from typing import Optional, Union

class CategoryCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class CategoryRefDTO(BaseModel):
    id: Optional[int] = None  # Use ID if available
    name: Optional[str] = None  # Fallback to name if ID missing

class ProductCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    brand: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(0, ge=0)
    category: Union[CategoryRefDTO, CategoryCreateDTO]  # Accepts either existing or new category

class ProductResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category_id: Optional[int] = None  
    brand: str
    quantity: int
    
    class Config:
        from_attributes = True 