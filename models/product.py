from abc import ABC, abstractmethod
from typing import Any

from models.supplier import Supplier


class Product(ABC):
    def __init__(
        self,
        product_id: int | str,
        name: str,
        price: float,
        quantity: int,
        supplier: Supplier,
        transaction_history: list[int] | None = None,
    ) -> None:
        self.id: int | str = product_id
        self.name: str = name
        self.price: float = price
        self.quantity: int = quantity
        self.supplier: Supplier = supplier
        self.transaction_history: list[int] = (
            transaction_history if transaction_history is not None else [quantity]
        )

    def add_stock(self, amount: int, new_price: float) -> None:
        """Record a delivery: more stock and an updated price."""
        self.transaction_history.append(amount)
        self.quantity += amount
        self.price = new_price

    def set_quantity(self, new_quantity: int) -> None:
        """Set stock to a new value, recording the change (e.g. +10 or -5)."""
        change = new_quantity - self.quantity
        self.quantity = new_quantity
        if change != 0:
            self.transaction_history.append(change)

    # display product information
    @abstractmethod
    def display_information(self) -> str:
        return (
            f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | "
            f"Stock: {self.quantity} | Supplier: {self.supplier.name}"
        )

    # display a message explaining  that the product requires type of shipping
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, object]:
        """JSON can't save objects directly, so convert to a dict."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "transaction_history": self.transaction_history,
            "supplier": {
                "supplier_id": self.supplier.supplier_id,
                "name": self.supplier.name,
                "contact_email": self.supplier.contact_email,
            }
            if self.supplier is not None
            else None,
        }

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_item: dict[str, Any]) -> "Product":
        pass