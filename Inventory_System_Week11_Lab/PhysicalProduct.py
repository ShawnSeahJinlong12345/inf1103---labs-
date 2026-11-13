from product import Product
from CanBeShipped import CanBeShipped
from supplier import Supplier
import math

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