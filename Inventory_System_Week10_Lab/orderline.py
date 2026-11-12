from product import Product

class OrderLine:
    def __init__(self,product: "Product",quantity: int) -> None:
        self.product: "Product" = product
        self.quantity: int = quantity

    def calculate_subtotal(self)-> float:
        return self.product.get_price() * self.quantity