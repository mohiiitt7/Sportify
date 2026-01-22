from fastapi import APIRouter, Depends, status, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import database, models

router = APIRouter(tags=["Authentication"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    # Hardcoded Admin Check (from legacy code)
    if email == "mohit07@gmail.com" and password == "mohit123":
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="user_role", value="Admin")
        response.set_cookie(key="user_email", value=email)
        return response

    # Database Check for Employees
    # Database Check for Employees
    employee = db.query(models.Employee).filter(models.Employee.email == email).first()
    
    if employee and employee.password == password: # In real app, hash passwords!
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="user_role", value=employee.usertype)
        response.set_cookie(key="user_email", value=email)
        return response
    
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid Credentials"})

@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("user_role")
    response.delete_cookie("user_email")
    return response
