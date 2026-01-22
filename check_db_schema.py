from app.database import engine
from sqlalchemy import inspect

def check_columns():
    inspector = inspect(engine)
    for table_name in ["product_data", "sales_data"]:
        columns = [c["name"] for c in inspector.get_columns(table_name)]
        print(f"Table: {table_name}, Columns: {columns}")

if __name__ == "__main__":
    check_columns()
