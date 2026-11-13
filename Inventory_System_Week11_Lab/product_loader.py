import csv

from ProductFactory import ProductFactory
from inventory import Inventory
from supplier import Supplier


def load_products(
    path: str,
    inventory: Inventory,
    supplier: Supplier
) -> None:
    loaded = 0

    try:
        file = open(path, newline="", encoding="utf-8-sig")

    except FileNotFoundError:
        print(f"Products file not found: {path}")

    else:
        with file:
            reader = csv.DictReader(file)

            for row_number, row in enumerate(reader, start=2):
                try:
                    product_type = row["product_type"].strip()

                    # The lab CSV omits these measurements.
                    # Use sample defaults only when the columns are absent.
                    weight = None
                    download_size = None

                    if product_type == "physical":
                        weight = float(row.get("weight", "1"))

                    elif product_type == "digital":
                        download_size = float(
                            row.get("download_size", "1")
                        )

                    product = ProductFactory.create(
                        product_type=product_type,
                        product_id=row["product_id"],
                        name=row["name"],
                        price=float(row["price"]),
                        stock_quantity=int(row["stock_quantity"]),
                        supplier=supplier,
                        weight=weight,
                        download_size=download_size
                    )

                    if not inventory.add_product(product):
                        raise ValueError(
                            f"Duplicate product ID: "
                            f"{product.get_product_id()}"
                        )

                    loaded += 1

                except ValueError as error:
                    print(f"Skipping row {row_number}: {error}")

                except (KeyError, TypeError, AttributeError) as error:
                    print(
                        f"Skipping row {row_number}: "
                        f"missing or invalid CSV data ({error})"
                    )

        print(f"{loaded} products loaded.")

    finally:
        print("Load attempt finished.")