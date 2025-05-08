from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, name: str, description: str, price: float,
                quantity: int, brand: str, category_id: int = None) -> Product:
        product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            brand=brand,
            category_id=category_id
        )

        return self.product_repository.create(product)
