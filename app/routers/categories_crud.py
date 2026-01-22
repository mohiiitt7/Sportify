from fastapi import APIRouter, Depends, Request, Cookie, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import database, models

router = APIRouter(tags=["Categories CRUD"])

# Add Category
@router.post("/categories/add")
def add_category(
    name: str = Form(...),
    description: str = Form(None),
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        # Check if category with same name already exists
        existing = db.query(models.Category).filter(models.Category.name == name).first()
        if existing:
            return RedirectResponse(url="/categories?error=exists", status_code=303)
        
        # Manual ID Generation
        last_cat = db.query(models.Category).order_by(models.Category.id.desc()).first()
        next_id = (last_cat.id + 1) if last_cat else 1
        
        new_cat = models.Category(
            id=next_id,
            name=name,
            description=description
        )
        db.add(new_cat)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error adding category: {e}")
        return RedirectResponse(url=f"/categories?error={str(e)}", status_code=303)
    
    return RedirectResponse(url="/categories?success=1", status_code=303)

# Edit Category
@router.post("/categories/edit")
def edit_category(
    category_id: int = Form(...),
    name: str = Form(...),
    description: str = Form(None),
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if category:
            category.name = name
            category.description = description
            db.commit()
        else:
            print(f"DEBUG: Category {category_id} not found")
    except Exception as e:
        db.rollback()
        print(f"DEBUG: Error editing category: {e}")
    
    return RedirectResponse(url="/categories?success=1", status_code=303)

# Delete Category
@router.post("/categories/delete/{category_id}")
def delete_category(
    category_id: int,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if category:
            db.delete(category)
            db.commit()
        else:
            print(f"DEBUG: Category {category_id} not found")
    except Exception as e:
        db.rollback()
        print(f"DEBUG: Error deleting category: {e}")
    
    return RedirectResponse(url="/categories?success=1", status_code=303)
