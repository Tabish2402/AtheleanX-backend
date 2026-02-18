from datetime import datetime, timedelta, timezone
from typing import Any
import os
from jose import jwt, JWTError

# ------------------------------------------------------------------
# JWT configuration
# ----------------------------------------------------------------__

ALGORITHM = "HS256"

# NOTE:
# This MUST come from environment variables in production.
# We hardcode temporarily for local dev clarity.


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set")

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ------------------------------------------------------------------
# Token creation
# ------------------------------------------------------------------

def create_access_token(subject: str | int) -> str:
    """
    Creates a signed JWT access token.

    `subject` is the user identifier (usually user.id).
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload: dict[str, Any] = {
        "sub": str(subject),  # JWT spec expects string
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    encoded_jwt = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return encoded_jwt


# ------------------------------------------------------------------
# Token verification
# ------------------------------------------------------------------

def verify_access_token(token: str) -> dict[str, Any]:
    """
    Verifies and decodes a JWT access token.

    Returns the payload if valid.
    Raises JWTError if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload
    except JWTError:
        # We don't expose details — caller decides how to respond
        raise
