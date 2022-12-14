import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .yield_db import get_db
from .crud import *
from jose import JWTError, jwt
from . import schema
from environs import Env

env = Env()

env.read_env()
SECRET_KEY = env.str("SECRET_KEY")
ALGO = env.str("ALGO")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def token_response(token: str):
    return {"access_token": token}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def create_access_token(data: dict, expire_time: timedelta | None = None):
    to_encode = data.copy()
    if expire_time:
        expire = datetime.utcnow() + expire_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
    return token


def auth_user(db: Session, username: str, password: str):
    """
    Return user in sql format
    """
    user = return_user(db, username)
    if not user:
        return False
    if not verify_password(password + user.salt, user.hashed_password):
        return False
    return user


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)

    except JWTError:
        raise credentials_exception
    user = return_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: schema.UserInDb = Depends(get_current_user),
):
    return current_user
