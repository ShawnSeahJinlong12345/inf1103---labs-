from product import Product
from supplier import Supplier
import math

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
