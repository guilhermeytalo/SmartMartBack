from sqlalchemy.orm import Session

from app.infrastructure.db.models.category import CategoryModel
from app.interfaces.dtos.product_dto import CategoryResponseDTO


def list_categories(db: Session):
    categories = db.query(CategoryModel).all()
    result = []
    for category in categories:
        category_data = CategoryResponseDTO.model_validate(category)
        category_dict = category_data.model_dump()
        result.append(category_dict)

    return result
