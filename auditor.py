stock_total = 0
failed_entries = 0

while True:
    stock = input("Enter a stock quantity (or 'quit' to stop): ")

    if stock.lower() == "quit":
            break