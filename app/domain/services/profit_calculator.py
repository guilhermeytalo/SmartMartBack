def calculate_profit(price: float, quantity: int) -> float:
    cost_per_item = price * 0.6
    profit = (price - cost_per_item) * quantity
    return round(profit, 2)
