from product import (
    Product,
    Supplier,
    PhysicalProduct,
    DigitalProduct,
)
from inventory import Inventory


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


supplier = Supplier(
    "S001", "Tech Supplies", "sales@example.com"
)

physical = PhysicalProduct(
    "P001", "Keyboard", 50.0, 10,
    weight=0.8,
    supplier=supplier,
)

digital = DigitalProduct(
    "D001", "E-book", 12.0, 100,
    download_size=5.0,
    supplier=supplier,
)

inventory = Inventory()
inventory.add_product(physical)
inventory.add_product(digital)

inventory.display_all()

show_product_details(physical)
show_product_details(digital)