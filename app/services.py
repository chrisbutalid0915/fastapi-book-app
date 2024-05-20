
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Query, Depends, HTTPException, status
from app.database import get_db

from app.schemas.user import UserInDB, TokenData
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import logging


SECRET_KEY="c2426d96adfa1412615c13381b982d7d8ee91668a87136c42e1583dcd001d681" # run `rand hex 32` to generate Random Hex Number
ALGORITHM ="HS256" # encryption algorithm



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    from app.models.user import User
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        # Return Exception 404 when no address found
        logging.error(f"User not found")
        raise ValueError("User not found")
    return user
    

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials", 
                                         headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    user = get_user(db, username=token_data.username)
    if user is None:
        return credential_exception
    
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disable:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user