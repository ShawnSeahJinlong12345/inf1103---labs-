LINE = "-" * 48

from product import Product

#class inventory
class Inventory:
    def __init__(self) -> None:
    #attributes
        self.__products: list[Product] = []

    #methods
    def add_product(self,product: Product) -> bool:
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def find_product(self,product_id: str) -> Product | None:
        for product in self.__products:
             if product.get_product_id().lower() == product_id.strip().lower():
                 return product
        return None

    def update_stock(self,product_id: str, new_stock: int) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        product.update_stock(new_stock)
        return True

    def display_all(self) -> None:
        print("Current Inventory")
        print(LINE)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()

        print(LINE)
    
    def get_products(self) -> list[Product]:
        return self.__products.copy()

    def remove_product(self,product_id: str) -> Bool:
        product = self.find_product(product_id)
        if product is None:
            return False

        self.__products.remove(product)
        return True

