from models.physical_product import PhysicalProduct
from models.digital_product import DigitalProduct
from models.product import Product
import json


PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


class Inventory:
    """Holds all products and handles lookups, display and saving."""

    def __init__(self, products: list[Product] | None = None) -> None:
        self.products: list[Product] = products if products is not None else []

    # ---------------------------------------------------------------
    # Find id helper
    # ---------------------------------------------------------------
    def count_products(self) -> int:
        return len(self.products)

    def next_id(self) -> int:
        # max + 1 (not len) so IDs stay unique even if products are ever deleted
        if not self.products:
            return 0
        return max(p.id for p in self.products) + 1

    # ---------------------------------------------------------------
    # Aggregation Methods (Lab 8)
    # ---------------------------------------------------------------
    def add_product(self, product: Product) -> None:
        """Add an existing Product object to the inventory (Aggregation)."""
        self.products.append(product)

    def remove_product(self, product_id: str | int) -> Product | None:
        """Remove matching Product reference from inventory without destroying it."""
        for idx, p in enumerate(self.products):
            if str(p.id) == str(product_id):
                return self.products.pop(idx)
        return None

    def find_product(self, product_id: str | int) -> Product | None:
        """Find and return the matching Product, or None if not found."""
        for p in self.products:
            if str(p.id) == str(product_id):
                return p
        return None

    def find_product_by_name(self, name: str) -> Product | None:
        """Find product by case-insensitive name."""
        for p in self.products:
            if p.name.lower() == name.lower():
                return p
        return None

    # Aliases for backward compatibility with main.py
    def find_product_by_id(self, product_id: str | int) -> Product | None:
        return self.find_product(product_id)

    def remove_product_by_id(self, product_id: str | int) -> Product | None:
        return self.remove_product(product_id)

    # ---------------------------------------------------------------
    # Restock / Add Helper
    # ---------------------------------------------------------------
    def add_or_restock(self, product: Product) -> tuple[Product, bool]:
        """
        If a product with the same name exists, restock it.
        Otherwise, add the new product to the inventory.
        Returns (product, is_new).
        """
        existing = self.find_product_by_name(product.name)
        if existing is not None:
            existing.add_stock(product.quantity, product.price)
            return existing, False

        self.add_product(product)
        return product, True

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 100)
        if not self.products:
            print("No products in inventory.")
        for product in self.products:
            product_str = (
                product.display_information() + " | " + product.get_fulfilment_info()
            )
            print(product_str)
        print("-" * 100)

    def generate_report(self, failed_entries: int) -> None:
        print(f"\nThe number of Failed/Rejected Entries: {failed_entries}.")
        print("\n-----------------\nTRANSACTION HISTORY\n-----------------")
        for p in self.products:
            history = ", ".join(str(i) for i in p.transaction_history)
            print(
                f"ID: {p.id}. Product: {p.name}, "
                f"Quantity: {p.quantity}, Transaction History: {history}"
            )

    # ---------------------------------------------------------------
    # Load and Save functions
    # ---------------------------------------------------------------
    def save(self, inventory_file: str) -> bool:
        try:
            with open(inventory_file, "w", encoding="utf-8") as f:
                json.dump([p.to_dict() for p in self.products], f, indent=4)
        except OSError as e:
            print(f"Could not save inventory: {e}")
            return False
        return True

    @classmethod
    def load(cls, inventory_file: str) -> "Inventory":
        try:
            with open(inventory_file, "r", encoding="utf-8") as f:
                inventory = cls(
                    [
                        PRODUCT_TYPES[d["type"]].from_dict(d)
                        for d in json.load(f)
                        if d.get("type") in PRODUCT_TYPES
                    ]
                )
        # error handling
        except FileNotFoundError:
            print("Inventory file not found. Starting with empty inventory.")
            return cls()
        except (json.JSONDecodeError, KeyError):
            print("Inventory file is corrupted. Starting with empty inventory.")
            return cls()

        print("Inventory loaded successfully.")
        return inventory
