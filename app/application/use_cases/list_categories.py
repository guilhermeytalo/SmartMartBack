from sqlalchemy.orm import Session

from app.infrastructure.db.models.category import CategoryModel
from app.infrastructure.db.models.product import ProductModel
from app.interfaces.dtos.product_dto import ProductResponseDTO, CategoryResponseDTO
from app.domain.services.profit_calculator import calculate_profit


def list_categories(db: Session):
    categories = db.query(CategoryModel).all()
    result = []
    for category in categories:
        category_data = CategoryResponseDTO.model_validate(category)
        category_dict = category_data.model_dump()
        result.append(category_dict)

    return result
