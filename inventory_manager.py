import json
import os #checks files, folders, read environment variables 

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
