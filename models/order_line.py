from models.product import Product

class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_line(self) -> str:
        return (
            f"Product: {self.product.name} | Qty: {self.quantity} | "
            f"Subtotal: ${self.calculate_subtotal():.2f}"
        )