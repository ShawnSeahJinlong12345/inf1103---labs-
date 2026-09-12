stock_total = 0
failed_entries = 0

while True:
    stock_count =input("Enter stock quanitity (type quit to stop): ")

    if stock_count.lower() == "quit":
        break

    elif not stock_count.isdigit():
        print("Invalid Command, Type again.")
        failed_entries += 1
        print(f"Failed Entries Count: {failed_entries}")
        continue 

    else:
        quantity = int(stock_count) #safe to convert to int

    if quantity < 0:    
            print("Negative Number, Invalid, Try Again.")
            failed_entries += 1
            print(f"Failed Entries Count: {failed_entries}")
            continue

    stock_total += quantity
    print(f"Number of stocks running: {stock_total} ")

