import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path

import csv
import numpy as np

MASTER_DIR = Path("data/master")
OUT_FILE = Path("data/raw/sales_events.jsonl")


def load_csv(name):
    with open(MASTER_DIR / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def generate_day(business_date, products, stores, rng, counter):
    events = []
    for store in stores:
        size = float(store["size_factor"])
        for p in products:
            expected = int(p["base_demand"]) * size
            units_left = int(rng.poisson(expected))
            while units_left > 0:
                qty = min(units_left, int(rng.integers(1, 4)))
                units_left -= qty

                counter[0] += 1
                seconds = int(rng.integers(8 * 3600, 22 * 3600))  # store hours 08:00-22:00
                event_time = datetime.combine(business_date, datetime.min.time()) + timedelta(seconds=seconds)
                price = float(p["base_price"])

                events.append({
                    "transaction_id": f"TX{counter[0]:07d}",
                    "event_time": event_time.isoformat(),
                    "business_date": business_date.isoformat(),
                    "store_id": store["store_id"],
                    "product_id": p["product_id"],
                    "quantity": qty,
                    "unit_price": price,
                    "total_amount": round(qty * price, 2),
                })
    return events


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=3, help="number of simulated days")
    parser.add_argument("--start-date", default="2026-01-01")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    products = load_csv("dim_product.csv")
    stores = load_csv("dim_store.csv")
    rng = np.random.default_rng(args.seed)
    counter = [0]
    start = date.fromisoformat(args.start_date)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for d in range(args.days):
            day_events = generate_day(start + timedelta(days=d), products, stores, rng, counter)
            for e in day_events:
                f.write(json.dumps(e) + "\n")
            total += len(day_events)
            print(f"{start + timedelta(days=d)}: {len(day_events)} events")

    print(f"Total: {total} events -> {OUT_FILE}")


if __name__ == "__main__":
    main()