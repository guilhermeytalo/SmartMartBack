class Product:
    def __init__(self, id: int = None, name: str = None, description: str = None, 
                price: float = 0.0, quantity: int = 0, category_id: int = None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.category_id = category_id
        
    def calculate_value(self) -> float:
        return self.price * self.quantity