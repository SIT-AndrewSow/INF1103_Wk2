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

    def __init__(self, products=None):
        self.products: list[Product] = products if products is not None else []

    # ---------------------------------------------------------------
    # Find id helper
    # ---------------------------------------------------------------
    def count_products(self):
        return len(self.products)

    def next_id(self):
        # max + 1 (not len) so IDs stay unique even if products are ever deleted
        if not self.products:
            return 0
        return max(p.id for p in self.products) + 1

    def find_product_by_id(self, product_id) -> Product | None:
        if not product_id.isdecimal():
            return None
        for p in self.products:
            if p.id == int(product_id):
                return p
        return None

    def find_product_by_name(self, name):
        for p in self.products:
            if p.name.lower() == name.lower():
                return p
        return None

    # ---------------------------------------------------------------
    # Important functions
    # ---------------------------------------------------------------
    def add_or_restock(self, type, name, price, quantity, weight=0, download_size=0) -> None:
        """Returns (product, is_new)."""
        existing = self.find_product_by_name(name)

        # if it does not exist add new
        if existing is None:
            product = None
            # add based on product type
            if type == "physical":
                product = PhysicalProduct(self.next_id(), name, price, quantity, weight)
            elif type == "digital":
                product = DigitalProduct(
                    self.next_id(), name, price, quantity, download_size
                )

            self.products.append(product)
            return product, True

        # if it exist update the stock
        existing.add_stock(quantity, price)
        return existing, False

    def remove_product_by_id(self, product_id: str | int) -> Product | None:
        for idx, p in enumerate(self.products):
            if str(p.id) == str(product_id):
                return self.products.pop(idx)
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 100)
        if not self.products:
            print("No products in inventory.")
        for product in self.products:
            product_str = (
                product.display_information() + " | " + product.get_fulfilment_info()
            )
            if isinstance(product, PhysicalProduct):
                product_str += (
                    f" | Shipping Cost: ${product.calculate_shipping_cost():.2f}"
                )
            print(product_str)
        print("-" * 100)

    def generate_report(self, failed_entries):
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
    def save(self, inventory_file):
        try:
            with open(inventory_file, "w", encoding="utf-8") as f:
                json.dump([p.to_dict() for p in self.products], f, indent=4)
        except OSError as e:
            print(f"Could not save inventory: {e}")
            return False
        return True

    @classmethod
    def load(cls, inventory_file):
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
