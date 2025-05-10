from sqlalchemy.orm import Session
from app.infrastructure.db.models.product import ProductModel
from app.interfaces.dtos.product_dto import ProductResponseDTO
from app.domain.services.profit_calculator import calculate_profit


def list_products(db: Session):
    products = db.query(ProductModel).all()
    result = []

    for product in products:
        product_data = ProductResponseDTO.model_validate(product)
        profit = calculate_profit(product.price, product.quantity)
        product_dict = product_data.model_dump()
        product_dict["profit"] = profit
        result.append(product_dict)

    return result
