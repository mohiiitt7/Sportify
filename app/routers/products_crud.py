from fastapi import APIRouter, Depends, Request, Cookie, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import database, models

router = APIRouter(tags=["Products CRUD"])

# Add Product
@router.post("/products/add")
def add_product(
    name: str = Form(...),
    category: str = Form(...),
    supplier: str = Form(...),
    price: float = Form(...),
    cost_price: float = Form(0.0),
    discount: int = Form(0),
    quantity: int = Form(0),
    status: str = Form("Active"),
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        # Check if product with same name already exists
        existing = db.query(models.Product).filter(models.Product.name == name).first()
        if existing:
            return RedirectResponse(url="/products?error=exists", status_code=303)
        
        # Manual ID Generation (as per legacy DB schema without auto-increment)
        last_product = db.query(models.Product).order_by(models.Product.id.desc()).first()
        next_id = (last_product.id + 1) if last_product else 1
        
        # Calculate discounted price
        discounted_price = price - (price * discount / 100) if discount > 0 else price
        
        new_product = models.Product(
            id=next_id,
            name=name,
            category=category,
            supplier=supplier,
            price=price,
            cost_price=cost_price,
            discount=discount,
            discounted_price=discounted_price,
            quantity=quantity,
            status=status
        )
        db.add(new_product)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error adding product: {e}")
        return RedirectResponse(url=f"/products?error={str(e)}", status_code=303)
    
    return RedirectResponse(url="/products?success=1", status_code=303)

# Edit Product
@router.post("/products/edit")
def edit_product(
    product_id: int = Form(...),
    name: str = Form(...),
    category: str = Form(...),
    supplier: str = Form(...),
    price: float = Form(...),
    cost_price: float = Form(0.0),
    discount: int = Form(0),
    quantity: int = Form(0),
    status: str = Form("Active"),
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    print(f"DEBUG: Editing product id={product_id}, name={name}")
    try:
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if product:
            product.name = name
            product.category = category
            product.supplier = supplier
            product.price = price
            product.cost_price = cost_price
            product.discount = discount
            product.discounted_price = price - (price * discount / 100) if discount > 0 else price
            product.quantity = quantity
            product.status = status
            db.commit()
            print(f"DEBUG: Product {product_id} updated successfully")
        else:
            print(f"DEBUG: Product {product_id} not found")
    except Exception as e:
        db.rollback()
        print(f"DEBUG: Error editing product: {e}")
    
    return RedirectResponse(url="/products?success=1", status_code=303)

# Delete Product
@router.post("/products/delete/{product_id}")
def delete_product(
    product_id: int,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    print(f"DEBUG: Deleting product id={product_id}")
    try:
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            print(f"DEBUG: Product {product_id} deleted successfully")
        else:
            print(f"DEBUG: Product {product_id} not found")
    except Exception as e:
        db.rollback()
        print(f"DEBUG: Error deleting product: {e}")
    
    return RedirectResponse(url="/products?success=1", status_code=303)
