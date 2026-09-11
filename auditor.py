inventory = 0

if not quit:
    stockQuant = input("Enter a stock quantity")
    
while True:
    stockQuant = input("Enter a stock quantity: ")
    
    # check if the user wants to quit
    if stockQuant == "quit": 
        print("Final inventory:", inventory)
        break
    
    # check if input is a valid number
    if not stockQuant.isdigit():
        print("Invalid input. Please enter a valid number.")
    else:
        stockQuant = int(stockQuant)
        inventory += stockQuant
        print(f"Current inventory: {inventory}")