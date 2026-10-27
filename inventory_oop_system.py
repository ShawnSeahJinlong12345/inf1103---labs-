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