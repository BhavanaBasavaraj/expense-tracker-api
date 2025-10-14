from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date  # ← CHANGED: removed datetime, only need date
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=schemas.ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Create a new expense
    
    Validation:
    1. Category must exist and belong to user
    2. Amount must be greater than 0
    3. Date cannot be in the future
    """
    # Verify category exists and belongs to current user
    category = db.query(models.Category).filter(
        models.Category.id == expense.category_id,
        models.Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Validate amount is positive
    if expense.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than 0"
        )
    
    # Validate date is not in future  ← NEW VALIDATION
    if expense.date > date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expense date cannot be in the future"
        )
    
    # Create expense
    new_expense = models.Expense(
        user_id=current_user.id,
        category_id=expense.category_id,
        amount=expense.amount,
        description=expense.description,
        date=expense.date
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/", response_model=List[schemas.ExpenseResponse])
def get_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Get all expenses for current user
    
    Query parameters:
    - skip: number of records to skip (for pagination)
    - limit: max records to return (1-100)
    - category_id: filter by specific category (optional)
    """
    # Start with base query - only user's expenses
    query = db.query(models.Expense).filter(models.Expense.user_id == current_user.id)
    
    # Apply category filter if provided
    if category_id:
        query = query.filter(models.Expense.category_id == category_id)
    
    # Order by date descending (newest first)
    query = query.order_by(models.Expense.date.desc())
    
    # Apply pagination
    expenses = query.offset(skip).limit(limit).all()
    return expenses


@router.get("/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Get specific expense by ID
    """
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense


@router.put("/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_update: schemas.ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Update an expense
    
    Validation:
    - If updating category, verify it exists and belongs to user
    - If updating amount, verify it's positive
    - If updating date, verify it's not in the future
    """
    # Find expense
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Validate category if updating
    if expense_update.category_id:
        category = db.query(models.Category).filter(
            models.Category.id == expense_update.category_id,
            models.Category.user_id == current_user.id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        expense.category_id = expense_update.category_id
    
    # Validate amount if updating
    if expense_update.amount is not None:  # Check is not None because 0 is falsy
        if expense_update.amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount must be greater than 0"
            )
        expense.amount = expense_update.amount
    
    # Update description if provided
    if expense_update.description:
        expense.description = expense_update.description
    
    # Validate and update date if provided  ← NEW VALIDATION
    if expense_update.date:
        if expense_update.date > date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Expense date cannot be in the future"
            )
        expense.date = expense_update.date
    
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Delete an expense
    """
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    db.delete(expense)
    db.commit()
    return None