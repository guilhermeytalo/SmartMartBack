from sqlalchemy.orm import Session
from app.infrastructure.db.models.product import ProductModel
from app.interfaces.dtos.product_dto import ProductResponseDTO
from app.domain.services.profit_calculator import calculate_profit


def list_products(db: Session, skip: int = 0, limit: int = 10):
    total = db.query(ProductModel).count()

    products = db.query(ProductModel).offset(skip).limit(limit).all()
    items = []

    for product in products:
        product_data = ProductResponseDTO.model_validate(product)
        profit = calculate_profit(product.price, product.quantity)
        product_dict = product_data.model_dump()
        product_dict["profit"] = profit
        items.append(product_dict)

    return {
        "items": items,
        "total": total
    }

