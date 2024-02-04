from passlib.context import CryptContext
import schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_pasword: str):
    return pwd_context.verify(plain_password, hashed_pasword)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def authenticate_user(user: schemas.User, username: str, password: str):
    if user is None:
        return False
    if not verify_password(password, user.password):
        return False
    return user

