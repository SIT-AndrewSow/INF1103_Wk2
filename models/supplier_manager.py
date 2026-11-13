import json
from models.supplier import Supplier
from models.product import Product


class SupplierManager:
    """Manages the collection of suppliers independently from Inventory."""

    def __init__(self, suppliers: list[Supplier] | None = None) -> None:
        self.suppliers: list[Supplier] = suppliers if suppliers is not None else []

    def add_supplier(self, supplier: Supplier) -> bool:
        """Add a supplier if a supplier with the same ID does not already exist."""
        for s in self.suppliers:
            if str(s.supplier_id).strip().lower() == str(supplier.supplier_id).strip().lower():
                return False
        self.suppliers.append(supplier)
        return True

    def find_supplier_by_id(self, supplier_id: str) -> Supplier | None:
        """Find a supplier by their ID."""
        for s in self.suppliers:
            if str(s.supplier_id).strip().lower() == str(supplier_id).strip().lower():
                return s
        return None

    def get_all_suppliers(self) -> list[Supplier]:
        """Return the list of all registered suppliers."""
        return list(self.suppliers)

    def populate_from_products(self, products: list[Product]) -> None:
        """Collect and register any suppliers attached to products."""
        for p in products:
            if getattr(p, "supplier", None) is not None:
                self.add_supplier(p.supplier)

    def display_all(self) -> None:
        """Display all registered suppliers."""
        print("\nRegistered Suppliers")
        print("-" * 60)
        if not self.suppliers:
            print("No suppliers registered.")
        for idx, s in enumerate(self.suppliers, start=1):
            print(f"[{idx}] {s.display_information()}")
        print("-" * 60)

    def save(self, filepath: str = "suppliers.json") -> bool:
        """Save suppliers list to a JSON file."""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                data = [
                    {
                        "supplier_id": s.supplier_id,
                        "name": s.name,
                        "contact_email": s.contact_email,
                    }
                    for s in self.suppliers
                ]
                json.dump(data, f, indent=4)
        except OSError as e:
            print(f"Could not save suppliers: {e}")
            return False
        return True

    @classmethod
    def load(cls, filepath: str = "suppliers.json") -> "SupplierManager":
        """Load suppliers list from a JSON file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                suppliers = [
                    Supplier(
                        item["supplier_id"],
                        item["name"],
                        item["contact_email"],
                    )
                    for item in data
                    if isinstance(item, dict)
                    and "supplier_id" in item
                    and "name" in item
                    and "contact_email" in item
                ]
                return cls(suppliers)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return cls([])
