from schemas import Account
from starlette.requests import Request
from strawberry.types import Info
from database import db_session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Any
from strawberry.permission import BasePermission
from fastapi.security import  OAuth2PasswordBearer
from jose import jwt, JWTError
import models

db = db_session.session_factory()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY = "Klutj3f123jkl31JF2901j019284"
ALGORITHM = "HS256"

async def current_user(info: Info) -> Account:
        request: Request = info.context["request"] 
        token = request.headers['Authorization'].split(' ')[1]
        user: Account = db.query(models.AccountTable).where(models.AccountTable.token == token).first()
        return user

async def get_current_user(info: Info) -> Account:
    request: Request = info.context["request"]
    token = request.headers['Authorization'].split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user: Account = db.query(models.AccountTable).where(models.AccountTable.token == token).first()
        return user 
    except JWTError:
        raise Exception("Not authorized")

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def authenticate_user(email: str, password: str):
    user = db.query(models.AccountTable).filter(models.AccountTable.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hash_password):
        return False
    return user

def create_access_token(email: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"email": email, "user_id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    db.commit()
    return token

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request: Request = info.context["request"]

        if "authorization" in request.headers:
            # print(request.headers['Authorization']) 
            return True
            # return authenticate_header(request)

        return False