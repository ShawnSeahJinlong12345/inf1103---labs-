from product import Product

class OrderLine:
    def __init__(self,product: "Product",quantity: int) -> None:
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantity must be a whole number greater than zero.")
        self.product: "Product" = product
        self.quantity: int = quantity

    def calculate_subtotal(self)-> float:
        return self.product.get_price() * self.quantity