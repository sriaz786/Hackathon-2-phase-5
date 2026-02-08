from jose import jwt
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.api import deps
from app.core import security
from app.core.config import settings
from app.db.session import get_session
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserRead, UserLogin

router = APIRouter()

@router.post("/signup", response_model=UserRead)
def create_user(
    *,
    session: Session = Depends(get_session),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    if user_in.password != user_in.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match",
        )

    user = session.exec(
        select(User).where((User.email == user_in.email) | (User.username == user_in.username))
    ).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already exists",
        )
    
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=security.get_password_hash(user_in.password),
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login_access_token(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = session.exec(
        select(User).where(User.email == form_data.username)
    ).first()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_token: str,
    session: Session = Depends(get_session),
) -> Any:
    """
    Refresh access token
    """
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "refresh":
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_id = payload.get("sub")
        if user_id is None:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token subject",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
        
    user = session.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(user.id), # Rotate refresh token? Plan says long lived, but better to rotate or keep same? I'll just return new one for now.
        "token_type": "bearer",
    }
