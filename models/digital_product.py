from typing import Any

from models.product import Product
from models.supplier import Supplier


class DigitalProduct(Product):
    def __init__(
        self,
        product_id: int | str,
        name: str,
        price: float,
        quantity: int,
        download_size: float,
        supplier: Supplier,
        transaction_history: list[int] | None = None
    ) -> None:
        super().__init__(product_id, name, price, quantity, supplier, transaction_history)
        self.download_size: float = download_size

    def display_information(self) -> str:
        return (
            super().display_information() + f"| Download Size: {self.download_size}MB"
        )

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally"

    def to_dict(self) -> dict[str, object]:
        physical_product = super().to_dict()
        physical_product["download_size"] = self.download_size
        physical_product["type"] = "digital"
        return physical_product

    @classmethod
    def from_dict(cls, dict_item: dict[str, Any]) -> "DigitalProduct":
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
            dict_item["download_size"],
            supplier,
            dict_item.get("transaction_history"),
        )
