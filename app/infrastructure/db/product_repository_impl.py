from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.db.models.product import ProductModel

class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product) -> Product:
        db_product = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
            category_id=product.category_id,
            brand=product.brand
        )
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)

        return Product(
            id=db_product.id,
            name=db_product.name,
            description=db_product.description,
            price=db_product.price,
            quantity=db_product.quantity,
            category_id=db_product.category_id,
            brand=db_product.brand
        )

    def get_by_id(self, id: int) -> Optional[Product]:
        db_product = self.db.query(ProductModel).filter(ProductModel.id == id).first()
        if db_product is None:
            return None

        return Product(
            id=db_product.id,
            name=db_product.name,
            description=db_product.description,
            price=db_product.price,
            quantity=db_product.quantity,
            category_id=db_product.category_id,
            brand=db_product.brand
        )

    def get_all(self) -> List[Product]:
        db_products = self.db.query(ProductModel).all()
        return [
            Product(
                id=p.id,
                name=p.name,
                description=p.description,
                price=p.price,
                quantity=p.quantity,
                category_id=p.category_id,
                brand=p.brand
            )
            for p in db_products
        ]