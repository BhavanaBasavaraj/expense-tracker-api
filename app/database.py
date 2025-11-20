

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
# Database connection string
# Format: postgresql://username@localhost/database_name
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://bhavana@localhost/expense_tracker"  # Fallback for local dev
)

# Create database engine - manages connections
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session factory - opens/closes database connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Dependency function - provides database session to endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide session to endpoint
    finally:
        db.close()  # Always close connection when done
