from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database connection string
# Format: postgresql://username@localhost/database_name
# Replace YOUR_USERNAME with the output from 'whoami' command
SQLALCHEMY_DATABASE_URL = "postgresql://bhavana@localhost/expense_tracker"

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
