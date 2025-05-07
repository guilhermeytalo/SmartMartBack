from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.db.database import get_db
from app.interfaces.dtos.product_dto import ProductCreateDTO, ProductResponseDTO
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.db.product_repository_impl import SQLAlchemyProductRepository
from app.application.use_cases.create_product import CreateProductUseCase

router = APIRouter(tags=["Products"])

@router.post("/products", response_model=ProductResponseDTO)
def create_product(product_dto: ProductCreateDTO, db: Session = Depends(get_db)):
    # Create repository with db session
    product_repository = SQLAlchemyProductRepository(db)
    
    # Create and execute use case
    use_case = CreateProductUseCase(product_repository)
    product = use_case.execute(
        name=product_dto.name,
        description=product_dto.description,
        price=product_dto.price,
        quantity=product_dto.quantity,
        category_id=product_dto.category_id
    )
    
    # Return response
    return ProductResponseDTO(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id
    )