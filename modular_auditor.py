def get_valid_input():
    """Handles the prompt, validates input, returns a valid integer or 'quit' signal."""
    while True:
        stock_count = input("Enter stock quantity (type quit to stop): ")

        if stock_count.lower() == "quit":
            return "quit"

        elif not stock_count.isdigit():
            print("Invalid Command, Type again.")
            return None  # signals a failed attempt

        else:
            quantity = int(stock_count)

            if quantity < 0:
                print("Negative Number, Invalid, Try Again.")
                return None  # signals a failed attempt

            return quantity


def process_delivery(current_total, new_value):
    """Calculates the new total and returns it."""
    return current_total + new_value


def calculate_tax(amount):
    """Takes a delivery amount and returns the tax (10% of that delivery)."""
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    """Prints the final summary."""
    print("-- Report of Total Entries --")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


# ---- Main program loop ----
stock_total = 0
failed_entries = 0
total_tax = 0

while True:
    result = get_valid_input()

    if result == "quit":
        break

    if result is None:
        failed_entries += 1
        print(f"Failed Entries Count: {failed_entries}")
        continue

    quantity = result
    stock_total = process_delivery(stock_total, quantity)

    tax = calculate_tax(quantity)
    total_tax += tax

    print(f"Number of stocks running: {stock_total}")
    print(f"Tax on this delivery: {tax:.2f}")

    if quantity >= 500:
        print("Alert: Inventory exceeds 500 units!")
        break

generate_report(stock_total, failed_entries)
print(f"Total Tax Collected: {total_tax:.2f}")