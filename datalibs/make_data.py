"""Writes data/orders.csv: 200 made-up shop orders. The file is committed; run this only to regenerate it.

The random generator has a fixed seed, so the same file comes out every time.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

rng = random.Random(42)
start = date(2026, 1, 1)
out = Path(__file__).resolve().parent / "data" / "orders.csv"

with out.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["order_id", "customer_id", "order_date", "amount", "status"])
    for order_id in range(1, 201):
        status = rng.choices(["delivered", "shipped", "placed", "cancelled"], weights=[6, 2, 1, 1])[0]
        # About 1 order in 25 has not been priced yet: its amount is left empty (missing).
        amount = "" if rng.random() < 0.04 else f"{rng.randint(150, 12000) / 100:.2f}"
        writer.writerow([
            order_id,
            rng.randint(1, 12),
            (start + timedelta(days=rng.randint(0, 89))).isoformat(),
            amount,
            status,
        ])
