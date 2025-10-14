from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app import models, schemas, auth

# Create router with prefix and tag
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account
    
    Steps:
    1. Check if email already exists
    2. Hash the password
    3. Create new user in database
    4. Return user data (without password)
    """
    # Check if user with this email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password (NEVER store plain passwords!)
    hashed_password = auth.get_password_hash(user.password)
    
    # Create new user object
    new_user = models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )
    
    # Add to database and commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Get the new user's ID
    
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login and receive access token
    
    Steps:
    1. Find user by email
    2. Verify password
    3. Create JWT access token
    4. Return token
    
    Note: OAuth2PasswordRequestForm expects:
    - username field (we use email as username)
    - password field
    """
    # Find user by email (OAuth2 calls it username)
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # Verify user exists and password is correct
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},  # "sub" is standard JWT claim for subject
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    """
    Get current user's information
    
    This is a protected endpoint - requires valid JWT token
    The token is automatically extracted and validated by the dependency
    
    Try it:
    1. Register a user
    2. Login to get token
    3. Click "Authorize" button and paste token
    4. Call this endpoint
    """
    return current_user
