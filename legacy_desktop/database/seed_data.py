import psycopg2
import random

def seed_data():
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="mohit#2003",
            database="sportify18"
        )
        cursor = connection.cursor()

        # 1. Seed Categories
        categories = ["Basketball", "Running", "Tennis", "Football", "Equipment"]
        for cat in categories:
            cursor.execute("INSERT INTO category_data (id, name, description) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING",
                           (random.randint(100, 999), cat, f"Sporting goods for {cat}"))

        # 2. Seed Suppliers
        suppliers = ["Nike", "Adidas", "Wilson", "Puma", "Spalding"]
        for i, sup in enumerate(suppliers):
            cursor.execute("INSERT INTO supplier_data (invoice, name, contact, discription) VALUES (%s, %s, %s, %s) ON CONFLICT (invoice) DO NOTHING",
                           (1001 + i, sup, "9876543210", f"Official distributor for {sup}"))

        # 3. Seed Employees
        emp_types = ['Full time', 'Part time', 'Contract']
        genders = ['Male', 'Female']
        shifts = ['Morning', 'Evening', 'Night']
        for i in range(1, 11):
            cursor.execute("""
                INSERT INTO employee_data (eid, name, email, gender, dob, contact, emp_type, education, work_shift, address, doj, salary, userType, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (eid) DO NOTHING
            """, (
                100 + i,
                f"Employee {i}",
                f"emp{i}@sportify.com",
                random.choice(genders),
                "01/01/1990",
                "900000000" + str(i % 10),
                random.choice(emp_types),
                "B.A",
                random.choice(shifts),
                f"Address {i}",
                "01/01/2023",
                "25000",
                "Employee",
                "pass123"
            ))

        # 4. Seed Products
        products_info = [
            ("Official NBA Ball", "Basketball", "Spalding", 2500, "basketball.png"),
            ("Air Max Runner", "Running", "Nike", 5500, "running_shoes.png"),
            ("Pro Staff Racket", "Tennis", "Wilson", 12000, "tennis_racket.png"),
            ("Elite Football", "Football", "Adidas", 1800, "football.png"),
            ("Court Classic", "Tennis", "Puma", 3000, "running_shoes.png"),
            ("Street Pro Ball", "Basketball", "Wilson", 1500, "basketball.png"),
            ("Vapor Mesh Shoe", "Running", "Nike", 4000, "running_shoes.png"),
            ("Speed Racket", "Tennis", "Wilson", 8000, "tennis_racket.png"),
            ("Training Jersey", "Equipment", "Nike", 1200, "jersey.png"),
            ("Chrome Dumbbell", "Equipment", "Puma", 2000, "dumbbell.png")
        ]

        for name, cat, sup, price, photo in products_info:
            cursor.execute("""
                INSERT INTO product_data (category, supplier, name, price, quantity, status, photo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (name) DO NOTHING
            """, (cat, sup, name, price, random.randint(10, 50), "Active", photo))

        connection.commit()
        print("✅ Data seeded successfully!")
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"❌ Error seeding data: {e}")

if __name__ == "__main__":
    seed_data()
