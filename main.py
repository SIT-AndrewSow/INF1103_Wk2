# Imports
from models.physical_product import PhysicalProduct
from models.digital_product import DigitalProduct
from models.supplier import Supplier
from models.supplier_manager import SupplierManager
from models.inventory import Inventory

# Global Constants
INVENTORY_FILE = "inventory.json"
SUPPLIERS_FILE = "suppliers.json"
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
        "\n3. Add Supplier"
        "\n4. Update Stock"
        "\n5. Search Product"
        "\n6. Save Inventory"
        "\n7. Display All Suppliers"
        "\n8. Exit"
        "\n----------------------------"
    )
    try:
        option_input = int(input("Enter option: "))
    except ValueError:
        print("Invalid Option. Please enter a number from 1 to 8.")
        return None

    if 1 <= option_input <= 8:
        return option_input
    print("Invalid Option. Please enter a number from 1 to 8.")
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


def get_supplier_for_product(supplier_manager: SupplierManager) -> Supplier | None:
    """Prompt user to choose an existing supplier or enter a new supplier."""
    supplier_list = supplier_manager.get_all_suppliers()

    if supplier_list:
        print("\nSupplier Options:")
        print("1. Select an existing supplier")
        print("2. Enter a new supplier")
        choice = choose_option("Choose option", ["1", "2"])
        if choice == "1":
            print("\nExisting Suppliers:")
            for idx, s in enumerate(supplier_list, start=1):
                print(f"[{idx}] {s.display_information()}")
            sel_input = input(
                f"Select supplier (1-{len(supplier_list)} or enter Supplier ID): "
            ).strip()
            if sel_input.isdigit():
                sel = int(sel_input)
                if 1 <= sel <= len(supplier_list):
                    return supplier_list[sel - 1]
            for s in supplier_list:
                if s.supplier_id.lower() == sel_input.lower():
                    return s
            print("Invalid supplier selection.")
            return None
        elif choice != "2":
            return None

    # Enter new supplier
    print("\n--- Enter Supplier Details ---")
    supplier_id = input("Supplier ID: ").strip()
    if not supplier_id:
        print("Supplier ID cannot be empty.")
        return None

    existing_supplier = supplier_manager.find_supplier_by_id(supplier_id)
    if existing_supplier:
        print(
            f"Supplier ID '{supplier_id}' already exists ({existing_supplier.name}). Using this supplier."
        )
        return existing_supplier

    supplier_name = input("Supplier Name: ").strip()
    if not supplier_name:
        print("Supplier name cannot be empty.")
        return None

    supplier_email = input("Supplier Contact Email: ").strip()
    if not supplier_email:
        print("Supplier email cannot be empty.")
        return None

    new_supplier = Supplier(supplier_id, supplier_name, supplier_email)
    supplier_manager.add_supplier(new_supplier)
    return new_supplier


def add_supplier(supplier_manager: SupplierManager) -> bool:
    print("\nAdd New Supplier")
    supplier_id = input("Supplier ID: ").strip()
    if not supplier_id:
        print("Supplier ID cannot be empty.")
        return False

    if supplier_manager.find_supplier_by_id(supplier_id) is not None:
        print(f"Supplier with ID '{supplier_id}' already exists.")
        return False

    supplier_name = input("Supplier Name: ").strip()
    if not supplier_name:
        print("Supplier name cannot be empty.")
        return False

    supplier_email = input("Supplier Contact Email: ").strip()
    if not supplier_email:
        print("Supplier email cannot be empty.")
        return False

    supplier = Supplier(supplier_id, supplier_name, supplier_email)
    supplier_manager.add_supplier(supplier)
    print(f"Supplier '{supplier_name}' (ID: {supplier_id}) added successfully!")
    return True


# ---------------------------------------------------------------
# Menu actions. Each returns True if accepted, False if rejected.
# ---------------------------------------------------------------
def add_product(inventory, supplier_manager: SupplierManager):
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

    # Check if item exists already and update stock
    existing = inventory.find_product_by_name(name)
    if existing is not None:
        if existing.quantity + quantity > MAX_CAPACITY:
            print(f"Rejected: total stock for {existing.name} would exceed {MAX_CAPACITY}.")
            return False
        existing.add_stock(quantity, price)
        print(
            f"{existing.name} already exists (ID: {existing.id}). "
            f"Stock increased to {existing.quantity}."
        )
        return True

    # If it is new, obtain supplier details (Association)
    supplier = get_supplier_for_product(supplier_manager)
    if supplier is None:
        print("Product creation cancelled: valid supplier required.")
        return False

    new_id = inventory.next_id()
    if product_type == "physical":
        product = PhysicalProduct(new_id, name, price, quantity, weight, supplier)
    else:
        product = DigitalProduct(new_id, name, price, quantity, download_size, supplier)

    inventory.add_product(product)
    print("Product added successfully!")
    return True


def update_stock(inventory):
    print("\nUpdate Stock")
    product = inventory.find_product_by_id(input("Enter Product ID: "))
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
    product = inventory.find_product_by_id(input("Enter Product ID: "))
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
    supplier_manager = SupplierManager.load(SUPPLIERS_FILE)
    supplier_manager.populate_from_products(inventory.products)

    while True:
        option = get_menu_option()

        match option:
            case 1:
                inventory.display_all()
            case 2:
                if not add_product(inventory, supplier_manager):
                    failed_entries += 1
            case 3:
                if not add_supplier(supplier_manager):
                    failed_entries += 1
            case 4:
                if not update_stock(inventory):
                    failed_entries += 1
            case 5:
                search_product(inventory)
            case 6:
                print("\nSaving inventory and suppliers...")
                inv_saved = inventory.save(INVENTORY_FILE)
                sup_saved = supplier_manager.save(SUPPLIERS_FILE)
                if inv_saved and sup_saved:
                    print(
                        f"Data saved successfully to {INVENTORY_FILE} and {SUPPLIERS_FILE}."
                    )
            case 7:
                supplier_manager.display_all()
            case 8:
                inventory.generate_report(failed_entries)
                print("\nSaving inventory and suppliers before exit...")
                inventory.save(INVENTORY_FILE)
                supplier_manager.save(SUPPLIERS_FILE)
                print("Program terminated.")
                break
            case _:
                # invalid menu input (message already shown by get_menu_option)
                failed_entries += 1


if __name__ == "__main__":
    main()
