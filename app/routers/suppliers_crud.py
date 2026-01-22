from fastapi import APIRouter, Depends, Request, Cookie, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import database, models

router = APIRouter(tags=["Suppliers CRUD"])

# Add Supplier
@router.post("/suppliers/add")
def add_supplier(
    name: str = Form(...),
    contact: str = Form(...),
    description: str = Form(""),
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        # Get next invoice number
        last_supplier = db.query(models.Supplier).order_by(models.Supplier.invoice.desc()).first()
        next_invoice = (last_supplier.invoice + 1) if last_supplier else 1
        
        new_supplier = models.Supplier(
            invoice=next_invoice,
            name=name,
            contact=contact,
            discription=description  # Note: Model has typo 'discription'
        )
        db.add(new_supplier)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error adding supplier: {e}")
        # Could add a flash message here if system supported it
    
    return RedirectResponse(url="/suppliers?success=1", status_code=303)

# Edit Supplier
@router.post("/suppliers/edit")
def edit_supplier(
    invoice: int = Form(...),
    name: str = Form(...),
    contact: str = Form(...),
    description: str = Form(""),
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    print(f"DEBUG: Editing supplier invoice={invoice}, name={name}")
    try:
        supplier = db.query(models.Supplier).filter(models.Supplier.invoice == invoice).first()
        if supplier:
            supplier.name = name
            supplier.contact = contact
            supplier.discription = description
            db.commit()
            print(f"DEBUG: Supplier {invoice} updated successfully")
        else:
            print(f"DEBUG: Supplier {invoice} not found")
    except Exception as e:
        db.rollback()
        print(f"DEBUG: Error editing supplier: {e}")
    
    return RedirectResponse(url="/suppliers?success=1", status_code=303)

# Delete Supplier
@router.post("/suppliers/delete/{invoice}")
def delete_supplier(
    invoice: int,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    print(f"DEBUG: Deleting supplier invoice={invoice}")
    try:
        supplier = db.query(models.Supplier).filter(models.Supplier.invoice == invoice).first()
        if supplier:
            db.delete(supplier)
            db.commit()
            print(f"DEBUG: Supplier {invoice} deleted successfully")
        else:
            print(f"DEBUG: Supplier {invoice} not found")
    except Exception as e:
        db.rollback()
        print(f"DEBUG: Error deleting supplier: {e}")
    
    return RedirectResponse(url="/suppliers?success=1", status_code=303)
