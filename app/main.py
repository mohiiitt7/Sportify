from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app import models
from app.database import engine

from app.routers import auth, dashboard, products_crud, employees_crud, suppliers_crud, categories_crud

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sportify Web")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(products_crud.router)
app.include_router(employees_crud.router)
app.include_router(suppliers_crud.router)
app.include_router(categories_crud.router)

@app.get("/")
def read_root():
    return RedirectResponse(url="/login")
