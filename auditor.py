inventory = 0
failedEntries = 0

if not quit:
    stockQuant = input("Enter a stock quantity")
    
while True:
    stockQuant = input("Enter a stock quantity: ")
    
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