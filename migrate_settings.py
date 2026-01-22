from app.database import engine
from sqlalchemy import text

def run_migrations():
    with engine.begin() as connection:
        # Add Shop Settings to settings_data
        columns_to_add = {
            "shop_name": "VARCHAR(255) DEFAULT 'Sportify Store'",
            "shop_contact": "VARCHAR(20) DEFAULT '+91 9999999999'",
            "shop_email": "VARCHAR(100) DEFAULT 'contact@sportify.com'",
            "shop_address": "TEXT DEFAULT '123 Sportify Street, India'",
            "shop_logo": "VARCHAR(255) DEFAULT ''"
        }
        
        for col, type_def in columns_to_add.items():
            try:
                connection.execute(text(f"ALTER TABLE settings_data ADD COLUMN {col} {type_def};"))
                print(f"Added '{col}' to 'settings_data'.")
            except Exception as e:
                print(f"Skipping '{col}': {e}")

if __name__ == "__main__":
    run_migrations()
