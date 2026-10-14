import csv
import random
from dataclasses import dataclass, asdict
from pathlib import Path

SEED = 42
random.seed(SEED)  # same seed -> same "world" every run

OUT_DIR = Path("data/master")


@dataclass
class Supplier:
    supplier_id: str
    name: str
    lead_time_days: int
    reliability_score: float  # 0-1, chance a delivery arrives on time


@dataclass
class Product:
    product_id: str
    product_name: str
    category: str
    subcategory: str
    brand: str
    base_price: float      # MRP
    unit_cost: float
    base_demand: int       # avg units/day in a size_factor=1.0 store
    shelf_life_days: int
    supplier_id: str


@dataclass
class Store:
    store_id: str
    city: str
    state: str
    store_type: str
    size_factor: float


def build_suppliers():
    return [
        Supplier("SUP001", "Western Beverages Ltd", 3, 0.95),
        Supplier("SUP002", "Sahyadri Foods", 5, 0.88),
        Supplier("SUP003", "Metro Personal Care", 4, 0.92),
        Supplier("SUP004", "Konkan Distributors", 7, 0.80),
    ]


def build_products():
    # (name, category, subcategory, brand, mrp, cost_ratio, base_demand, shelf_life, supplier)
    catalog = [
        ("Cola 500ml",          "Beverages",     "Soft Drinks",   "FizzUp",    40,  0.70, 30, 180, "SUP001"),
        ("Lemon Soda 500ml",    "Beverages",     "Soft Drinks",   "FizzUp",    35,  0.68, 20, 180, "SUP001"),
        ("Mango Juice 1L",      "Beverages",     "Juices",        "FreshPulp", 110, 0.65, 15, 120, "SUP001"),
        ("Energy Drink 250ml",  "Beverages",     "Energy Drinks", "Voltz",     99,  0.60, 10, 240, "SUP001"),
        ("Salted Chips 50g",    "Snacks",        "Chips",         "Crunchy",   20,  0.65, 40, 90,  "SUP002"),
        ("Cream Biscuits",      "Snacks",        "Biscuits",      "Bakewell",  30,  0.72, 35, 150, "SUP002"),
        ("Spicy Namkeen 200g",  "Snacks",        "Namkeen",       "Desi Bite", 55,  0.66, 25, 120, "SUP004"),
        ("Herbal Shampoo 180ml","Personal Care", "Shampoo",       "Silkora",   175, 0.55, 12, 720, "SUP003"),
        ("Beauty Soap 100g",    "Personal Care", "Soap",          "Glowra",    45,  0.60, 28, 720, "SUP003"),
        ("Toothpaste 150g",     "Personal Care", "Toothpaste",    "Denta",     95,  0.58, 22, 720, "SUP003"),
    ]
    products = []
    for i, (name, cat, sub, brand, mrp, cost_ratio, demand, shelf, sup) in enumerate(catalog, start=1):
        products.append(Product(
            product_id=f"SKU{i:03d}",
            product_name=name, category=cat, subcategory=sub, brand=brand,
            base_price=float(mrp),
            unit_cost=round(mrp * cost_ratio, 2),
            base_demand=demand, shelf_life_days=shelf, supplier_id=sup,
        ))
    return products


def build_stores():
    # store type -> size factor range
    size_range = {"Hypermarket": (1.5, 2.0), "Supermarket": (0.9, 1.3), "Kirana": (0.4, 0.7)}
    layout = [
        ("Mumbai", "Hypermarket"), ("Mumbai", "Supermarket"), ("Mumbai", "Kirana"),
        ("Pune", "Hypermarket"),   ("Pune", "Supermarket"),
        ("Nashik", "Supermarket"), ("Nashik", "Kirana"),
        ("Nagpur", "Hypermarket"), ("Nagpur", "Kirana"),
        ("Kolhapur", "Supermarket"),
    ]
    stores = []
    for i, (city, stype) in enumerate(layout, start=1):
        lo, hi = size_range[stype]
        stores.append(Store(f"STORE{i:03d}", city, "Maharashtra", stype,
                            round(random.uniform(lo, hi), 2)))
    return stores


def write_csv(rows, filename):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / filename
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=asdict(rows[0]).keys())
        writer.writeheader()
        writer.writerows(asdict(r) for r in rows)
    print(f"Wrote {len(rows):>3} rows -> {path}")


if __name__ == "__main__":
    write_csv(build_suppliers(), "dim_supplier.csv")
    write_csv(build_products(), "dim_product.csv")
    write_csv(build_stores(), "dim_store.csv")