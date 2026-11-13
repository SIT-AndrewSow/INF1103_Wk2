from typing import Any

from models.can_be_shipped import CanBeShipped
from models.product import Product
from models.supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    def __init__(
        self,
        product_id: int | str,
        name: str,
        price: float,
        quantity: int,
        weight: float,
        supplier: Supplier,
        transaction_history: list[int] | None = None,
    ) -> None:
        super().__init__(
            product_id, name, price, quantity, supplier, transaction_history
        )
        self.weight: float = weight

    def display_information(self) -> str:
        return super().display_information() + f"| Weight: {self.weight}kg"

    def get_fulfilment_info(self) -> str:
        # Keep your existing fulfilment info (e.g. weight/dimensions) and append shipping cost
        return f"This product requires physical shipping | Shipping Cost: ${self.calculate_shipping_cost():.2f}"

    # base fee + rate per kg
    def calculate_shipping_cost(self) -> float:
        base_fee = 5.00
        rate_per_kg = 2.50
        return base_fee + (rate_per_kg * self.quantity * self.weight)

    def to_dict(self) -> dict[str, object]:
        physical_product = super().to_dict()
        physical_product["weight"] = self.weight
        physical_product["type"] = "physical"
        return physical_product

    @classmethod
    def from_dict(cls, dict_item: dict[str, Any]) -> "PhysicalProduct":
        supplier_data = dict_item.get("supplier")
        if isinstance(supplier_data, dict):
            supplier = Supplier(
                supplier_data.get("supplier_id", "S000"),
                supplier_data.get("name", "Unknown Supplier"),
                supplier_data.get("contact_email", "unknown@supplier.com"),
            )
        else:
            supplier = Supplier("S000", "Generic Supplier", "info@example.com")

        return cls(
            dict_item["id"],
            dict_item["name"],
            dict_item["price"],
            dict_item["quantity"],
            dict_item["weight"],
            supplier,
            dict_item.get("transaction_history"),
        )
