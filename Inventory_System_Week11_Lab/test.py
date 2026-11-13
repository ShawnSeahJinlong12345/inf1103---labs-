"""Task 7 checks. Run from the project root with unittest discovery."""
import ast
import csv
import inspect
import io
from pathlib import Path
import tempfile
import textwrap
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from DiscountStrategy import DiscountStrategy
from NoDiscount import NoDiscount
from PercentageDiscount import PercentageDiscount
from BulkDiscount import BulkDiscount
from StudentDiscount import StudentDiscount
from ProductFactory import ProductFactory
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from inventory import Inventory
from order import Order
from orderline import OrderLine
from supplier import Supplier
import main
import product_loader

PROJECT = Path(main.__file__).resolve().parent
LAB_CSV = """product_id,name,price,stock_quantity,supplier_id,supplier_name,contact_email,product_type,weight,download_size
P001,Laptop,25.5,15,100,MandyCompany,MandyCompany@gmail.com,physical,1.8,
P002,Mouse,25.5,15,101,SalesCompany,SalesCompany@gmail.com,physical,0.1,
P003,Keyboard,45.0,25,102,BeeCompany,BeeCompany@gmail.com,physical,0.8,
P004,Ebook,29.9,10,103,BookCompany,BookCompany@gmail.com,digital,,288.0
P005,CyberPunk Edgerunners Game,69.9,14,104,GameCompany,GameCompany@gmail.com,digital,,10000.0
"""

INVALID_ROWS_CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


class Tests(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    def make_product(self, kind="physical", price=25, stock=10):
        return ProductFactory.create(
            kind, "P001", "Test Product", price, stock, self.supplier,
            weight=1.8, download_size=100,
        )

    def make_order(self, strategy=None):
        order = Order("O001", strategy)
        order.add_order_line(self.make_product(), 10)
        return order

    def load_csv(self, content):
        inventory = Inventory()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "products.csv"
            path.write_text(content, encoding="utf-8")
            with redirect_stdout(io.StringIO()) as output:
                product_loader.load_products(str(path), inventory, self.supplier)
        return inventory, output.getvalue()

    def test_default_no_discount(self):
        self.assertEqual(self.make_order().calculate_total(), 250)

    def test_each_existing_strategy(self):
        for strategy, expected in (
            (NoDiscount(), 250), (PercentageDiscount(10), 225),
            (BulkDiscount(200, 20), 230), (StudentDiscount(), 237.5),
        ):
            with self.subTest(strategy=type(strategy).__name__):
                self.assertAlmostEqual(self.make_order(strategy).calculate_total(), expected)

    def test_bulk_threshold_boundary(self):
        strategy = BulkDiscount(200, 20)
        self.assertEqual(strategy.apply(199), 199)
        self.assertEqual(strategy.apply(200), 180)

    def test_order_calls_strategy_with_original_total(self):
        class RecordingDiscount(DiscountStrategy):
            def apply(self, total):
                self.received = total
                return 123.45
        strategy = RecordingDiscount()
        self.assertEqual(self.make_order(strategy).calculate_total(), 123.45)
        self.assertEqual(strategy.received, 250)

    def test_new_strategy_without_changing_order(self):
        class FixedDiscount(DiscountStrategy):
            def apply(self, total):
                return total - 7
        self.assertEqual(self.make_order(FixedDiscount()).calculate_total(), 243)

    def test_switching_strategy_replaces_previous_discount(self):
        order = self.make_order(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225)

    def test_order_has_no_discount_selection_if(self):
        tree = ast.parse(textwrap.dedent(inspect.getsource(Order.calculate_total)))
        self.assertFalse(any(isinstance(node, (ast.If, ast.IfExp, ast.Match))
                             for node in ast.walk(tree)))

    def test_factory_creates_both_product_types(self):
        self.assertIsInstance(self.make_product(), PhysicalProduct)
        self.assertIsInstance(self.make_product("digital"), DigitalProduct)

    def test_unknown_type_has_clear_error(self):
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            self.make_product("service")

    def test_product_creation_is_centralised(self):
        # Review application modules, excluding tests and the factory itself.
        direct_calls = []
        for path in PROJECT.glob("*.py"):
            if path.stem == "ProductFactory" or path.name.startswith("test_"):
                continue
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if not isinstance(node, ast.Call):
                    continue
                name = (node.func.id if isinstance(node.func, ast.Name)
                        else node.func.attr if isinstance(node.func, ast.Attribute)
                        else "")
                if name in ("PhysicalProduct", "DigitalProduct"):
                    direct_calls.append(f"{path.name}:{node.lineno}")
        self.assertEqual(direct_calls, [], f"Direct product creation: {direct_calls}")

    def test_invalid_prices_rejected_by_both_types(self):
        for kind in ("physical", "digital"):
            for price in (0, -5, float("nan"), float("inf")):
                with self.subTest(kind=kind, price=price):
                    with self.assertRaises(ValueError):
                        self.make_product(kind, price=price)

    def test_invalid_stock_rejected_by_both_types(self):
        for kind in ("physical", "digital"):
            for stock in (-1, 1.5):
                with self.subTest(kind=kind, stock=stock):
                    with self.assertRaises(ValueError):
                        self.make_product(kind, stock=stock)

    def test_stock_updates_reject_negative_values(self):
        for kind in ("physical", "digital"):
            product = self.make_product(kind)
            with self.assertRaises(ValueError):
                product.update_stock(-1)
            self.assertEqual(product.get_stock(), 10)

    def test_zero_stock_is_allowed(self):
        self.assertEqual(self.make_product(stock=0).get_stock(), 0)

    def test_invalid_order_quantities_rejected(self):
        product = self.make_product()
        for quantity in (0, -1, 1.5):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError):
                    OrderLine(product, quantity)
        order = Order("O001")
        with self.assertRaises(ValueError):
            order.add_order_line(product, 0)
        self.assertEqual(order.order_lines, [])

    def test_bad_price_input_retries_with_exact_messages(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as ask:
            with redirect_stdout(io.StringIO()) as output:
                value = main.get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(ask.call_count, 3)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_price_input_retries(self):
        with patch("builtins.input", side_effect=["0", "20"]) as ask:
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main.get_positive_float("Price: "), 20)
        self.assertEqual(ask.call_count, 2)

    def test_missing_csv_is_handled_and_finally_runs(self):
        inventory = Inventory()
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "missing.csv")
            with redirect_stdout(io.StringIO()) as output:
                product_loader.load_products(path, inventory, self.supplier)
        self.assertIn("Products file not found:", output.getvalue())
        self.assertTrue(output.getvalue().endswith("Load attempt finished.\n"))
        self.assertEqual(inventory.get_products(), [])

    def test_lab_csv_loads_all_five_products(self):
        inventory, output = self.load_csv(LAB_CSV)
        self.assertEqual(
            [p.get_product_id() for p in inventory.get_products()],
            ["P001", "P002", "P003", "P004", "P005"],
        )
        self.assertEqual(output, "5 products loaded.\nLoad attempt finished.\n")
        self.assertEqual(inventory.find_product("P001").get_name(), "Laptop")
        self.assertEqual(inventory.find_product("P001").get_weight(), 1.8)
        self.assertEqual(inventory.find_product("P004").get_download_size(), 288.0)
        self.assertEqual(inventory.find_product("P005").get_name(),
                         "CyberPunk Edgerunners Game")

    def test_invalid_csv_skips_bad_rows_and_continues(self):
        inventory, output = self.load_csv(INVALID_ROWS_CSV)
        self.assertEqual([p.get_product_id() for p in inventory.get_products()],
                         ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", output)
        self.assertIn("abc", output)
        self.assertIn("3 products loaded.", output)
        self.assertTrue(output.endswith("Load attempt finished.\n"))

    def test_csv_loader_uses_factory(self):
        with patch.object(ProductFactory, "create", wraps=ProductFactory.create) as create:
            inventory, _ = self.load_csv(LAB_CSV)
        self.assertEqual(create.call_count, 5)
        self.assertEqual(len(inventory.get_products()), 5)

    def test_except_blocks_catch_specific_exceptions(self):
        broad = []
        for path in PROJECT.glob("*.py"):
            if path.name.startswith("test_"):
                continue
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.ExceptHandler):
                    names = [] if node.type is None else [
                        n.id for n in ast.walk(node.type) if isinstance(n, ast.Name)
                    ]
                    if node.type is None or {"Exception", "BaseException"}.intersection(names):
                        broad.append(f"{path.name}:{node.lineno}")
        self.assertEqual(broad, [], f"Overly broad except blocks: {broad}")

    def test_project_csv_works_with_loader(self):
        # This deliberately checks YOUR real CSV too, not only a test fixture.
        path = PROJECT / "products.csv"
        self.assertTrue(path.exists(), "Place products.csv in the project root.")
        with path.open(newline="", encoding="utf-8-sig") as file:
            rows = list(csv.DictReader(file))
        self.assertTrue(rows, "The supplied CSV should contain products.")
        inventory = Inventory()
        with redirect_stdout(io.StringIO()) as output:
            product_loader.load_products(str(path), inventory, self.supplier)
        self.assertGreater(len(inventory.get_products()), 0,
                           "No products loaded from your CSV: " + output.getvalue())


if __name__ == "__main__":
    unittest.main()
