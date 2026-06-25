"""
Generate synthetic Superstore-style sales data for the project.
Run this once to create sample_sales_data.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# Config
N_ROWS = 9994

categories = {
    "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
    "Technology": ["Phones", "Accessories", "Machines", "Copiers"],
    "Office Supplies": ["Labels", "Storage", "Art", "Binders", "Appliances", "Envelopes", "Fasteners", "Paper", "Supplies"]
}

products = {
    "Chairs": ["HON 5400 Series Task Chair", "Global Troy Executive Chair", "Realspace Magellan Chair"],
    "Tables": ["Bevis 36 x 72 Conference Table", "Chromcraft Bull-Nose Table", "Bretford CR4500"],
    "Bookcases": ["Bush Westfield Bookcase", "O'Sullivan 2-Shelf Bookcase", "Sauder Forest Hills"],
    "Furnishings": ["Eldon Jumbo Plastic Desk Accessories", "Tensor Brushed Steel Torchiere", "Howard Miller 11\" Wall Clock"],
    "Phones": ["Samsung Galaxy S6", "Motorola Smart Phone", "Apple iPhone 6S", "Nokia Smart Phone"],
    "Accessories": ["Belkin F8N112 Laptop Power Adapter", "Kensington Lock", "Logitech Wireless Mouse"],
    "Machines": ["Brother Intelli-Fax 4750E", "HP Designjet T520", "Xerox WorkCentre"],
    "Copiers": ["Canon PC1060 Copier", "Hewlett Packard LaserJet", "Konica Minolta"],
    "Labels": ["Avery 490 Labels", "3M Polarizing Label", "Avery Laser Labels"],
    "Storage": ["Eldon Fold N Roll Cart", "Fellowes Super Stor/Drawer", "Rogers File Cabinet"],
    "Art": ["SAFCO Arco Folding Chair", "Boston 16-Shelf Bookcase", "Hunt Boston Pencil Sharpener"],
    "Binders": ["Avery Durable Binders", "Avery Flexi-View Binders", "Wilson Jones Gold Binder"],
    "Appliances": ["Hoover Portapower Machine", "Sanyo 2.5 Cubic Foot Compact Refrigerator"],
    "Envelopes": ["Poly String & Button Envelopes", "Wintrust Envelope Selection"],
    "Fasteners": ["Advantus Push Pins", "OIC Binder Clips"],
    "Paper": ["Xerox 1967", "Hammermill Copy Plus Paper", "Easy-staple paper"],
    "Supplies": ["Acco Remark Laser Pointer", "Fiskars Adult Scissors"],
}

segments = ["Consumer", "Corporate", "Home Office"]
regions = ["West", "East", "Central", "South"]
states_by_region = {
    "West": ["California", "Washington", "Oregon", "Nevada", "Arizona", "Utah", "Colorado"],
    "East": ["New York", "Pennsylvania", "New Jersey", "Virginia", "Massachusetts", "Ohio", "Michigan"],
    "Central": ["Texas", "Illinois", "Minnesota", "Wisconsin", "Indiana", "Missouri", "Kansas"],
    "South": ["Florida", "Georgia", "North Carolina", "Tennessee", "Alabama", "Louisiana", "South Carolina"]
}
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
ship_mode_weights = [0.6, 0.2, 0.15, 0.05]

base_prices = {
    "Furniture": (80, 800),
    "Technology": (30, 1200),
    "Office Supplies": (5, 100),
}
discount_rates = [0.0, 0.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5]

rows = []
order_date_start = datetime(2021, 1, 1)
order_date_end = datetime(2024, 12, 31)

for i in range(N_ROWS):
    category = random.choice(list(categories.keys()))
    sub_category = random.choice(categories[category])
    product_list = products.get(sub_category, [f"{sub_category} Item"])
    product_name = random.choice(product_list)

    region = random.choice(regions)
    state = random.choice(states_by_region[region])

    order_date = order_date_start + timedelta(days=random.randint(0, (order_date_end - order_date_start).days))
    ship_delay = {"Standard Class": 5, "Second Class": 3, "First Class": 2, "Same Day": 0}
    ship_mode = random.choices(ship_modes, weights=ship_mode_weights)[0]
    ship_date = order_date + timedelta(days=ship_delay[ship_mode] + random.randint(0, 2))

    price_range = base_prices[category]
    unit_price = round(random.uniform(*price_range), 2)
    quantity = random.randint(1, 14)
    discount = random.choice(discount_rates)
    sales = round(unit_price * quantity * (1 - discount), 2)
    profit_margin = random.uniform(0.05, 0.40) if discount < 0.3 else random.uniform(-0.15, 0.15)
    profit = round(sales * profit_margin, 2)

    rows.append({
        "Row ID": i + 1,
        "Order ID": f"CA-{order_date.year}-{random.randint(100000, 999999)}",
        "Order Date": order_date.strftime("%Y-%m-%d"),
        "Ship Date": ship_date.strftime("%Y-%m-%d"),
        "Ship Mode": ship_mode,
        "Customer ID": f"CG-{random.randint(10000, 99999)}",
        "Customer Name": f"Customer {random.randint(1, 800)}",
        "Segment": random.choice(segments),
        "Region": region,
        "State": state,
        "Category": category,
        "Sub-Category": sub_category,
        "Product Name": product_name,
        "Sales": sales,
        "Quantity": quantity,
        "Discount": discount,
        "Profit": profit,
    })

df = pd.DataFrame(rows)
df.to_csv("data/sample_sales_data.csv", index=False)
print(f"✅ Generated {len(df)} rows → data/sample_sales_data.csv")
print(df.head())
