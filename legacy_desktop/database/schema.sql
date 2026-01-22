-- ============================================
-- Sportify Inventory Management System
-- PostgreSQL Database Schema
-- ============================================

-- Drop existing tables if recreating (use with caution)
-- DROP TABLE IF EXISTS cart_data CASCADE;
-- DROP TABLE IF EXISTS product_data CASCADE;
-- DROP TABLE IF EXISTS customer_data CASCADE;
-- DROP TABLE IF EXISTS category_data CASCADE;
-- DROP TABLE IF EXISTS supplier_data CASCADE;
-- DROP TABLE IF EXISTS employee_data CASCADE;
-- DROP TABLE IF EXISTS tax_data CASCADE;

-- ============================================
-- 1. EMPLOYEE TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS employee_data (
    eid INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    gender VARCHAR(20) CHECK (gender IN ('Male', 'Female')),
    dob VARCHAR(50),
    contact VARCHAR(15) CHECK (LENGTH(contact) = 10),
    emp_type VARCHAR(50) CHECK (emp_type IN ('Full time', 'Part time', 'Casual', 'Contract', 'Intern')),
    education VARCHAR(100),
    work_shift VARCHAR(20) CHECK (work_shift IN ('Morning', 'Evening', 'Night')),
    address TEXT,
    doj VARCHAR(50),
    salary VARCHAR(50),
    userType VARCHAR(20) CHECK (userType IN ('Admin', 'Employee')),
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE employee_data IS 'Stores employee information and login credentials';
COMMENT ON COLUMN employee_data.eid IS 'Employee ID (Primary Key)';
COMMENT ON COLUMN employee_data.userType IS 'User role: Admin or Employee';

-- ============================================
-- 2. SUPPLIER TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS supplier_data (
    invoice INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(15) NOT NULL CHECK (LENGTH(contact) = 10),
    discription VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE supplier_data IS 'Stores supplier/vendor information';
COMMENT ON COLUMN supplier_data.invoice IS 'Supplier invoice number (Primary Key)';

-- ============================================
-- 3. CATEGORY TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS category_data (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE category_data IS 'Product categories for inventory organization';

-- ============================================
-- 4. PRODUCT TABLE (with Foreign Keys)
-- ============================================
CREATE TABLE IF NOT EXISTS product_data (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    supplier VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    discount INT DEFAULT 0 CHECK (discount >= 0 AND discount <= 100),
    discounted_price DECIMAL(10,2) GENERATED ALWAYS AS (price * (1 - discount::DECIMAL / 100)) STORED,
    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    status VARCHAR(20) CHECK (status IN ('Active', 'Inactive')),
    photo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add foreign key constraints (optional - can be enabled later)
-- ALTER TABLE product_data ADD CONSTRAINT fk_category 
--     FOREIGN KEY (category) REFERENCES category_data(name) ON DELETE RESTRICT ON UPDATE CASCADE;
-- ALTER TABLE product_data ADD CONSTRAINT fk_supplier 
--     FOREIGN KEY (supplier) REFERENCES supplier_data(name) ON DELETE RESTRICT ON UPDATE CASCADE;

COMMENT ON TABLE product_data IS 'Product inventory with pricing and stock information';
COMMENT ON COLUMN product_data.discounted_price IS 'Automatically calculated from price and discount';

-- ============================================
-- 5. CUSTOMER TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS customer_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(15) NOT NULL CHECK (LENGTH(contact) = 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE customer_data IS 'Customer information for billing and records';

-- ============================================
-- 6. CART TABLE (Temporary Shopping Cart)
-- ============================================
CREATE TABLE IF NOT EXISTS cart_data (
    cid SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    quantity INT NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add foreign key constraint (optional)
-- ALTER TABLE cart_data ADD CONSTRAINT fk_product 
--     FOREIGN KEY (name) REFERENCES product_data(name) ON DELETE CASCADE ON UPDATE CASCADE;

COMMENT ON TABLE cart_data IS 'Temporary cart for employee billing system';

-- ============================================
-- 7. TAX CONFIGURATION TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS tax_data (
    id INT PRIMARY KEY DEFAULT 1,
    tax DECIMAL(5,2) NOT NULL CHECK (tax >= 0 AND tax <= 100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ensure only one tax configuration row
-- Ensure only one tax configuration row (id = 1)
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'single_tax_row') THEN
        ALTER TABLE tax_data ADD CONSTRAINT single_tax_row CHECK (id = 1);
    END IF;
END $$;

COMMENT ON TABLE tax_data IS 'Global tax configuration (single row)';

-- ============================================
-- INDEXES for Performance
-- ============================================
CREATE INDEX IF NOT EXISTS idx_employee_email ON employee_data(email);
CREATE INDEX IF NOT EXISTS idx_product_name ON product_data(name);
CREATE INDEX IF NOT EXISTS idx_product_category ON product_data(category);
CREATE INDEX IF NOT EXISTS idx_product_supplier ON product_data(supplier);
CREATE INDEX IF NOT EXISTS idx_product_status ON product_data(status);
CREATE INDEX IF NOT EXISTS idx_customer_contact ON customer_data(contact);

-- ============================================
-- TRIGGERS for Updated Timestamp
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_product_updated_at ON product_data;
CREATE TRIGGER update_product_updated_at
    BEFORE UPDATE ON product_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- INITIAL DATA (Optional)
-- ============================================
-- Insert default admin user (password: 123)
INSERT INTO employee_data (eid, name, email, gender, dob, contact, emp_type, education, work_shift, address, doj, salary, userType, password)
VALUES (1, 'Admin User', 'lily@gmail.com', 'Female', '01/01/1990', '1234567890', 'Full time', 'B.Tech', 'Morning', 'Admin Address', '01/01/2020', '50000', 'Admin', '123')
ON CONFLICT (eid) DO NOTHING;

-- Insert default tax rate (10%)
INSERT INTO tax_data (id, tax) VALUES (1, 10.00)
ON CONFLICT (id) DO UPDATE SET tax = EXCLUDED.tax;

-- ============================================
-- SCHEMA VERSION
-- ============================================
COMMENT ON SCHEMA public IS 'Sportify v1.0 - PostgreSQL Schema';
