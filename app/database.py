from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL format: postgresql://user:password@host/db_name
# Using credentials from legacy code: postgres / mohit#2003
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mohit#2003@localhost/sportify18"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
