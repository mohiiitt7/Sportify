from fastapi import APIRouter, Depends, Request, Cookie, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import database, models

router = APIRouter(tags=["Employees CRUD"])

# Add Employee
@router.post("/employees/add")
def add_employee(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    contact: str = Form(""),
    emp_type: str = Form("Full time"),
    work_shift: str = Form("Morning"),
    usertype: str = Form("Employee"),
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        # Get next EID
        last_emp = db.query(models.Employee).order_by(models.Employee.eid.desc()).first()
        next_eid = (last_emp.eid + 1) if last_emp else 1
        
        new_employee = models.Employee(
            eid=next_eid,
            name=name,
            email=email,
            password=password,  # Note: In production, hash this password!
            contact=contact,
            emp_type=emp_type,
            work_shift=work_shift,
            usertype=usertype
        )
        db.add(new_employee)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error adding employee: {e}")
    
    return RedirectResponse(url="/employees?success=1", status_code=303)

# Edit Employee
@router.post("/employees/edit")
def edit_employee(
    eid: int = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    contact: str = Form(""),
    emp_type: str = Form("Full time"),
    work_shift: str = Form("Morning"),
    usertype: str = Form("Employee"),
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    print(f"DEBUG: Editing employee eid={eid}, name={name}, email={email}")
    try:
        employee = db.query(models.Employee).filter(models.Employee.eid == eid).first()
        if employee:
            print(f"DEBUG: Found employee - Current name: {employee.name}")
            employee.name = name
            employee.email = email
            employee.contact = contact
            employee.emp_type = emp_type
            employee.work_shift = work_shift
            employee.usertype = usertype
            print(f"DEBUG: Updated employee object - New name: {employee.name}")
            db.flush()  # Flush changes to database
            db.commit()
            db.refresh(employee)  # Refresh to get latest state
            print(f"DEBUG: Employee {eid} updated successfully - Verified name: {employee.name}")
        else:
            print(f"DEBUG: Employee {eid} not found")
    except Exception as e:
        db.rollback()
        print(f"DEBUG: Error editing employee: {e}")
        import traceback
        traceback.print_exc()
    
    return RedirectResponse(url="/employees?success=1", status_code=303)

# Delete Employee
@router.post("/employees/delete/{eid}")
def delete_employee(
    eid: int,
    user_email: str = Cookie(None),
    user_role: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not user_email or user_role != "Admin":
        return RedirectResponse(url="/login", status_code=303)
    
    print(f"DEBUG: Deleting employee eid={eid}")
    try:
        employee = db.query(models.Employee).filter(models.Employee.eid == eid).first()
        if employee:
            db.delete(employee)
            db.commit()
            print(f"DEBUG: Employee {eid} deleted successfully")
        else:
            print(f"DEBUG: Employee {eid} not found")
    except Exception as e:
        db.rollback()
        print(f"DEBUG: Error deleting employee: {e}")
    
    return RedirectResponse(url="/employees?success=1", status_code=303)
