"""
Database Models for Sportify Inventory Management System
Python dataclasses for type-safe data handling
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from decimal import Decimal


@dataclass
class Employee:
    """Employee data model"""
    eid: int
    name: str
    email: str
    password: str
    gender: Optional[str] = None
    dob: Optional[str] = None
    contact: Optional[str] = None
    emp_type: Optional[str] = None
    education: Optional[str] = None
    work_shift: Optional[str] = None
    address: Optional[str] = None
    doj: Optional[str] = None
    salary: Optional[str] = None
    userType: str = "Employee"
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate employee data"""
        if self.contact and len(self.contact) != 10:
            raise ValueError("Contact must be 10 digits")
        if self.userType not in ['Admin', 'Employee']:
            raise ValueError("userType must be 'Admin' or 'Employee'")
        if self.gender and self.gender not in ['Male', 'Female']:
            raise ValueError("gender must be 'Male' or 'Female'")


@dataclass
class Supplier:
    """Supplier data model"""
    invoice: int
    name: str
    contact: str
    discription: Optional[str] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate supplier data"""
        if len(self.contact) != 10:
            raise ValueError("Contact must be 10 digits")


@dataclass
class Category:
    """Product category data model"""
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Product:
    """Product data model"""
    name: str
    category: str
    supplier: str
    price: Decimal
    quantity: int
    status: str
    id: Optional[int] = None
    discount: int = 0
    discounted_price: Optional[Decimal] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate and calculate product data"""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.discount < 0 or self.discount > 100:
            raise ValueError("Discount must be between 0 and 100")
        if self.status not in ['Active', 'Inactive']:
            raise ValueError("Status must be 'Active' or 'Inactive'")
        
        # Calculate discounted price if not provided
        if self.discounted_price is None:
            self.discounted_price = self.price * (1 - Decimal(self.discount) / 100)

    @property
    def total_value(self) -> Decimal:
        """Calculate total inventory value"""
        return self.discounted_price * self.quantity


@dataclass
class Customer:
    """Customer data model"""
    name: str
    contact: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate customer data"""
        if len(self.contact) != 10:
            raise ValueError("Contact must be 10 digits")


@dataclass
class CartItem:
    """Shopping cart item data model"""
    name: str
    price: Decimal
    quantity: int
    cid: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate cart item"""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

    @property
    def subtotal(self) -> Decimal:
        """Calculate item subtotal"""
        return self.price * self.quantity


@dataclass
class Tax:
    """Tax configuration data model"""
    tax: Decimal
    id: int = 1
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate tax data"""
        if self.tax < 0 or self.tax > 100:
            raise ValueError("Tax must be between 0 and 100")
        if self.id != 1:
            raise ValueError("Tax configuration must have id=1")


# Helper functions for database operations

def employee_to_tuple(emp: Employee) -> tuple:
    """Convert Employee to tuple for database insertion"""
    return (
        emp.eid, emp.name, emp.email, emp.gender, emp.dob,
        emp.contact, emp.emp_type, emp.education, emp.work_shift,
        emp.address, emp.doj, emp.salary, emp.userType, emp.password
    )


def supplier_to_tuple(sup: Supplier) -> tuple:
    """Convert Supplier to tuple for database insertion"""
    return (sup.invoice, sup.name, sup.contact, sup.discription)


def category_to_tuple(cat: Category) -> tuple:
    """Convert Category to tuple for database insertion"""
    return (cat.id, cat.name, cat.description)


def product_to_tuple(prod: Product) -> tuple:
    """Convert Product to tuple for database insertion"""
    return (
        prod.category, prod.supplier, prod.name, prod.price,
        prod.discount, prod.quantity, prod.status
    )


def customer_to_tuple(cust: Customer) -> tuple:
    """Convert Customer to tuple for database insertion"""
    return (cust.name, cust.contact)


def cart_item_to_tuple(item: CartItem) -> tuple:
    """Convert CartItem to tuple for database insertion"""
    return (item.name, item.price, item.quantity)
