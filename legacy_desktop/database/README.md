# Sportify Database Schema

This directory contains the centralized database schema and models for the Sportify Inventory Management System.

## Files

### 📄 `schema.sql`
Complete PostgreSQL schema definition with:
- All 7 tables (employee, supplier, category, product, customer, cart, tax)
- Primary keys and constraints
- Foreign key relationships (commented out, can be enabled)
- Check constraints for data validation
- Indexes for performance
- Triggers for automatic timestamp updates
- Initial seed data (admin user, default tax)

### 🐍 `models.py`
Python dataclass models for type-safe data handling:
- `Employee` - Employee information
- `Supplier` - Supplier/vendor data
- `Category` - Product categories
- `Product` - Product inventory
- `Customer` - Customer records
- `CartItem` - Shopping cart items
- `Tax` - Tax configuration

Each model includes validation and helper methods.

### 🚀 `init_db.py`
Database initialization script:
- Creates `sportify18` database
- Executes `schema.sql`
- Verifies table creation
- Shows table statistics

## Database Structure

```
sportify18 (PostgreSQL Database)
├── employee_data      (Employee records & login)
├── supplier_data      (Supplier information)
├── category_data      (Product categories)
├── product_data       (Product inventory) → references category, supplier
├── customer_data      (Customer records)
├── cart_data          (Temporary shopping cart) → references product
└── tax_data           (Tax configuration - single row)
```

## Usage

### Initialize Database

Run the initialization script to create all tables:

```bash
python database/init_db.py
```

This will:
1. Connect to PostgreSQL
2. Create `sportify18` database
3. Execute schema.sql
4. Verify all tables created
5. Show table statistics

### Reset Database

To recreate the database from scratch:

1. Uncomment the DROP TABLE statements in `schema.sql`
2. Run `init_db.py`

**⚠️ WARNING**: This will delete all existing data!

### Enable Foreign Keys

Foreign key constraints are commented out in `schema.sql` by default. To enable them:

1. Uncomment the ALTER TABLE statements in `schema.sql`
2. Re-run `init_db.py`

**Note**: Existing data must satisfy constraints before enabling them.

## Schema Features

### ✅ Data Validation
- Email uniqueness for employees
- Contact number length checks (10 digits)
- Price and quantity non-negative constraints
- Discount range validation (0-100%)
- Status enumeration checks

### 🔗 Relationships
- Products reference categories and suppliers (optional FK)
- Cart items reference products (optional FK)
- Cascade delete rules can be configured

### ⚡ Performance
- Indexes on frequently queried columns
- Automatic timestamp updates via triggers
- Computed column for discounted prices

### 🔒 Data Integrity
- Primary keys on all tables
- Unique constraints on emails and product names
- Check constraints for valid data ranges
- Single-row constraint for tax configuration

## Default Data

The schema includes initial seed data:

**Admin User:**
- Email: `mohit07@gmail.com`
- Password: `mohit123`
- Role: Admin

**Tax Configuration:**
- Default tax rate: 10%

## Viewing Schema

### Using psql:
```bash
# Connect to database
psql -U postgres -d sportify18

# List all tables
\dt

# Describe a table
\d employee_data

# View constraints
\d+ product_data
```

### Using pgAdmin:
1. Connect to PostgreSQL server
2. Navigate to: Databases → sportify18 → Schemas → public → Tables
3. Right-click any table → Properties to view structure

## Migration from Old Schema

The application code currently creates tables inline. To migrate:

1. Run `init_db.py` to create centralized schema
2. Update application code to remove CREATE TABLE statements
3. Test all CRUD operations
4. Optionally enable foreign key constraints

## Maintenance

### Backup Database:
```bash
pg_dump -U postgres sportify18 > backup.sql
```

### Restore Database:
```bash
psql -U postgres sportify18 < backup.sql
```

### View Table Statistics:
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Future Enhancements

- [ ] Add foreign key constraints
- [ ] Implement database migrations
- [ ] Add audit logging tables
- [ ] Create views for common queries
- [ ] Add stored procedures for complex operations
- [ ] Implement row-level security
