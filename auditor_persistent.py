# Imports
import json

# Global Constant
INVENTORY_FILE = "inventory.json"
MAX_CAPACITY = 500
TAX_RATE = 0.1 # 10% 

class Product:
    def __init__(self, product_id, name, price, quantity, transaction_history=None):
        self.id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.transaction_history = (
            transaction_history if transaction_history is not None else [quantity]
        )
        
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

class Inventory:
    def __init__(self, products=None):
        self.products = products if products is not None else []
    
    # stores product
    # adds product
    # searches product
    
    def count_products(self):
        return len(self.products)
    
    def add_or_restock(self, name, price, quantity):
            existing = self.find_by_name(name)
            if existing is None:
                product = Product(self.next_id(), name, price, quantity)
                self.products.append(product)
                return product, True
            existing.add_stock(quantity, price)
            return existing, False
    
    def find_by_id(self, product_id):
        if not product_id.isdecimal():
            return None
        for p in self.products:
            if p.id == int(product_id):
                return p
        return None

    def find_by_name(self, name):
        for p in self.products:
            if p.name.lower() == name.lower():
                return p
        return None
    
    def display_all(self):
            print("\nCurrent Inventory")
            print("-" * 48)
            if not self.products:
                print("No products in inventory.")
            for p in self.products:
                print(p)
            print("-" * 48)
    
    def save(self):
        try:
            with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
                json.dump([p.to_dict() for p in self.products], f, indent=4)
        except OSError as e:
            print(f"Could not save inventory: {e}")
            return False
        return True

    @classmethod
    def load(cls):
        try:
            with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
                inventory = cls([Product.from_dict(d) for d in json.load(f)])
        except FileNotFoundError:
            print("Inventory file not found. Starting with empty inventory.")
            return cls()
        except (json.JSONDecodeError, KeyError):
            print("Inventory file is corrupted. Starting with empty inventory.")
            return cls()

        print("Inventory loaded successfully.")
        return inventory

# Menu options
def get_menu_option():
    print("\n----------- MENU -----------"+
        "\n1. Display All Products"+
        "\n2. Add Product" + 
        "\n3. Update Stock" + 
        "\n4. Search Product" + 
        "\n5. Save Inventory" + 
        "\n6. Exit" +
        "\n----------------------------")
    try:
        option_input = int(input("Enter option: "))
    except ValueError:
        print("Invalid Option. Please enter a number from 1 to 6.")
        return None

    if 1 <= option_input <= 6:
        return option_input
    print("Invalid Option. Please enter a number from 1 to 6.")
    return None
    

#input helper
def get_input_price(prompt):
    try:
        input_price = float(input(prompt))
    except ValueError:
        return None
    if input_price >= 0:
        return input_price
    return None

def get_input_quantity(prompt):
    input_quantity = input(prompt)
    if not input_quantity.isdecimal():
        return None
    input_quantity = int(input_quantity)
    if input_quantity <= MAX_CAPACITY:
        return input_quantity
    return None


#Menu Options
def add_product(inventory):
    print("\nAdd New Product")
    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return False

    price = get_input_price("Price: ")
    if price is None:
        print("Invalid price. Please enter a number of 0 or more.")
        return False

    quantity = get_input_quantity("Stock Quantity: ")
    if quantity is None:
        print(f"Invalid quantity. Please enter a whole number from 0 to {MAX_CAPACITY}.")
        return False

    existing = inventory.find_by_name(name)
    if existing is not None and existing.quantity + quantity > MAX_CAPACITY:
        print(f"Rejected: total stock for {existing.name} would exceed {MAX_CAPACITY}.")
        return False

    product, is_new = inventory.add_or_restock(name, price, quantity)
    if is_new:
        print("Product added successfully!")
    else:
        print(f"{product.name} already exists (ID: {product.id}). "
              f"Stock increased to {product.quantity}.")
    return True

def update_stock(inventory):
    print("\nUpdate Stock")
    
    # Get/update price
    product_id = input("Enter Product ID: ")
    
    item = find_by_id(product_id, inventory)
    if item is None:
        print("Product not found.")
        return False

    print("Product Found:")
    print(f"Name: {item['name']}")
    print(f"Current Stock: {item['quantity']}")

    new_quantity = get_input_quantity("New Stock Quantity: ")
    if new_quantity is None:
        print(f"Invalid quantity. Please enter a whole number from 0 to {MAX_CAPACITY}.")
        return False

    # record the change (e.g. +10 or -5) so the history still adds up to the stock
    change = new_quantity - item["quantity"]
    item["quantity"] = new_quantity
    if change != 0:
        item["transaction_history"].append(change)

    print("Stock updated successfully!")
    return True

def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ")
        
    item = find_by_id(product_id, inventory)
    if item is None:
        print("Product not found.")
        return False

    print("Product Found")
    print("-" * 48)
    print(f"ID: {item['id']}")
    print(f"Name: {item['name']}")
    print(f"Price: ${item['price']:.2f}")
    print(f"Stock: {item['quantity']}")
    print("-" * 48)


# General Display Data
def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("No products in inventory.")
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | "
              f"Price: ${item['price']:.2f} | Stock: {item['quantity']}")
    print("-" * 48)

def generate_report(inventory, failed_entries):
    print(f"\nThe number of Failed/Rejected Entries: {failed_entries}.")

    print("\n-----------------\nTRANSACTION HISTORY\n-----------------")
    for item in inventory:
        history = ", ".join(str(i) for i in item["transaction_history"])
        print(f"ID: {item['id']}. Product: {item['name']}, "
              f"Quantity: {item['quantity']}, Transaction History: {history}")


# Main function
def main():
    failed_entries = 0

    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = Inventory.load()

    while True:
        option = get_menu_option()

        match option:
            case 1:
                inventory.display_all()
            case 2:
                if not add_product(inventory):
                    failed_entries += 1
            case 3:
                if not update_stock(inventory):
                    failed_entries += 1
            case 4:
                search_product(inventory)
            case 5:
                print("\nSaving inventory...")
                if inventory.save():
                    print(f"Inventory saved successfully to {INVENTORY_FILE}.")
            case 6:
                inventory.generate_report(failed_entries)
                print("\nSaving inventory before exit...")
                if inventory.save():
                    print(f"Inventory saved successfully to {INVENTORY_FILE}.")
                print("Program terminated.")
                break
            case _:
                # invalid menu input (message already shown by get_menu_option)
                failed_entries += 1

   
# Call Main
if __name__=="__main__":
    main()