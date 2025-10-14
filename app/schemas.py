from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from datetime import datetime, date 

# ===== User Schemas =====

class UserBase(BaseModel):
    """
    Base user fields shared across schemas
    """
    email: EmailStr  # Validates email format
    first_name: str
    last_name: str


class UserCreate(UserBase):
    """
    Schema for creating a new user (registration)
    Includes password which we don't want in other schemas
    """
    password: str = Field(min_length=8)  # Password must be at least 8 characters


class UserResponse(UserBase):
    """
    Schema for returning user data (no password!)
    """
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows SQLAlchemy models to be converted


# ===== Authentication Schemas =====

class Token(BaseModel):
    """
    Schema for JWT token response after login
    """
    access_token: str
    token_type: str  # Will always be "bearer"


class TokenData(BaseModel):
    """
    Schema for data stored inside JWT token
    """
    email: Optional[str] = None


class CategoryBase(BaseModel):
    """
    Base category fields shared across schemas
    """
    name: str  # Category name like "Groceries", "Rent"
    type: str  # Must be 'income' or 'expense'


class CategoryCreate(CategoryBase):
    """
    Schema for creating a new category
    Inherits name and type from CategoryBase
    """
    pass


class CategoryUpdate(BaseModel):
    """
    Schema for updating a category
    All fields optional - update only what's provided
    """
    name: Optional[str] = None
    type: Optional[str] = None


class CategoryResponse(CategoryBase):
    """
    Schema for returning category data to client
    Includes database fields like id and user_id
    """
    id: int
    user_id: int
    
    class Config:
        from_attributes = True  # Allows SQLAlchemy models to be converted

# ===== Expense Schemas =====

class ExpenseBase(BaseModel):
    """
    Base expense fields
    """
    category_id: int
    amount: float
    description: str
    date: date  


class ExpenseCreate(ExpenseBase):
    """
    Schema for creating expense
    Inherits all fields from ExpenseBase
    """
    pass


class ExpenseUpdate(BaseModel):
    """
    Schema for updating expense
    All fields optional
    """
    category_id: Optional[int] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[datetime] = None


class ExpenseResponse(ExpenseBase):
    """
    Schema for returning expense data
    Includes database-generated fields
    """
    id: int
    user_id: int
    created_at: datetime  # When record was created in database
    
    class Config:
        from_attributes = True

# ===== Analytics Schemas =====
class MonthlySummary(BaseModel):
    """
    Monthly spending/income summary
    """
    month: str  # Format: "2025-10"
    total_income: float
    total_expenses: float
    net_balance: float  # income - expenses
    
class CategorySummary(BaseModel):
    """
    Summary by category
    """
    category_id: int
    category_name: str
    category_type: str
    total_amount: float
    transaction_count: int
    
class DashboardSummary(BaseModel):
    """
    Overall dashboard statistics
    """
    total_income: float
    total_expenses: float
    net_balance: float
    top_expense_category: Optional[str] = None
    top_income_category: Optional[str] = None