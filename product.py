class Product:
    """Data and behaviour for a single item."""

    def __init__(self, product_id, name, price, quantity, transaction_history=None):
        self.id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.transaction_history = (
            transaction_history if transaction_history is not None else [quantity]
        )

    def add_stock(self, amount, new_price):
        """Record a delivery: more stock and an updated price."""
        self.transaction_history.append(amount)
        self.quantity += amount
        self.price = new_price

    def set_quantity(self, new_quantity):
        """Set stock to a new value, recording the change (e.g. +10 or -5)."""
        change = new_quantity - self.quantity
        self.quantity = new_quantity
        if change != 0:
            self.transaction_history.append(change)

    def to_dict(self):
        """JSON can't save objects directly, so convert to a dict."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "transaction_history": self.transaction_history,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["name"], d["price"], d["quantity"], d["transaction_history"])

    def __str__(self):
        return (f"ID: {self.id} | Name: {self.name} | "
                f"Price: ${self.price:.2f} | Stock: {self.quantity}")


class PhysicalProduct(Product):
    pass


class DigitalProduct(Product):
    pass