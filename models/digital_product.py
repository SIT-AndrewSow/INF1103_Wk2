from models.product import Product


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
            dict_item["transaction_history"],
        )
