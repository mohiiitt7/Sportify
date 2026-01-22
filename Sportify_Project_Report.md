# 📑 Project Report: Sportify - Sports Store Management System

---

## 1. Project Synopsis
**Sportify** is an integrated Web-based Management System designed for sports retail stores. The primary objective of the project is to digitize the manual operations of a sports gear outlet, including inventory tracking, supplier coordination, employee management, and sales processing. By leveraging a modern tech stack (Python FastAPI + PostgreSQL), it ensures high performance, data security, and real-time analytics for store owners.

---

## 2. Project Description
The **Sportify** system serves as a centralized platform for both store administrators and employees. It transitions traditional store management into a data-driven environment.

### Core Objectives:
*   **Automation:** Reduce manual errors in billing and stock entry.
*   **Inventory Control:** Maintain optimal stock levels with low-stock alerts.
*   **Financial Tracking:** Real-time calculation of revenue, profit, taxes (GST), and discounts.
*   **Payment Versatility:** Support for modern digital payment methods (UPI/Card) alongside cash.
*   **Role-Based Security:** Ensure sensitive data (like employee salaries or supplier invoices) is only accessible to admins.

### Technical Stack:
*   **Backend:** FastAPI (Python) - High-performance asynchronous framework.
*   **Database:** PostgreSQL - Robust relational database for scalable data storage.
*   **Frontend:** Bootstrap 5, Vanilla CSS3, and HTML5 for a premium, responsive design.
*   **Logic/Templating:** Jinja2 templates and JavaScript for dynamic UI updates.
*   **Analytics:** Chart.js for graphical data representation.

---

## 3. Detailed Module Description

### 🛡️ Module 1: Authentication & Authorization
This module handles all user entry points and security.
*   **Features:** Secure login with password hashing (Bcrypt).
*   **Functionality:** It detects user roles (Admin vs. Employee). Admins are redirected to a full-management view, while Employees are restricted to Billing and Inventory viewing.
*   **Highlights:** Includes a modern "Show/Hide Password" toggle and session management via secure cookies.

### 📊 Module 2: Analytics Dashboard
The "Brain" of the system that provides a birds-eye view of the business.
*   **Statistics:** Displays total counts of products, employees, and suppliers.
*   **Visual Reports:** Uses **Chart.js** to show a 7-day Line Chart of sales trends and a Bar Chart for Top Selling Gear categories.
*   **Stock Monitoring:** Lists products that are below a threshold (e.g., 5 units) to prevent "Out of Stock" scenarios.

### 📦 Module 3: Inventory (Product) Management
A comprehensive CRUD (Create, Read, Update, Delete) module for managing sports gear.
*   **Details Tracked:** Product name, category, supplier, cost price, selling price, and current quantity.
*   **Image Management:** Supports uploading product photos to the server for visual identification in the POS.
*   **Status Control:** Products can be marked as "Active" or "Inactive" to control their visibility in the billing section.

### 💳 Module 4: Billing & POS (Point of Sale)
The most critical module for business operations.
*   **Cart System:** Employees can add multiple products to a temporary cart.
*   **Dynamic Calculations:** Automatically calculates Subtotal, GST (as per store settings), and applied Discounts.
*   **Payment Integration:** Supports **Cash, UPI, and Card**. For digital payments, it records Transaction IDs and UPI IDs for bank reconciliation.
*   **Receipt Generation:** Generates a professional, print-ready digital receipt for the customer upon successful sale.

### 👥 Module 5: Employee Management (Admin Only)
Manages the staff database and payroll information.
*   **Details:** Tracks Name, Contact, Email, Education, Work Shift, and Salary.
*   **Access Control:** Only the Admin can add new staff members or modify existing employee records to ensure confidentiality.

### 🚚 Module 6: Supplier Management
Maintains relationships with vendors who provide the sports equipment.
*   **Invoicing:** Links products to specific supplier invoice numbers.
*   **Efficiency:** Allows the store owner to quickly contact suppliers when stock is low, ensuring the supply chain remains uninterrupted.

### 📋 Module 7: Sales History & Reporting
A data log of every transaction ever made.
*   **Filtering:** Filters sales records by date range (Start Date to End Date).
*   **Profit Analysis:** (Admin View Only) Calculates net profit for each bill by comparing Cost Price vs. Selling Price.
*   **Payment Audit:** Displays colored badges showing how each customer paid (Cash/UPI/Card).

### ⚙️ Module 8: System Settings
Allows the admin to configure global store parameters.
*   **Financials:** Set global GST percentages and default store discounts.
*   **Branding:** Update store name, contact email, address, and upload the official store logo to be printed on receipts.

---

**Summary:** Together, these modules create a seamless workflow where data flows from the Supplier (Restocking) to Inventory (Storage) to the POS (Sales) and finally to the Dashboard (Analysis).
