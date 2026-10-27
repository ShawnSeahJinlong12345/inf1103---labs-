import json
import os
import math

FILENAME = os.environ.get("INVENTORY_FILE","inventory.json")
LINE = "-" * 48

#class product
class Product:
    def __init__(self,product_id,name,price,stock_quantity):
        if not isinstance(product_id,str) or not product_id.strip():
            raise ValueError("Product ID cannot be empty.")
        if not isinstance(name,str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if (not isinstance(price,(int,float))
            or not math.isfinite(price)
            or price < 0):
            raise ValueError("Price must be a finite, non-negative number.")
    #attributes
        self.__product_id = product_id.strip()
        self.__name = name.strip()
        self.__price = float(price)
        self.update_stock(stock_quantity)
    #methods
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self,quantity):
        if type(quantity) is not int or quantity < 0:
            raise ValueError("Stock must be a whole number of 0 or more")
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name:{self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

#class inventory
class Inventory:
    def __init__(self):
    #attributes
        self.__products = []

    #methods
    def add_product(self,product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self,product_id):
        for product in self.__products:
             if product.get_product_id().lower() == product_id.strip().lower():
                 return product
        return None

    def update_stock(self,product_id, new_stock):
        product = self.search_product(product_id)
        if product is None:
            return False
        product.update_stock(new_stock)
        return True

    def display_all(self):
        print("Current Inventory")
        print(LINE)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print(LINE)
    
    def get_products(self):
        return self.__products.copy()

#file handling
def load_inventory(filename = FILENAME):
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
            product = Product(item["id"],item["name"],
                              item["price"],item["stock"])
        except KeyError as error:
            raise ValueError(f"A saved product is missing {error}.") from error
        if not inventory.add_product(product):
            raise ValueError(f"Duplicate product ID: {product.get_product_id()}")

    print("Inventory loaded successfully.")
    return inventory
    
def save_inventory(inventory, filename=FILENAME):
    data = [
        {"id": product.get_product_id(), "name": product.get_name(),
         "price": product.get_price(), "stock": product.get_stock()}
        for product in inventory.get_products()
    ]
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def read_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if not math.isfinite(value) or value < 0:
                print("Enter a finite number of 0 or more.")
                continue
            return value
        except ValueError:
            print("Invalid number. Try again.")


def read_int(prompt):
    while True:
        try:
            value = int(input(prompt).strip())
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Invalid quantity. Enter a whole number (0 or more).")

def handle_add(inventory):
    print("Add New Product")
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print("Product ID already exists. Product not added.")
        return
    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    price = read_float("Price: ")
    stock = read_int("Stock Quantity: ")
    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print("Product added successfully!")


def handle_update(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    new_stock = read_int("New Stock Quantity: ")
    inventory.update_stock(product_id, new_stock)
    print("Stock updated successfully!")

def handle_search(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    print(LINE)
    product.display_information()
    print(LINE)

#menu control loop
def print_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
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
            except OSError as error:
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