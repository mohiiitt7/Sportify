from app.database import SessionLocal, engine
from app import models
from app.models import Employee

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if employee exists
if not db.query(Employee).filter_by(email="test@sportify.com").first():
    new_emp = Employee(
        name="Test Employee",
        email="test@sportify.com",
        password="password123",
        userType="Employee",
        eid=101,
        contact="1234567890"
    )
    db.add(new_emp)
    db.commit()
    print("Test employee created.")
else:
    print("Test employee already exists.")

db.close()
