from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    """
    User table - stores user account information
    """
    __tablename__ = "users"
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships - one user has many expenses and categories
    # cascade="all, delete-orphan" means: delete expenses if user deleted
    expenses = relationship("Expense", back_populates="owner", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="owner", cascade="all, delete-orphan")


class Category(Base):
    """
    Category table - expense categories like 'Food', 'Rent', etc.
    Each category belongs to one user
    """
    __tablename__ = "categories"
    
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)  # e.g., "Groceries"
    type = Column(String, nullable=False)  # 'income' or 'expense'
    
    # Relationships
    owner = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category", cascade="all, delete-orphan")


class Expense(Base):
    """
    Expense table - individual expense/income records
    Each expense belongs to one user and one category
    """
    __tablename__ = "expenses"
    
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)  # Dollar amount
    description = Column(String, nullable=False)  # What was purchased
    date = Column(DateTime(timezone=True), nullable=False)  # When it happened
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")

