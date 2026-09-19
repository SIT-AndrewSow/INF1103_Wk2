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
    return amount * TAX_RATE


def generate_report(total_units, failed_entries):
    print(f"Total Deliveries Processed:{total_units} and the number of Failed/Rejected Entries:{failed_entries}.")
    return

    
def main():
    # local variables
    inventory = 0
    deliveries_count = 0
    failed_entries = 0
    
    while True:
        input_res = get_valid_input()
        
        if input_res == "quit":
            generate_report(deliveries_count, failed_entries)
            break
        elif input_res == "invalid":
            print("Invalid input. Please enter a valid positive number.")
            failed_entries += 1
            continue
        
        deliveries_count += 1
        inventory = process_delivery(inventory, input_res)
        tax = calculate_tax(input_res)
        print(f"The tax for this delivery is :{tax:.2f}")
        print(f"Current inventory: {inventory}")
              
        
if __name__=="__main__":
    main()