from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List
from datetime import datetime
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/dashboard", response_model=schemas.DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Get overall dashboard statistics
    """
    # Get total income
    total_income = db.query(func.sum(models.Expense.amount)).join(
        models.Category
    ).filter(
        models.Expense.user_id == current_user.id,
        models.Category.type == 'income'
    ).scalar() or 0
    
    # Get total expenses
    total_expenses = db.query(func.sum(models.Expense.amount)).join(
        models.Category
    ).filter(
        models.Expense.user_id == current_user.id,
        models.Category.type == 'expense'
    ).scalar() or 0
    
    # Get top expense category
    top_expense = db.query(
        models.Category.name,
        func.sum(models.Expense.amount).label('total')
    ).join(
        models.Expense
    ).filter(
        models.Expense.user_id == current_user.id,
        models.Category.type == 'expense'
    ).group_by(
        models.Category.id, models.Category.name
    ).order_by(
        func.sum(models.Expense.amount).desc()
    ).first()
    
    # Get top income category
    top_income = db.query(
        models.Category.name,
        func.sum(models.Expense.amount).label('total')
    ).join(
        models.Expense
    ).filter(
        models.Expense.user_id == current_user.id,
        models.Category.type == 'income'
    ).group_by(
        models.Category.id, models.Category.name
    ).order_by(
        func.sum(models.Expense.amount).desc()
    ).first()
    
    return {
        "total_income": float(total_income),
        "total_expenses": float(total_expenses),
        "net_balance": float(total_income - total_expenses),
        "top_expense_category": top_expense[0] if top_expense else None,
        "top_income_category": top_income[0] if top_income else None
    }

@router.get("/by-category", response_model=List[schemas.CategorySummary])
def get_category_breakdown(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Get spending/income breakdown by category
    """
    results = db.query(
        models.Category.id,
        models.Category.name,
        models.Category.type,
        func.sum(models.Expense.amount).label('total'),
        func.count(models.Expense.id).label('count')
    ).join(
        models.Expense
    ).filter(
        models.Expense.user_id == current_user.id
    ).group_by(
        models.Category.id,
        models.Category.name,
        models.Category.type
    ).order_by(
        func.sum(models.Expense.amount).desc()
    ).all()
    
    return [
        {
            "category_id": r[0],
            "category_name": r[1],
            "category_type": r[2],
            "total_amount": float(r[3]),
            "transaction_count": r[4]
        }
        for r in results
    ]

@router.get("/monthly", response_model=List[schemas.MonthlySummary])
def get_monthly_summary(
    months: int = Query(6, ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Get monthly income/expense summary
    months: number of recent months to include (default 6)
    """
    # Get all expenses with month grouping
    results = db.query(
        func.to_char(models.Expense.date, 'YYYY-MM').label('month'),
        models.Category.type,
        func.sum(models.Expense.amount).label('total')
    ).join(
        models.Category
    ).filter(
        models.Expense.user_id == current_user.id
    ).group_by(
    'month',
    models.Category.type
).order_by(
    func.to_char(models.Expense.date, 'YYYY-MM').desc() 
).limit(months * 2).all() # *2 because income and expense separate
    
    # Group by month
    monthly_data = {}
    for month, type_, total in results:
        if month not in monthly_data:
            monthly_data[month] = {"income": 0, "expenses": 0}
        if type_ == 'income':
            monthly_data[month]['income'] = float(total)
        else:
            monthly_data[month]['expenses'] = float(total)
    
    # Format response
    return [
        {
            "month": month,
            "total_income": data['income'],
            "total_expenses": data['expenses'],
            "net_balance": data['income'] - data['expenses']
        }
        for month, data in sorted(monthly_data.items(), reverse=True)
    ]