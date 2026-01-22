from app.database import engine
from sqlalchemy import text

def run_migrations():
    with engine.begin() as connection:
        # 1. Add cost_price to product_data
        try:
            connection.execute(text("ALTER TABLE product_data ADD COLUMN cost_price NUMERIC(10, 2) DEFAULT 0.00;"))
            print("Added 'cost_price' to 'product_data'.")
        except Exception as e:
            print(f"Skipping 'cost_price': {e}")
            
        # 2. Add profit to sales_data
        try:
            connection.execute(text("ALTER TABLE sales_data ADD COLUMN profit NUMERIC(10, 2) DEFAULT 0.00;"))
            print("Added 'profit' to 'sales_data'.")
        except Exception as e:
            print(f"Skipping 'profit': {e}")

if __name__ == "__main__":
    run_migrations()
