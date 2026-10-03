# Imports
import json

# Global Constant
INVENTORY_FILE = "inventory.json"
MAX_CAPACITY = 500
TAX_RATE = 0.1 # 10% 

# Menu options
def getMenuOption():
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
        if option_input >= 1 and option_input <=6:
            return option_input
        else:
            return None
    except ValueError:
        print("Invalid Option. Please enter a number from 1 to 6.");
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
def process_delivery(product_id, product, price, quantity, inventory):
    item = find_by_name(product, inventory)

    if item is None:
        # create a new item
        item = {
            "id": product_id,
            "name": product,
            "price": price,
            "quantity": quantity,
            "transaction_history": [quantity],
        }
        inventory.append(item)
        return item, True

    # item exists, so append to its history and update stock and price
    item["transaction_history"].append(quantity)
    item["quantity"] += quantity
    item["price"] = price
    return item, False

def add_product(inventory):
    #Returns True if the entry was accepted, False if it was rejected.
    print("\nAdd New Product")
    name = input("Product Name: ")

    # Get product name
    if not name:
        print("Product name cannot be empty.")
        return False

    # Get/update price
    price = get_input_price("Price: ")
    if price is None:
        print("Invalid price. Please enter a number of 0 or more.")
        return False

    # Get/update quantity
    quantity = get_input_quantity("Stock Quantity: ")
    if quantity is None:
        print(f"Invalid quantity. Please enter a whole number from 0 to {MAX_CAPACITY}.")
        return False

    # exceed max cap
    existing = find_by_name(name, inventory)
    if existing is not None and existing["quantity"] + quantity > MAX_CAPACITY:
        print(f"Rejected: total stock for {existing['name']} would exceed {MAX_CAPACITY}.")
        return False

    product_id = len(inventory)
    item, is_new = process_delivery(product_id, name, price, quantity, inventory)
    if is_new:
        print("Product added successfully!")
    else:
        print(f"{item['name']} already exists (ID: {item['id']}). "
              f"Stock increased to {item['quantity']}.")
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




# Inventory Lookups
def find_by_id(product_id, inventory):
    if not product_id.isdecimal():
        return None
    for item in inventory:
        if item["id"] == int(product_id):
            return item
    return None

def find_by_name(product_name, inventory):
    for item in inventory:
        if item["name"].lower() == product_name.lower():
            return item
    return None


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


# Load and Save inventory data
def load_inventory():
    # check if json exist if not return empty
    try:
        with open("inventory.json", "r", encoding="utf-8") as file:
            inventory = json.load(file)
    except FileNotFoundError:
        print("Inventory file not found. Start with empty inventory")
        return []
    
    print("Invenotory loaded successfully")
    return inventory

def save_inventory(inventory):
    # Write the inventory list first
    with open("inventory.json", "w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=4)


# Main function
def main():
    # local variables
    failed_entries = 0
    
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    
    inventory = load_inventory()
    
    while True:
        # prompt option
        option = getMenuOption()
        
        match option:
            # all case that is not 1-6
            case 1:
                display_all(inventory)
            case 2:
                if not add_product(inventory):
                    failed_entries += 1
            case 3:
                if not update_stock(inventory):
                    failed_entries += 1
            case 4:
                return
            case 5:
                print("\nSaving inventory...")
                if save_inventory(inventory):
                    print(f"Inventory saved successfully to {INVENTORY_FILE}.")
            case 6:
                generate_report(inventory, failed_entries)
                print("\nSaving inventory before exit...")
                if save_inventory(inventory):
                    print("Inventory saved successfully.")
                print("Program terminated.")
                break
            case _:
                # invalid menu input (message already shown by getMenuOption)
                failed_entries += 1
    
    
# Call Main
if __name__=="__main__":
    main()