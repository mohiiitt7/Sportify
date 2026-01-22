from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Employee(Base):
    __tablename__ = "employee_data"

    eid = Column(Integer, primary_key=True, index=True) # Manual ID as per legacy
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    gender = Column(String(20))
    dob = Column(String(50))
    contact = Column(String(15))
    emp_type = Column(String(50))
    education = Column(String(100))
    work_shift = Column(String(20))
    address = Column(Text)
    doj = Column(String(50))
    salary = Column(String(50))
    usertype = Column(String(20)) # Admin or Employee
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Supplier(Base):
    __tablename__ = "supplier_data"

    invoice = Column(Integer, primary_key=True, index=True) # Manual Invoice ID
    name = Column(String(100), nullable=False)
    contact = Column(String(15), nullable=False)
    discription = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Category(Base):
    __tablename__ = "category_data"

    id = Column(Integer, primary_key=True, index=True) # Manual ID
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Product(Base):
    __tablename__ = "product_data"

    id = Column(Integer, primary_key=True, index=True) # Serial/Auto in legacy
    category = Column(String(100), nullable=False)
    supplier = Column(String(100), nullable=False)
    name = Column(String(100), unique=True, nullable=False, index=True)
    cost_price = Column(Numeric(10, 2), default=0.00) # Buying Price
    price = Column(Numeric(10, 2), nullable=False) # Selling Price
    discount = Column(Integer, default=0)
    discounted_price = Column(Numeric(10, 2)) # Calculated
    quantity = Column(Integer, default=0)
    status = Column(String(20)) # Active/Inactive
    photo = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class Customer(Base):
    __tablename__ = "customer_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact = Column(String(15), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Cart(Base):
    __tablename__ = "cart_data"

    cid = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Tax(Base):
    __tablename__ = "tax_data"

    id = Column(Integer, primary_key=True, default=1)
    tax = Column(Numeric(5, 2), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class Settings(Base):
    __tablename__ = "settings_data"

    id = Column(Integer, primary_key=True, default=1)
    gst_percent = Column(Numeric(5, 2), default=18.00)
    discount_percent = Column(Numeric(5, 2), default=0.00)
    shop_name = Column(String(255), default="Sportify Store")
    shop_contact = Column(String(20), default="+91 9999999999")
    shop_email = Column(String(100), default="contact@sportify.com")
    shop_address = Column(Text, default="123 Sportify Street, India")
    shop_logo = Column(String(255), default="")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class Sale(Base):
    __tablename__ = "sales_data"

    bill_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    customer_contact = Column(String(15), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False) # Before tax/discount
    gst_amount = Column(Numeric(10, 2), default=0.00)
    discount_amount = Column(Numeric(10, 2), default=0.00)
    net_amount = Column(Numeric(10, 2), nullable=False) # Final to pay
    profit = Column(Numeric(10, 2), default=0.00) # Net Amount - Total Cost
    items_summary = Column(Text, nullable=False) # JSON or text of items
    
    # Payment Integration Fields
    payment_method = Column(String(20), default="Cash") # Cash, UPI, Card, Split
    payment_status = Column(String(20), default="Completed") # Pending, Completed, Failed
    transaction_id = Column(String(100)) # For UPI/Card transactions
    upi_id = Column(String(100)) # UPI ID if payment via UPI
    card_last4 = Column(String(4)) # Last 4 digits of card (for reference)
    
    bill_date = Column(DateTime(timezone=True), server_default=func.now())
