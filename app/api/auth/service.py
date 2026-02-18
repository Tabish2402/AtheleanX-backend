from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.jwt import create_access_token


def create_user(db: Session, email: str, password: str) -> User:
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise ValueError("Email already registered")

    # Hash the password
    hashed_pw = hash_password(password)

    # Create user instance
    user = User(
        email=email,
        hashed_password=hashed_pw,
    )

    # Persist to DB
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

from app.core.security import verify_password
from app.core.jwt import create_access_token


def authenticate_user(db: Session, email: str, password: str) -> str:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")

    # Create JWT using user.id as subject
    token = create_access_token(subject=user.id)
    return token

