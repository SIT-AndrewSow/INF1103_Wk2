from abc import ABC, abstractmethod


class Product(ABC):
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

    # display product information
    @abstractmethod
    def display_information(self):
        return f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.quantity}"

    # display a message explaining  that the product requires type of shipping
    @abstractmethod
    def get_fulfilment_info(self):
        pass

    @abstractmethod
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
    @abstractmethod
    def from_dict(cls, dict_item):
        pass
        # return cls(d["id"], d["name"], d["price"], d["quantity"], d["transaction_history"])


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(
        self, product_id, name, price, quantity, weight, transaction_history=None
    ):
        super().__init__(product_id, name, price, quantity, transaction_history)
        self.weight = weight

    def display_information(self):
        return super().display_information() + f"| Weight: {self.weight}KG"

    def get_fulfilment_info(self):
        return "This product requires physical shipping"

    # base fee + rate per kg
    def calculate_shipping_cost(self):
        base_fee = 5.00
        rate_per_kg = 2.50
        return base_fee + (rate_per_kg * self.quantity * self.weight)

    def to_dict(self):
        physical_product = super().to_dict()
        physical_product["weight"] = self.weight
        physical_product["type"] = "physical"
        return physical_product

    @classmethod
    def from_dict(cls, dict_item):
        return cls(
            dict_item["id"],
            dict_item["name"],
            dict_item["price"],
            dict_item["quantity"],
            dict_item["weight"], 
            dict_item["transaction_history"],
        )


class DigitalProduct(Product):
    def __init__(
        self, product_id, name, price, quantity, download_size, transaction_history=None
    ):
        super().__init__(product_id, name, price, quantity, transaction_history)
        self.download_size = download_size

    def display_information(self):
        return (
            super().display_information() + f"| Download Size: {self.download_size}MB"
        )

    def get_fulfilment_info(self):
        return "This product is delivered digitally"

    def to_dict(self):
        physical_product = super().to_dict()
        physical_product["download_size"] = self.download_size
        physical_product["type"] = "digital"
        return physical_product

    @classmethod
    def from_dict(cls, dict_item):
        return cls(
            dict_item["id"],
            dict_item["name"],
            dict_item["price"],
            dict_item["quantity"],
            dict_item["download_size"],
            dict_item["transaction_history"]
        )
