import math
from abc import ABC, abstractmethod

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

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class PhysicalProduct(Product):
    def __init__ (self,product_id,name,price,stock_quantity,weight):
        super().__init__(product_id,name,price,stock_quantity)
        #validate weight
        if (
            isinstance(weight,bool)
            or not isinstance(weight,(int,float))
            or not math.isfinite(weight)
            or weight <= 0
            ):
            raise ValueError("Weight must be a finite number greater than 0.")
    
        self.__weight = float(weight)

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    

class DigitalProduct(Product):
    def __init__ (self,product_id,name,price,stock_quantity,download_size):
        super().__init__(product_id,name,price,stock_quantity)

        #validate downloadsize 
        if (
            isinstance(download_size, bool)
            or not isinstance(download_size, (int, float))
            or not math.isfinite(download_size)
            or download_size <= 0
        ):
            raise ValueError(
                "Download size must be a finite number greater than 0."
            )

        self._download_size = float(download_size)

    def get_download_size(self):
        return self._download_size

    def display_information(self):
        super().display_information()
        print(f"Download size: {self._download_size} megabytes")
        
    def get_fulfilment_info(self):
        return "This product is delivered digitally."