from models.product import Product
from models.order_line import OrderLine

class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Composition rule: The Order creates and manages its OrderLine instances internally
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order(self) -> None:
        print(f"\n--- Order ID: {self.order_id} ---")
        for line in self.order_lines:
            print(f"  {line.display_line()}")
        print(f"Total: ${self.calculate_total():.2f}")
