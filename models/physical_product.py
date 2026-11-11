from models.can_be_shipped import CanBeShipped
from models.product import Product


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
