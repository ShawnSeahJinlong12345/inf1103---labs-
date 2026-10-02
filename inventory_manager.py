import json
import os

# Path can be overridden (used by Docker so the file lives on a mounted volume)
FILENAME = os.environ.get("INVENTORY_FILE", "inventory.json")
LINE = "-" * 48


# ---------------- Data persistence ----------------
def load_inventory(filename=FILENAME):
    """Loads inventory from JSON if the file exists, otherwise returns an empty list."""
    if os.path.exists(filename):
        print("inventory.json found.")
        try:
            with open(filename, "r") as f:
                inventory = json.load(f)
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError):
            print("Could not read inventory.json. Starting with an empty inventory.")
            return []
    print("inventory.json not found. Starting with an empty inventory.")
    return []


def save_inventory(inventory, filename=FILENAME):
    """Saves the inventory list to a JSON file."""
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filename, "w") as f:
        json.dump(inventory, f, indent=4)


# ---------------- Data manipulation ----------------
def search_product(inventory, product_id):
    """Returns the product dictionary matching the ID, or None."""
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product
    return None


def add_product(inventory, product_id, name, price, stock):
    """Adds a new product dictionary to the inventory. Returns True if added."""
    if search_product(inventory, product_id):
        return False
    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
    })
    return True


def update_stock(inventory, product_id, new_stock):
    """Updates the stock of an existing product. Returns True if updated."""
    product = search_product(inventory, product_id)
    if product is None:
        return False
    product["stock"] = new_stock
    return True


def display_all(inventory):
    """Prints every product in the inventory."""
    print("Current Inventory")
    print(LINE)
    if not inventory:
        print("No products in inventory.")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print(LINE)


# ---------------- Input helpers ----------------
def read_float(prompt):
    """Keeps asking until a non-negative number is entered."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative. Try again.")
                continue
            return value
        except ValueError:
            print("Invalid number. Try again.")


def read_int(prompt):
    """Keeps asking until a non-negative whole number is entered."""
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Invalid quantity. Enter a whole number (0 or more).")


# ---------------- Menu handlers ----------------
def handle_add(inventory):
    print("Add New Product")
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if search_product(inventory, product_id):
        print("Product ID already exists. Product not added.")
        return
    name = input("Product Name: ").strip()
    price = read_float("Price: ")
    stock = read_int("Stock Quantity: ")
    add_product(inventory, product_id, name, price, stock)
    print("Product added successfully!")


def handle_update(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    new_stock = read_int("New Stock Quantity: ")
    update_stock(inventory, product_id, new_stock)
    print("Stock updated successfully!")


def handle_search(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    print(LINE)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print(LINE)


def print_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


# ---------------- Main program ----------------
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()
    print_menu()

    while True:
        option = input("Enter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            handle_add(inventory)
        elif option == "3":
            handle_update(inventory)
        elif option == "4":
            handle_search(inventory)
        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()