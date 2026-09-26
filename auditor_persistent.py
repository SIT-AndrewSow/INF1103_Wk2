# Imports
import json

# Global Constant
MAX_CAPACITY = 500
TAX_RATE = 0.1 # 10% tax rate
# Define data structure
ITEM_FIELDS = {
    "id": 0,
    "name": 1,
    "quantity": 2,
    "transaction_history": 3
}

# get input for product name, quantity and validate
def get_valid_input():
    # Get product name and quantity
    input_name = input("Enter product name: ")
    if input_name == "quit":
        return "quit", 0
    
    input_quantity = input("Enter a stock quantity: ")
    if input_quantity == "quit":
        return "quit", 0
    
    # check if the input is a number
    if not input_quantity.isdigit():
        return "invalid", 0
    
    return input_name, int(input_quantity)


# check item
def find_item(product, inventory):
    for item in inventory:
        if item[ITEM_FIELDS["name"]].lower() == product.lower():
            return item[ITEM_FIELDS["id"]]
    return False


# Check if item exist in the list if not just add append to items
def process_delivery(product, quantity, inventory):
    
    # find if the same item exist in the inventory
    item_id = find_item(product, inventory)
    
    if item_id is False:
        # create a new item
        item_id = len(inventory)
        inventory.append([item_id, product, quantity, [quantity]])
    else:
        # item exist, so append!
        inventory[item_id][ITEM_FIELDS["transaction_history"]].append(quantity)
        inventory[item_id][ITEM_FIELDS["quantity"]] += quantity
        
    # return the item for transaction history
    return [item_id, product, quantity]


def calculate_tax(amount):
    return amount * TAX_RATE


def generate_report(inventory, failed_entries):
    print(f"\nThe number of Failed/Rejected Entries:{failed_entries}.")
    
    #print inventory
    print(f"\n-----------------\nINVENTORY\n-----------------\n")
    for item in inventory:
        print(f"ID: {item[ITEM_FIELDS["id"]]}. Product: {item[ITEM_FIELDS["name"]]}, Quantity: {item[ITEM_FIELDS["quantity"]]}, Transaction History: {", ".join(str(i) for i in item[ITEM_FIELDS["transaction_history"]])}\n")
    return


def load_inventory():
    # check if json exist if not return empty
    try:
        with open("inventory.json", "r", encoding="utf-8") as file:
            inventory = json.load(file)
        return inventory
    except FileNotFoundError:
        return []


def save_inventory(inventory):
    # Write the inventory list first
    with open("inventory.json", "w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=4)


def main():
    # local variables
    inventory = 0
    failed_entries = 0
    inventory = []
    
    # try to load existing data first
    inventory = load_inventory()
    
    while True:
        (product, quantity) = get_valid_input()
        
        # check if quit or quantity is invalid
        if product == "quit":
            generate_report(inventory, failed_entries)
            
            # save existing inventory and transaction history
            save_inventory(inventory)
            break
        elif product == "invalid":
            print("Invalid input. Please enter a valid positive number.")
            failed_entries += 1
            continue
        
        # pass the name, quantity and the current inventory list
        curr_item = process_delivery(product, quantity, inventory)
        print(f"\nNew Order Added:\nID:{curr_item[0]}, {curr_item[1]}, {curr_item[2]}\n")
    
    
if __name__=="__main__":
    main()