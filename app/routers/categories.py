from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Create a new category for the current user
    
    Steps:
    1. Validate type is 'income' or 'expense'
    2. Create category with user_id = current_user.id
    3. Save to database
    4. Return created category
    """
    # Validate type
    if category.type not in ['income', 'expense']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type must be 'income' or 'expense'"
        )
    
    # Create category linked to current user
    new_category = models.Category(
        user_id=current_user.id,  # Links category to authenticated user
        name=category.name,
        type=category.type
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)  # Get id from database
    return new_category


@router.get("/", response_model=List[schemas.CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Get all categories for current user
    
    Security: Filter ensures user only sees their own categories
    """
    categories = db.query(models.Category).filter(
        models.Category.user_id == current_user.id  # CRITICAL: only user's categories
    ).all()
    return categories


@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Get specific category by ID
    
    Security: Checks both ID match AND user ownership
    """
    category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.user_id == current_user.id  # User can only access their own
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(
    category_id: int,
    category_update: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Update a category
    
    Steps:
    1. Find category (verify user owns it)
    2. Validate new type if provided
    3. Update fields that were provided
    4. Save changes
    """
    # Find category and verify ownership
    category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Validate type if being updated
    if category_update.type and category_update.type not in ['income', 'expense']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type must be 'income' or 'expense'"
        )
    
    # Update only provided fields
    if category_update.name:
        category.name = category_update.name
    if category_update.type:
        category.type = category_update.type
    
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Delete a category
    
    Note: Due to CASCADE in models, all expenses in this category
    will also be deleted automatically
    """
    category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    db.delete(category)
    db.commit()
    return None  # 204 No Content means success with no body
