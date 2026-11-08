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

show_product_details(physical)
show_product_details(digital)

inventory = Inventory()

assert inventory.add_product(physical)
assert inventory.add_product(digital)

inventory.display_all()

assert inventory.find_product("P001") is physical
assert inventory.find_product("D001") is digital


assert inventory.update_stock("P001", 20)
assert inventory.update_stock("D001", 200)

assert physical.get_stock() == 20
assert digital.get_stock() == 200

print("Both product types passed the substitutability checks.")