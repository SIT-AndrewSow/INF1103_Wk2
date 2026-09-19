# Global Constant
MAX_CAPACITY = 500
TAX_RATE = 0.1 # 10% tax rate


def get_valid_input():
    user_input = input("Enter a stock quantity: ")
    if user_input == "quit":
        return "quit"
    elif not user_input.isdigit():
        return "invalid"
    return int(user_input)


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = 0
    return tax


def generate_report(total_units, failed_entries):
    return


'''
while True:
    
    # check if the inventory limit has been exceeded
    if inventory > 500:
        print("Inventory limit exceeded. Cannot add more stock.")
        break
    
    # check if the user wants to quit
    if stockQuant == "quit": 
        print(f"Total Units Processed:{inventory} and the number of Failed/Rejected Entries:{failedEntries}.")
        break
    
    # check if input is a valid number, isdigit checks for negative sign and returns false
    if not stockQuant.isdigit():
        print("Invalid input. Please enter a valid positive number.")
        failedEntries += 1
    else:
        stockQuant = int(stockQuant)
        inventory += stockQuant
        print(f"Current inventory: {inventory}")

'''
    
def main():
    """
    Main function to run inventory auditor program.
    """
    
    # local variables
    inventory = 0
    tax_amount = 0
    failed_entries  = 0
    exit_program = False
    
    while not exit_program:
        input_res = get_valid_input()
        
        if input_res == "quit":
            print(f"Total Deliveries Processed:{inventory} and the number of Failed/Rejected Entries:{failed_entries}.")
            break
        elif input_res == "invalid":
            print("Invalid input. Please enter a valid positive number.")
            failedEntries += 1
            continue
        
        inventory = process_delivery(inventory, input_res)
            
        
        
# __name__ (Program Entry Point)
if __name__=="__main__":
    main()