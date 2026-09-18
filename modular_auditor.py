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