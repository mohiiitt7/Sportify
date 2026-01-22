from app.database import SessionLocal
from app import models
import json

db = SessionLocal()

# 1. Create Dummy Products if not exist
products_to_add = [
    {"name": "Cricket Bat", "category": "Cricket", "supplier": "Sports Co", "price": 1200, "cost_price": 800, "quantity": 10},
    {"name": "Cricket Ball", "category": "Cricket", "supplier": "Sports Co", "price": 300, "cost_price": 150, "quantity": 50},
    {"name": "Football", "category": "Football", "supplier": "Sports Co", "price": 800, "cost_price": 500, "quantity": 20},
    {"name": "Tennis Racket", "category": "Tennis", "supplier": "Sports Co", "price": 2500, "cost_price": 2000, "quantity": 5},
    {"name": "Running Shoes", "category": "Athletics", "supplier": "Sports Co", "price": 3000, "cost_price": 1500, "quantity": 10},
    {"name": "Badminton Racket", "category": "Badminton", "supplier": "Sports Co", "price": 1500, "cost_price": 1000, "quantity": 15},
    {"name": "Badminton Shuttle", "category": "Badminton", "supplier": "Sports Co", "price": 500, "cost_price": 300, "quantity": 100},
]

created_products = []
for p in products_to_add:
    existing = db.query(models.Product).filter(models.Product.name == p['name']).first()
    if not existing:
        new_p = models.Product(**p)
        db.add(new_p)
        db.commit()
        db.refresh(new_p)
        created_products.append(new_p)
        print(f"Created Product: {new_p.name}")
    else:
        created_products.append(existing)

# 2. Operations to simulate sales
# Sale 1: Cricket emphasis
items_summary_list = []
total_1 = 0
items_1 = [(created_products[0], 2), (created_products[1], 5)] # 2 Bats, 5 Balls
for p, qty in items_1:
    total_1 += float(p.price) * qty
    items_summary_list.append(f"{p.name} x{qty} (₹{p.price})")

sale1 = models.Sale(
    customer_name="Dhoni Fan",
    customer_contact="9876543210",
    total_amount=total_1,
    net_amount=total_1,
    items_summary=", ".join(items_summary_list)
)
db.add(sale1)

# Sale 2: Football and Badminton
items_summary_list_2 = []
total_2 = 0
items_2 = [(created_products[2], 3), (created_products[5], 2)] # 3 Footballs, 2 Rackets
for p, qty in items_2:
    total_2 += float(p.price) * qty
    items_summary_list_2.append(f"{p.name} x{qty} (₹{p.price})")

sale2 = models.Sale(
    customer_name="Ronaldo Fan",
    customer_contact="9988776655",
    total_amount=total_2,
    net_amount=total_2,
    items_summary=", ".join(items_summary_list_2)
)
db.add(sale2)

db.commit()
print("Created Sales Data successfully.")
