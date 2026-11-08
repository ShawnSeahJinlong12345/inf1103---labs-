import math
from abc import ABC, abstractmethod


class OrderLine:
    def __init__(self,product: "Product",quantity: int) -> None:
        self.product: "Product" = product
        self.quantity: int = quantity

    def calculate_subtotal(self)-> float:
        return self.product.get_price() * self.quantity

class Order:
    def __init__(self,order_id:str)-> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self,product: "Product",quantity: int) -> None:
        order_line = OrderLine(product,quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = 0.0

        for order_line in self.order_lines:
            total += order_line.calculate_subtotal()

        return total

class Supplier:
    def __init__(self,supplier_id : str,name : str ,contact_email : str) -> None:
        self._supplier_id: str = supplier_id
        self._name: str= name
        self._contact_email: str = contact_email

    def display_information(self)->None:
        print(f"Supplier id: {self._supplier_id} | "
            f"Name: {self._name}"
            f"Contact email: {self._contact_email}")

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
        if (not isinstance(price,(int,float))
            or not math.isfinite(price)
            or price < 0):
            raise ValueError("Price must be a finite, non-negative number.")
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
    def get_fulfilment_info(self):
        pass

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class PhysicalProduct(Product,CanBeShipped):
    def __init__ (self,
                  product_id: str,
                  name: str,
                  price: float,
                  stock_quantity: int,
                  weight: float,
                  supplier: Supplier,):
        super().__init__(product_id,name,price,stock_quantity,supplier)
        #validate weight
        if (
            isinstance(weight,bool)
            or not isinstance(weight,(int,float))
            or not math.isfinite(weight)
            or weight <= 0
            ):
            raise ValueError("Weight must be a finite number greater than 0.")
    
        self.__weight = float(weight)

    def get_weight(self)->float:
        return self.__weight

    def display_information(self)->None:
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self)->str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self)->float:
        rate_per_kg = 5.0 
        return self.__weight * rate_per_kg

class DigitalProduct(Product):
    def __init__ (self,
                  product_id: str,
                  name: str,
                  price: float,
                  stock_quantity: int,
                  download_size: float,
                  supplier: Supplier):
        super().__init__(product_id,name,price,stock_quantity,supplier)

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

    def get_download_size(self)->float:
        return self._download_size

    def display_information(self)->None:
        super().display_information()
        print(f"Download size: {self._download_size} megabytes")

    def get_fulfilment_info(self)->str:
        return "This product is delivered digitally."


