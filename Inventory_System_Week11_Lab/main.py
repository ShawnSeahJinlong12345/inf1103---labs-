import json
import os
import math

from product import Supplier,PhysicalProduct,DigitalProduct
from inventory import Inventory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.environ.get(
    "INVENTORY_FILE",
    os.path.join(BASE_DIR, "inventory.json")
)

LINE = "-" * 48

def read_supplier() -> Supplier:
    while True:
        supplier_id = input("Supplier ID: ").strip()
        name = input("Supplier name: ").strip()
        contact_email = input("Supplier email: ").strip()

        if supplier_id and name and contact_email:
            return Supplier(supplier_id, name, contact_email)

        print("All supplier fields must be filled in. Please try again.")

#file handling
def load_inventory(filename: str = FILENAME)->Inventory:
    inventory = Inventory()
    try:
        with open(filename,"r",encoding = "utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty inventory")
        return inventory

    if not isinstance(data,list):
        raise ValueError("The inventory file must contain a list of products.")

    for item in data:
        if not isinstance(item,dict):
            raise ValueError("Each saved product must be a JSON object")
        try:
            product_type = item["type"]
            if product_type not in ("physical", "digital"):
                raise ValueError(
                    f"Unknown saved product type: {product_type!r}"
                )
            if "supplier" not in item:
                print(
                    f"Supplier details are missing for "
                    f"{item['id']} ({item['name']})."
                )
                supplier = read_supplier()
            else:
                supplier_data = item["supplier"]
                if not isinstance(supplier_data, dict):
                    raise ValueError("Saved supplier details must be an object.")

                for field in ("supplier_id", "name", "contact_email"):
                    value = supplier_data[field]
                    if not isinstance(value, str) or not value.strip():
                        raise ValueError(
                            f"Supplier {field} must be a non-empty string."
                        )

                supplier = Supplier(
                    supplier_data["supplier_id"].strip(),
                    supplier_data["name"].strip(),
                    supplier_data["contact_email"].strip(),
                )

            if product_type == "physical":
                product = PhysicalProduct(
                    item["id"], item["name"], item["price"],
                    item["stock"], item["weight"], supplier,
                )
            else:
                product = DigitalProduct(
                    item["id"], item["name"], item["price"],
                    item["stock"], item["download_size"], supplier,
                )

        except KeyError as error:
            raise ValueError(
                f"A saved product or supplier is missing {error}."
            ) from error

        if not inventory.add_product(product):
            raise ValueError(
                f"Duplicate product ID: {product.get_product_id()}"
            )

    print("Inventory loaded successfully.")
    return inventory
      

def save_inventory(inventory:Inventory, filename: str=FILENAME)-> None:
    data = []
    for product in inventory.get_products():
        supplier = product.supplier
        item = {
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
            "supplier":{
                "supplier_id": supplier._supplier_id,
                "name": supplier._name,
                "contact_email": supplier._contact_email,
            }
        }

        if isinstance(product, PhysicalProduct):
            item["type"] = "physical"
            item["weight"] = product.get_weight()

        elif isinstance(product, DigitalProduct):
            item["type"] = "digital"
            item["download_size"] = product.get_download_size()

        else:
            raise ValueError(
                f"Unsupported product type: {type(product).__name__}"
            )
        data.append(item)

    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def read_float(prompt:str)->float:
    while True:
        try:
            value = float(input(prompt))
            if not math.isfinite(value) or value < 0:
                print("Enter a finite number of 0 or more.")
                continue
            return value
        except ValueError:
            print("Invalid number. Try again.")


def read_int(prompt:str)->int:
    while True:
        try:
            value = int(input(prompt).strip())
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Invalid quantity. Enter a whole number (0 or more).")

def read_positive_float(prompt:str)->float:
    while True:
        value = read_float(prompt)
        if value > 0:
            return value
        print("Enter a number greater than 0.")

def handle_add(inventory:Inventory  )->None:
    print("Add New Product")
    while True:
        product_type = input("Choose product type (1 = Physical, 2 = Digital): ").strip()
        if product_type in ("1","2"):
            break
        print("Please enter 1 or 2.")
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.find_product(product_id) is not None:
        print("Product ID already exists. Product not added.")
        return

    name = input("Product name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    price = read_float("Price: ")
    stock = read_int("Stock Quantity: ")

    print("Enter the supplier details for this product.")
    supplier = read_supplier()

    if product_type == "1":
        weight = read_positive_float("Weight in kilograms: ")
        product = PhysicalProduct(product_id,name,price,stock,weight,supplier)
    else: 
        download_size = read_positive_float("Download size in MB: ")
        product = DigitalProduct(product_id, name, price, stock, download_size,supplier)

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("Product could not be added.")

def handle_update(inventory:Inventory)->None:
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    new_stock = read_int("New Stock Quantity: ")
    inventory.update_stock(product_id, new_stock)
    print("Stock updated successfully!")

def handle_search(inventory:Inventory)->None:
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    print(LINE)
    product.display_information()
    print(product.get_fulfilment_info())
    product.supplier.display_information()
    print(LINE)

#menu control loop
def print_menu()->None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main()->None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    print("Loading inventory from:", os.path.abspath(FILENAME))
    
    try:
        inventory = load_inventory()
    except (OSError, ValueError) as error:
        # Do not overwrite an unreadable/invalid file with an empty inventory.
        print(f"Could not load inventory: {error}")
        print("Check the inventory file before running the program again.")
        return

    while True:
        print_menu()
        option = input("Enter option: ").strip()
        if option == "1":
            inventory.display_all()
        elif option == "2":
            handle_add(inventory)
        elif option == "3":
            handle_update(inventory)
        elif option == "4":
            handle_search(inventory)
        elif option in ("5", "6"):
            try:
                save_inventory(inventory)
            except (OSError,ValueError) as error:
                print(f"Could not save inventory: {error}")
                continue
            print(f"Inventory saved successfully to {FILENAME}.")
            if option == "6":
                print("Thank you for using Inventory Management System.")
                break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")
            
if __name__ == "__main__":
    main()