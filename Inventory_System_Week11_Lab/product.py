import math
from abc import ABC, abstractmethod
from supplier import Supplier

#class product
class Product(ABC):
    def __init__(self,
                 product_id: str,
                 name: str,
                 price: float,
                 stock_quantity: int,
                 supplier: Supplier,) -> None:
        if not isinstance(product_id,str) or not product_id.strip():
            raise ValueError("Product ID cannot be empty.")
        if not isinstance(name,str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if (isinstance(price, bool)
            or not isinstance(price,(int,float))
            or not math.isfinite(price)
            or price <= 0):
            raise ValueError("Price must be a finite number greater than zero.")
    #attributes
        self.__product_id = product_id.strip()
        self.__name = name.strip()
        self.__price = float(price)
        self.supplier: Supplier = supplier
        self.update_stock(stock_quantity)
    #methods
    def get_product_id(self)->str:
        return self.__product_id

    def get_name(self)->str:
        return self.__name

    def get_price(self)->float:
        return self.__price

    def get_stock(self)->int:
        return self.__stock

    def update_stock(self,quantity)->None:
        if type(quantity) is not int or quantity < 0:
            raise ValueError("Stock must be a whole number of 0 or more")
        self.__stock = quantity

    def display_information(self)->None:
        print(f"ID: {self.__product_id} | Name:{self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        
    #child class must implement get_fulfilment_info method
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass








