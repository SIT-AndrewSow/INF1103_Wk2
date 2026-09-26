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


def generate_report(transaction_history, failed_entries):
    print(f"Total Transactions Processed:{len(transaction_history)} and the number of Failed/Rejected Entries:{failed_entries}.")
    print(f"\n-----------\nTRANSACTION HISTORY:\n-----------\n")
    return


def load_inventory():
    # check if json exist if not return empty
    try:
        with open("inventory.json", "r", encoding="utf-8") as file:
            loaded_data = json.load(file)

        inventory = loaded_data["inventory"]
        transaction_history = loaded_data["transaction_history"]
        return inventory, transaction_history
    except FileNotFoundError:
        return [], []


def save_inventory(inventory, transaction_history):
    combined_data = {
        "inventory": inventory,
        "transaction_history": transaction_history
    }
    
    # Write the inventory list first
    with open("inventory.json", "w", encoding="utf-8") as file:
        json.dump(combined_data, file, indent=4)


def main():
    # local variables
    inventory = 0
    failed_entries = 0
    inventory = []
    transaction_history = []
    
    # try to load existing data first
    (inventory, transaction_history) = load_inventory()
    
    while True:
        (product, quantity) = get_valid_input()
        
        # check if quit or quantity is invalid
        if product == "quit":
            # save existing inventory and transaction history
            save_inventory(inventory, transaction_history)
            
            # generate_report(deliveries_count, failed_entries)
            print(inventory)
            break
        elif product == "invalid":
            print("Invalid input. Please enter a valid positive number.")
            failed_entries += 1
            continue
        
        
        # pass the name, quantity and the current inventory list
        curr_item = process_delivery(product, quantity, inventory)
        transaction_history.append(curr_item)
        print(f"\nNew Order Added:\nID:{curr_item[0]}, {curr_item[1]}, {curr_item[2]}\n")
    
    
if __name__=="__main__":
    main()