from fastapi import APIRouter, Depends, Request, Cookie, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import database, models
import shutil
import os

router = APIRouter(tags=["Dashboard"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")

    # Fetch stats
    try:
        total_employees = db.query(models.Employee).count()
    except:
        total_employees = 0

    try:
        total_suppliers = db.query(models.Supplier).count()
    except:
        total_suppliers = 0

    try:
        total_categories = db.query(models.Category).count()
    except:
        total_categories = 0

    try:
        total_products = db.query(models.Product).count()
    except:
        total_products = 0
    
    total_customers = 0

    
    # Calculate Total Sales (Revenue)
    total_sales_amount = 0
    try:
        sales_data = db.query(models.Sale).all()
        total_sales_amount = sum(float(s.net_amount) for s in sales_data)
    except:
        total_sales_amount = 0
        
    # Get Recent Orders (Last 5)
    recent_sales = []
    try:
        recent_sales = db.query(models.Sale).order_by(models.Sale.bill_date.desc()).limit(5).all()
    except:
        recent_sales = []

    # Fetch All Products for mapping and low stock alerts
    products_data = []
    products = []
    low_stock_products = []
    try:
        products = db.query(models.Product).all()
        for p in products:
            products_data.append({"name": p.name, "qty": p.quantity})
            if p.quantity is not None and p.quantity <= 5:
                low_stock_products.append(p)
    except Exception as e:
        print(f"Error fetching products: {e}")

    # --- Chart Data Calculation ---
    from datetime import datetime, timedelta
    
    # 1. Weekly Sales Data (Last 7 Days)
    daily_sales = {}
    today = datetime.now().date()
    # Initialize labels for last 7 days
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        daily_sales[day.strftime("%a")] = 0.0
    
    try:
        for sale in sales_data:
            s_date = sale.bill_date.date()
            if s_date >= (today - timedelta(days=6)):
                day_name = s_date.strftime("%a")
                if day_name in daily_sales:
                    daily_sales[day_name] += float(sale.net_amount)
    except:
        pass
    
    daily_sales_labels = list(daily_sales.keys())
    daily_sales_values = list(daily_sales.values())

    # 2. Category-wise Sales Data (Top Selling Sports Gear)
    category_sales_map = {}
    try:
        # Create a mapping of Product Name -> Category
        product_cat_map = {p.name: p.category for p in products}
        
        for sale in sales_data:
            if not sale.items_summary: continue
            import re
            # Parse items_summary: "Product Name xQuantity (₹Price), ..."
            # Regex to match: Name xQty (₹Price)
            # Example: "Bat x2 (₹500.00)"
            item_pattern = re.compile(r"^(.*?) x(\d+) \(₹(.*?)\)$")

            items = sale.items_summary.split(', ')
            for item_str in items:
                try:
                    match = item_pattern.match(item_str)
                    if match:
                        name_part = match.group(1)
                        qty = int(match.group(2))
                        
                        category = product_cat_map.get(name_part, "Other")
                        category_sales_map[category] = category_sales_map.get(category, 0) + qty
                except:
                    continue
    except Exception as e:
        print(f"Error calculating category sales: {e}")

    # Sort categories by sales volume and take top ones
    sorted_categories = sorted(category_sales_map.items(), key=lambda x: x[1], reverse=True)
    category_labels = [c[0] for c in sorted_categories]
    category_values = [c[1] for c in sorted_categories]


    context = {
        "request": request,
        "total_employees": total_employees,
        "total_suppliers": total_suppliers,
        "total_categories": total_categories,
        "total_products": total_products,
        "total_customers": total_customers,
        "total_sales": total_sales_amount,
        "recent_sales": recent_sales,
        "products_data": products_data,
        "low_stock_products": low_stock_products,
        "user_role": user_role,
        "daily_sales_labels": daily_sales_labels,
        "daily_sales_values": daily_sales_values,
        "category_labels": category_labels,
        "category_values": category_values
    }

    try:
        return templates.TemplateResponse("dashboard.html", context)
    except Exception as e:
        import traceback
        print(f"Error rendering dashboard template: {e}")
        print(traceback.format_exc())
        return HTMLResponse(content=f"<h1>Internal Server Error</h1><p>Error rendering template: {e}</p><pre>{traceback.format_exc()}</pre>", status_code=500)

# Products Page
@router.get("/products", response_class=HTMLResponse)
def products(
    request: Request,
    status: str = None,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    # Filter products logic
    query = db.query(models.Product)
    
    # If user is NOT Admin (i.e. Employee), FORCE filter to "Active" only
    if user_role != "Admin":
        products_list = query.filter(models.Product.status == "Active").order_by(models.Product.id.asc()).all()
    else:
        # Admin Logic (Existing)
        if status:
            products_list = query.filter(models.Product.status == status).order_by(models.Product.id.asc()).all()
        else:
            products_list = query.order_by(models.Product.id.asc()).all()
    
    categories_list = db.query(models.Category).order_by(models.Category.name.asc()).all()
    suppliers_list = db.query(models.Supplier).order_by(models.Supplier.name.asc()).all()

    context = {
        "request": request,
        "products": products_list,
        "categories": categories_list,
        "suppliers": suppliers_list,
        "user_role": user_role,
        "status_filter": status  # Pass filter to template for UI state
    }
    return templates.TemplateResponse("products.html", context)

# Employees Page
@router.get("/employees", response_class=HTMLResponse)
def employees(
    request: Request,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    if user_role != "Admin":
        return RedirectResponse(url="/dashboard")
    
    employees_list = db.query(models.Employee).order_by(models.Employee.eid.asc()).all()
    context = {
        "request": request,
        "employees": employees_list,
        "user_role": user_role
    }
    return templates.TemplateResponse("employees.html", context)

# Suppliers Page
@router.get("/suppliers", response_class=HTMLResponse)
def suppliers(
    request: Request,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    if user_role != "Admin":
        return RedirectResponse(url="/dashboard")
    
    suppliers_list = db.query(models.Supplier).order_by(models.Supplier.invoice.asc()).all()
    context = {
        "request": request,
        "suppliers": suppliers_list,
        "user_role": user_role
    }
    return templates.TemplateResponse("suppliers.html", context)

# Categories Page
@router.get("/categories", response_class=HTMLResponse)
def categories(
    request: Request,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    if user_role != "Admin":
        return RedirectResponse(url="/dashboard")
    
    categories_list = db.query(models.Category).order_by(models.Category.id.asc()).all()
    context = {
        "request": request,
        "categories": categories_list,
        "user_role": user_role
    }
    return templates.TemplateResponse("categories.html", context)

# Billing Page
@router.get("/billing", response_class=HTMLResponse)
def billing(
    request: Request,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    context = {
        "request": request,
        "user_role": user_role
    }
    return templates.TemplateResponse("billing.html", context)

# Orders/Sales Page
@router.get("/orders", response_class=HTMLResponse)
@router.get("/sales", response_class=HTMLResponse)
def orders(
    request: Request,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    start_date: str = None, # format YYYY-MM-DD
    end_date: str = None,   # format YYYY-MM-DD
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    query = db.query(models.Sale)
    
    if start_date:
        from datetime import datetime
        try:
            # Parse start date and set time to 00:00:00
            s_date = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(models.Sale.bill_date >= s_date)
        except:
             pass # Ignore invalid date
             
    if end_date:
        from datetime import datetime, timedelta
        try:
             # Parse end date and set time to 23:59:59 (essentially next day 00:00)
            e_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            query = query.filter(models.Sale.bill_date < e_date)
        except:
            pass

    # Fetch ordered sales
    sales_list = query.order_by(models.Sale.bill_date.desc()).all()
    
    context = {
        "request": request,
        "user_role": user_role,
        "sales": sales_list,
        "start_date": start_date,
        "end_date": end_date
    }
    return templates.TemplateResponse("orders.html", context)

# Cart - Add to cart
@router.post("/add-to-cart")
def add_to_cart(
    request: Request,
    product_id: int = Form(...),
    quantity: int = Form(1),
    user_email: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        cart_item = models.Cart(
            name=product.name,
            price=product.price,
            quantity=quantity
        )
        db.add(cart_item)
        db.commit()
    
    return RedirectResponse(url="/products", status_code=303)

# Remove from Cart
@router.post("/remove-from-cart")
def remove_from_cart(
    request: Request,
    cart_id: int = Form(...),
    user_email: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    cart_item = db.query(models.Cart).filter(models.Cart.cid == cart_id).first()
    if cart_item:
        db.delete(cart_item)
        db.commit()
    
    return RedirectResponse(url="/cart", status_code=303)

# View Cart
@router.get("/cart", response_class=HTMLResponse)
def view_cart(
    request: Request,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    cart_items = db.query(models.Cart).all()
    total = sum(float(item.price) * item.quantity for item in cart_items)
    
    # Get settings for tax/discount
    settings = db.query(models.Settings).first()
    if not settings:
        settings = models.Settings(id=1, gst_percent=18.00, discount_percent=0.00)

    context = {
        "request": request,
        "cart_items": cart_items,
        "total": total,
        "user_role": user_role,
        "settings": settings
    }
    return templates.TemplateResponse("cart.html", context)

# Generate Bill
@router.post("/generate-bill")
def generate_bill(
    request: Request,
    customer_name: str = Form(...),
    customer_contact: str = Form(...),
    payment_method: str = Form("Cash"),
    transaction_id: str = Form(None),
    upi_id: str = Form(None),
    card_last4: str = Form(None),
    user_email: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    # Get Cart Items
    cart_items = db.query(models.Cart).all()
    if not cart_items:
        return RedirectResponse(url="/cart")
    
    # Basic Total
    total_amount = sum(float(item.price) * item.quantity for item in cart_items)
    
    # Get Settings for Calculation
    settings = db.query(models.Settings).first()
    if not settings:
        settings = models.Settings(id=1, gst_percent=18.00, discount_percent=0.00)
    
    # Calculations
    gst_val = total_amount * (float(settings.gst_percent) / 100)
    discount_val = total_amount * (float(settings.discount_percent) / 100)
    net_amount = total_amount + gst_val - discount_val
    
    # Create Items Summary and Calculate Profit
    items_list = []
    total_profit = 0
    
    # We need to iterate differently because we need Product data for profit calc
    # But product fetching is done later in the code. Let's do a pass here or combine.
    # It's better to fetch product info while building summary to get cost price.
    
    # Let's refactor the loop to fetch products first.
    
    # Dictionary to hold product objects map to cart items
    # Actually, let's just loop through cart items, fetch product, update calc, add summary. 
    # But wait, original code did fetching later to reduce stock.
    # We can fetch here.
    
    final_cart_items = [] # Store tuple (cart_item, product_obj)
    
    for item in cart_items:
        product = db.query(models.Product).filter(models.Product.name == item.name).first()
        if product:
             # Calculate profit for this item lineup
             # Profit = (Selling Price - Cost Price) * Qty
             # Selling Price here is item.price (from cart, which came from product.price)
             # Cost Price is product.cost_price
             
             cost = float(product.cost_price) if product.cost_price else 0.0
             selling = float(item.price)
             item_profit = (selling - cost) * item.quantity
             total_profit += item_profit
             
             items_list.append(f"{item.name} x{item.quantity} (₹{item.price})")
             final_cart_items.append((item, product))
        else:
             # Product deleted? Just add summary
             items_list.append(f"{item.name} x{item.quantity} (₹{item.price})")
             # No profit if product not found/cost unknown
             
    items_summary = ", ".join(items_list)
    
    # Create Sale Record with Payment Details
    new_sale = models.Sale(
        customer_name=customer_name,
        customer_contact=customer_contact,
        total_amount=total_amount,
        gst_amount=gst_val,
        discount_amount=discount_val,
        net_amount=net_amount,
        profit=total_profit,
        items_summary=items_summary,
        payment_method=payment_method,
        payment_status="Completed",
        transaction_id=transaction_id if transaction_id else None,
        upi_id=upi_id if upi_id else None,
        card_last4=card_last4 if card_last4 else None
    )
    db.add(new_sale)
    
    # Reduce Product Quantity
    for item, product in final_cart_items:
        if product:
            # Ensure quantity doesn't go below 0
            if product.quantity >= item.quantity:
                product.quantity -= item.quantity
            else:
                product.quantity = 0 # Or handle error appropriately
    
    # Clear cart after billing
    db.query(models.Cart).delete()
    db.commit()
    db.refresh(new_sale)
    
    return RedirectResponse(url=f"/receipt/{new_sale.bill_id}", status_code=303)

# Receipt Page
@router.get("/receipt/{bill_id}", response_class=HTMLResponse)
def receipt_page(
    request: Request,
    bill_id: int,
    user_email: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    sale = db.query(models.Sale).filter(models.Sale.bill_id == bill_id).first()
    if not sale:
        return RedirectResponse(url="/dashboard")
        
    settings = db.query(models.Settings).first()
    if not settings:
        settings = models.Settings(shop_name="Sportify Store", shop_contact="+91 9999999999", shop_email="contact@sportify.com", shop_address="123 Sportify Street, India")

    context = {
        "request": request,
        "sale": sale,
        "settings": settings
    }
    return templates.TemplateResponse("receipt.html", context)



# Bill Success Page
@router.get("/bill-success", response_class=HTMLResponse)
def bill_success(
    request: Request,
    total: float = 0,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    context = {
        "request": request,
        "total": total,
        "user_role": user_role
    }
    return templates.TemplateResponse("bill_success.html", context)

# Admin Settings Page (GST & Discount)
@router.get("/settings", response_class=HTMLResponse)
def settings_page(
    request: Request,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email:
        return RedirectResponse(url="/login")
    
    # Only Admin can access settings
    if user_role != "Admin":
        return RedirectResponse(url="/dashboard")
    
    # Get or create settings
    settings = db.query(models.Settings).first()
    if not settings:
        settings = models.Settings(id=1, gst_percent=18.00, discount_percent=0.00)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    context = {
        "request": request,
        "settings": settings,
        "user_role": user_role,
        "success": request.query_params.get("success", None)
    }
    return templates.TemplateResponse("settings.html", context)

# Update Settings
@router.post("/settings")
def update_settings(
    request: Request,
    gst_percent: float = Form(...),
    discount_percent: float = Form(...),
    shop_name: str = Form(...),
    shop_contact: str = Form(...),
    shop_email: str = Form(...),
    shop_address: str = Form(...),
    shop_logo: UploadFile = File(None),
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login")
    
    settings = db.query(models.Settings).first()
    if not settings:
        settings = models.Settings(id=1)
        db.add(settings)
    
    settings.gst_percent = gst_percent
    settings.discount_percent = discount_percent
    settings.shop_name = shop_name
    settings.shop_contact = shop_contact
    settings.shop_email = shop_email
    settings.shop_address = shop_address
    
    # Handle Logo Upload
    if shop_logo and shop_logo.filename:
        # Create directory if it doesn't exist
        os.makedirs("app/static/uploads", exist_ok=True)
        file_path = f"app/static/uploads/logo_{shop_logo.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(shop_logo.file, buffer)
        settings.shop_logo = f"/static/uploads/logo_{shop_logo.filename}"
    
    db.commit()
    return RedirectResponse(url="/settings?success=1", status_code=303)

