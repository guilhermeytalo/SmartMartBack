from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.database import get_db
from app.interfaces.dtos.product_dto import CategoryResponseDTO

router = APIRouter(tags=["Categories"])

@router.get('/categories', response_model=list[CategoryResponseDTO])
def get_categories(db: Session = Depends(get_db)):
    from app.application.use_cases.list_categories import list_categories
    return list_categories(db)