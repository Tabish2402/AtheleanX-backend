from passlib.context import CryptContext

# CryptContext is a wrapper that lets us:
# - choose hashing algorithm
# - upgrade algorithms later
# - keep verification logic centralized
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    """
    Takes a raw password and returns a secure Argon2 hash.
    Used ONLY during signup / password change.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a raw password against a stored hash.
    Used ONLY during login.
    """
    return pwd_context.verify(plain_password, hashed_password)
