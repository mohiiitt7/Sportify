"""
Database Initialization Script for Sportify
Reads and executes schema.sql to create all tables
"""

import psycopg2
import os
from pathlib import Path


def get_db_connection():
    """Create PostgreSQL connection"""
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="mohit#2003",
            database="postgres"  # Connect to default database first
        )
        return connection
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        return None


def create_database(connection):
    """Create sportify18 database if it doesn't exist"""
    try:
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'sportify18'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE sportify18")
            print("✅ Database 'sportify18' created successfully")
        else:
            print("ℹ️  Database 'sportify18' already exists")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False


def execute_schema(schema_path):
    """Execute schema.sql file"""
    try:
        # Connect to sportify18 database
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="mohit#2003",
            database="sportify18"
        )
        cursor = connection.cursor()
        
        # Read schema file
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Execute schema
        cursor.execute(schema_sql)
        connection.commit()
        
        print("✅ Schema executed successfully")
        print("\n📊 Tables created:")
        
        # List all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error executing schema: {e}")
        return False


def verify_schema():
    """Verify schema was created correctly"""
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="mohit#2003",
            database="sportify18"
        )
        cursor = connection.cursor()
        
        print("\n🔍 Verifying schema...")
        
        # Check table counts
        expected_tables = [
            'employee_data', 'supplier_data', 'category_data',
            'product_data', 'customer_data', 'cart_data', 'tax_data'
        ]
        
        for table in expected_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   ✓ {table}: {count} rows")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verifying schema: {e}")
        return False


def main():
    """Main initialization function"""
    print("=" * 50)
    print("Sportify Database Initialization")
    print("=" * 50)
    
    # Get script directory
    script_dir = Path(__file__).parent
    schema_path = script_dir / "schema.sql"
    
    if not schema_path.exists():
        print(f"❌ Schema file not found: {schema_path}")
        return False
    
    print(f"\n📄 Schema file: {schema_path}")
    
    # Step 1: Connect to PostgreSQL
    print("\n1️⃣  Connecting to PostgreSQL...")
    connection = get_db_connection()
    if not connection:
        return False
    print("✅ Connected to PostgreSQL")
    
    # Step 2: Create database
    print("\n2️⃣  Creating database...")
    if not create_database(connection):
        return False
    connection.close()
    
    # Step 3: Execute schema
    print("\n3️⃣  Executing schema...")
    if not execute_schema(schema_path):
        return False
    
    # Step 4: Verify schema
    print("\n4️⃣  Verifying schema...")
    if not verify_schema():
        return False
    
    print("\n" + "=" * 50)
    print("✅ Database initialization completed successfully!")
    print("=" * 50)
    print("\n📝 Next steps:")
    print("   1. Run the Sportify application")
    print("   2. Test CRUD operations")
    print("   3. Verify data persistence")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
