LINE = "-" * 48

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
