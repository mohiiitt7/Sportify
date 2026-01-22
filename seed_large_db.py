from app.database import SessionLocal, engine
from app import models
from decimal import Decimal
import random

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed_data():
    # Seed Employees (20)
    print("Seeding Employees...")
    for i in range(1, 21):
        email = f"emp_new_{i}@sportify.com"
        try:
            if not db.query(models.Employee).filter_by(email=email).first():
                emp = models.Employee(
                    eid=300 + i,
                    name=f"New Employee {i}",
                    email=email,
                    gender=random.choice(["Male", "Female"]),
                    dob="1990-01-01",
                    contact=f"9876543{i:03d}",
                    emp_type="Full Time",
                    education="Bachelor",
                    work_shift=random.choice(["Morning", "Evening"]),
                    address=f"Street {i}, City",
                    doj="2023-01-01",
                    salary="30000",
                    usertype="Employee",
                    password="password123"
                )
                db.add(emp)
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Skipping Employee {i}: {e}")
    
    # Seed Suppliers (10)
    print("Seeding Suppliers...")
    for i in range(1, 11):
        name = f"New Supplier {i}"
        try:
            if not db.query(models.Supplier).filter_by(name=name).first():
                sup = models.Supplier(
                    invoice=600 + i,
                    name=name,
                    contact=f"9998887{i:03d}",
                    discription=f"Description for supplier {i}"
                )
                db.add(sup)
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Skipping Supplier {i}: {e}")
            
    # Seed Categories
    print("Seeding Categories...")
    categories = ["Sports Wear", "Equipment", "Footwear", "Accessories", "New Arrivals"]
    for cat_name in categories:
        try:
            if not db.query(models.Category).filter_by(name=cat_name).first():
                cat = models.Category(
                    name=cat_name,
                    description=f"Description for {cat_name}"
                )
                db.add(cat)
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Skipping Category {cat_name}: {e}")

    # Seed Products (20)
    print("Seeding Products...")
    for i in range(1, 21):
        name = f"New Product {i}"
        supplier_name = f"New Supplier {random.randint(1, 10)}"
        try:
            if not db.query(models.Product).filter_by(name=name).first():
                price = Decimal(random.randint(50, 500))
                prod = models.Product(
                    id=1200 + i,
                    category=random.choice(categories),
                    supplier=supplier_name,
                    name=name,
                    price=price,
                    quantity=random.randint(10, 100),
                    status="Active"
                )
                db.add(prod)
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Skipping Product {i}: {e}")



    print("Seeding completed successfully!")

if __name__ == "__main__":
    try:
        seed_data()
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
