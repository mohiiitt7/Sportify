"""
Payment Integration Migration Script
Adds payment-related columns to sales_data table
"""

from sqlalchemy import create_engine, text

# Database connection
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mohit#2003@localhost/sportify18"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

def migrate_payment_columns():
    """Add payment columns to sales_data table"""
    
    with engine.connect() as conn:
        try:
            # Check if columns already exist
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='sales_data' AND column_name='payment_method'
            """)
            result = conn.execute(check_query)
            
            if result.fetchone():
                print("✓ Payment columns already exist. Skipping migration.")
                return
            
            # Add payment columns
            print("Adding payment columns to sales_data table...")
            
            alter_queries = [
                "ALTER TABLE sales_data ADD COLUMN payment_method VARCHAR(20) DEFAULT 'Cash'",
                "ALTER TABLE sales_data ADD COLUMN payment_status VARCHAR(20) DEFAULT 'Completed'",
                "ALTER TABLE sales_data ADD COLUMN transaction_id VARCHAR(100)",
                "ALTER TABLE sales_data ADD COLUMN upi_id VARCHAR(100)",
                "ALTER TABLE sales_data ADD COLUMN card_last4 VARCHAR(4)"
            ]
            
            for query in alter_queries:
                conn.execute(text(query))
                print(f"  ✓ Executed: {query}")
            
            conn.commit()
            print("\n✅ Migration completed successfully!")
            print("Payment integration columns added:")
            print("  - payment_method (Cash/UPI/Card)")
            print("  - payment_status (Pending/Completed/Failed)")
            print("  - transaction_id")
            print("  - upi_id")
            print("  - card_last4")
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    print("=" * 60)
    print("Payment Integration Migration")
    print("=" * 60)
    migrate_payment_columns()
    print("=" * 60)
