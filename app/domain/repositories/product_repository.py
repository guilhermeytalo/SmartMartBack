from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self) -> List[Product]:
        pass
