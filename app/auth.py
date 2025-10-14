from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

# ===== Security Configuration =====

# Secret key for JWT - CHANGE THIS in production!
SECRET_KEY = "your-secret-key-change-this-in-production-use-openssl-rand-hex-32"
ALGORITHM = "HS256"  # Hashing algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tokens expire after 30 minutes

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme - tells FastAPI where to look for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ===== Password Functions =====

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    Returns True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password for secure storage
    Same password will produce same hash
    """
    return pwd_context.hash(password)


# ===== JWT Token Functions =====

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token
    
    Args:
        data: Dictionary to encode in token (usually {"sub": email})
        expires_delta: How long until token expires
    
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    # Encode the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ===== Get Current User Function =====

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Dependency function to get current authenticated user
    
    This function:
    1. Extracts token from Authorization header
    2. Decodes and validates the token
    3. Looks up user in database
    4. Returns user object or raises 401 error
    
    Use as dependency in protected endpoints:
    @app.get("/protected")
    def protected_route(current_user: User = Depends(get_current_user)):
        ...
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # "sub" is standard claim for subject
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Look up user in database
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if user is None:
        raise credentials_exception
        
    return user
