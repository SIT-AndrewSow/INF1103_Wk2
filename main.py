# Imports
from product import PhysicalProduct
from inventory import Inventory
from icecream import ic

# Global Constants
INVENTORY_FILE = "inventory.json"
MAX_CAPACITY = 500
TAX_RATE = 0.1  # 10%


# ---------------------------------------------------------------
# User interface
# ---------------------------------------------------------------
def get_menu_option():
    print(
        "\n----------- MENU -----------"
        "\n1. Display All Products"
        "\n2. Add Product"
        "\n3. Update Stock"
        "\n4. Search Product"
        "\n5. Save Inventory"
        "\n6. Exit"
        "\n----------------------------"
    )
    try:
        option_input = int(input("Enter option: "))
    except ValueError:
        print("Invalid Option. Please enter a number from 1 to 6.")
        return None

    if 1 <= option_input <= 6:
        return option_input
    print("Invalid Option. Please enter a number from 1 to 6.")
    return None


# ---------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------
def get_input_float(prompt):
    try:
        input_price = float(input(prompt))
    except ValueError:
        return None
    if input_price >= 0:
        return input_price
    return None


def get_input_int(prompt):
    input_quantity = input(prompt)
    if not input_quantity.isdecimal():
        return None
    input_quantity = int(input_quantity)
    if input_quantity <= MAX_CAPACITY:
        return input_quantity
    return None


def choose_option(prompt, valid_options):
    choice = input(f"{prompt} ({'/'.join(valid_options)}): ").strip().lower()
    if choice in valid_options:
        return choice
    print(f"Invalid choice. Please select from {valid_options}.")
    return None


# ---------------------------------------------------------------
# Menu actions. Each returns True if accepted, False if rejected.
# ---------------------------------------------------------------
def add_product(inventory):
    print("\nAdd New Product")

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return False

    price = get_input_float("Price: ")
    if price is None:
        print("Invalid price. Please enter a number of 0 or more.")
        return False

    quantity = get_input_int("Stock Quantity: ")
    if quantity is None:
        print(
            f"Invalid quantity. Please enter a whole number from 0 to {MAX_CAPACITY}."
        )
        return False

    product_type = choose_option("Select product type", ["physical", "digital"])
    if not product_type:
        return False

    # weight/download size
    weight, download_size = 0, 0
    if product_type == "physical":
        weight = get_input_float("Weight: ")
        if weight is None:
            print("Invalid weight. Please enter a number of 0 or more.")
            return False
    elif product_type == "digital":
        download_size = get_input_float("Download Size: ")
        if download_size is None:
            print("Invalid download size. Please enter a number of 0 or more.")
            return False

    # Check if item exist alr and attempt to add on if not maxed
    existing = inventory.find_by_name(name)
    if existing is not None and existing.quantity + quantity > MAX_CAPACITY:
        print(f"Rejected: total stock for {existing.name} would exceed {MAX_CAPACITY}.")
        return False

    # Add product to inventory here
    product, is_new = inventory.add_or_restock(
        product_type, name, price, quantity, weight=weight, download_size=download_size
    )
    if is_new:
        print("Product added successfully!")
    else:
        print(
            f"{product.name} already exists (ID: {product.id}). "
            f"Stock increased to {product.quantity}."
        )
    return True


def update_stock(inventory):
    print("\nUpdate Stock")
    product = inventory.find_by_id(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return False

    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.quantity}")

    new_quantity = get_input_int("New Stock Quantity: ")
    if new_quantity is None:
        print(
            f"Invalid quantity. Please enter a whole number from 0 to {MAX_CAPACITY}."
        )
        return False

    product.set_quantity(new_quantity)
    print("Stock updated successfully!")
    return True


def search_product(inventory):
    print("\nSearch Product")
    product = inventory.find_by_id(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return False

    print("Product Found")
    print("-" * 100)
    product_str = product.display_information() + " | " + product.get_fulfilment_info()
    if isinstance(product, PhysicalProduct):
        product_str += f" | Shipping Cost: ${product.calculate_shipping_cost():.2f}"
    print(product_str)
    print("-" * 100)
    return True


# ---------------------------------------------------------------
# Main function
# ---------------------------------------------------------------
def main():
    failed_entries = 0

    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = Inventory.load(INVENTORY_FILE)

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
                if inventory.save(INVENTORY_FILE):
                    print(f"Inventory saved successfully to {INVENTORY_FILE}.")
            case 6:
                inventory.generate_report(failed_entries)
                print("\nSaving inventory before exit...")
                if inventory.save(INVENTORY_FILE):
                    print(f"Inventory saved successfully to {INVENTORY_FILE}.")
                print("Program terminated.")
                break
            case _:
                # invalid menu input (message already shown by get_menu_option)
                failed_entries += 1


if __name__ == "__main__":
    main()
