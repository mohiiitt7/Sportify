# 🏆 Sportify - Sports Store Management System

**Sportify** is a modern and powerful Sports Store Management Web Application built using **FastAPI** (Python) and **PostgreSQL**. It is designed to streamline inventory management, supplier tracking, employee coordination, and sales operations.

---

## 🚀 Key Features

### 📊 1. Intelligent Dashboard
- **Real-time Statistics:** Instant overview of total employees, suppliers, products, and total revenue.
- **Data Visualization:** Interactive charts for weekly sales trends and top-selling product categories.
- **Low Stock Alerts:** Automated notifications when product inventory falls below a certain threshold.

### 💳 2. Advanced Billing & POS (Point of Sale)
- **POS Interface:** Optimized interface for generating bills quickly.
- **Multiple Payment Methods:** Integrated support for **Cash, UPI, and Card** payments.
- **Transaction Tracking:** Ability to store Transaction IDs for digital payments to simplify reconciliation.
- **Tax & Discounts:** Automatic calculation of GST and discounts on every bill.

### 📦 3. Inventory & Supplier Management
- **Complete CRUD:** Add, Edit, and Delete products with photo upload support.
- **Supplier Directory:** Manage third-party vendors and track their specific invoice details.
- **Categorization:** Organize sports gear into categories for better-targeted sales analysis.

### 🔐 4. Security & User Experience
- **Role-Based Access Control (RBAC):** Distinct permissions for **Admin** and **Employee** roles.
- **Secure Authentication:** Password hashing using `Passlib` (Bcrypt).
- **Modern UI:** Added a "Show/Hide Password" toggle on the login page for enhanced user convenience.

---

## 🛠️ Tech Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python Framework)
- **Database:** [PostgreSQL](https://www.postgresql.org/) with SQLAlchemy ORM
- **Frontend:** HTML5, CSS3, [Bootstrap 5](https://getbootstrap.com/), JavaScript
- **Templates:** Jinja2
- **Security:** OAuth2 with Password Hashing
- **Visuals:** [Chart.js](https://www.chartjs.org/) for analytics

---

## 📂 Project Structure

```text
sportifyy/
├── app/
│   ├── main.py            # Application entry point
│   ├── database.py        # Database connection & session setup
│   ├── models.py          # SQLAlchemy Database Models
│   ├── routers/           # Business logic & API routes
│   ├── static/            # CSS, JS, and uploaded assets
│   └── templates/         # Jinja2 HTML templates
├── requirements.txt       # Project dependencies
└── migrate_*.py           # Database migration scripts
```

---

## ⚙️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/sportifyy.git
   cd sportifyy
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration:**
   Update your PostgreSQL credentials in `app/database.py` and run the migration scripts:
   ```bash
   python migrate_payment_integration.py
   ```

5. **Run the Application:**
   ```bash
   uvicorn app.main:app --reload
   ```
   *Access the app at: `http://localhost:8000`*

---

## 🎯 Future Roadmap

- **Dynamic QR Generation:** Feature to generate per-bill UPI QR codes.
- **Cloud Integration:** Deploying the system to AWS or Google Cloud.
- **WhatsApp API:** Sending digital receipts directly to customers' phone numbers.
- **Export Reports:** One-click export of sales reports to Excel or PDF.

---

## 📄 License
This project is licensed under the MIT License.

---

**Developed with ❤️ by Mohit**
