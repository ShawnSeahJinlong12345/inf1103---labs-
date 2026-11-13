from product import Product
from orderline import OrderLine
from DiscountStrategy import DiscountStrategy
from NoDiscount import NoDiscount

class Order:
    def __init__(self,order_id:str,discount:DiscountStrategy | None = None)-> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

        self.discount = discount if discount is not None else NoDiscount()

    def add_order_line(self,product: "Product",quantity: int) -> None:
        order_line = OrderLine(product,quantity)
        self.order_lines.append(order_line)

    def set_discount(self,discount:DiscountStrategy)->None:
        self.discount = discount 

    def calculate_total(self) -> float:
        total = 0.0

        for order_line in self.order_lines:
            total += order_line.calculate_subtotal()

        return self.discount.apply(total)