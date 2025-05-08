from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.db.database import get_db
from app.interfaces.dtos.product_dto import ProductCreateDTO, ProductResponseDTO, CategoryRefDTO
from app.infrastructure.db.models.product import ProductModel
from app.infrastructure.db.models.category import CategoryModel

router = APIRouter(tags=["Products"])

@router.post("/products", response_model=ProductResponseDTO)
def create_product(
    product_data: ProductCreateDTO, 
    db: Session = Depends(get_db)
):
     
    if isinstance(product_data.category, CategoryRefDTO):
        
        if product_data.category.id:
            category = db.query(CategoryModel).get(product_data.category.id)
        else:
            category = db.query(CategoryModel).filter_by(
                name=product_data.category.name
            ).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found. Provide a valid ID/name or create a new one."
            )
    else:
        
        existing_category = db.query(CategoryModel).filter_by(
            name=product_data.category.name
        ).first()
        
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category '{product_data.category.name}' already exists."
            )
        
        category = CategoryModel(**product_data.category.model_dump())
        db.add(category)
        db.flush() 

    
    product = ProductModel(
        **product_data.model_dump(exclude={"category"}),
        category_id=category.id
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product