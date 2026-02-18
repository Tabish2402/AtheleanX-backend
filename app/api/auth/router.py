from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.api.auth.schemas import SignupRequest, SignupResponse
from app.api.auth.service import create_user
from app.db.database import get_db
from app.api.auth.schemas import LoginRequest, TokenResponse
from app.api.auth.service import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    try:
        user = create_user(
            db=db,
            email=payload.email,
            password=payload.password,
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    



@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    try:
        token = authenticate_user(
            db=db,
            email=payload.email,
            password=payload.password,
        )
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.models.user import User






