import fastapi
import logging
from fastapi import Depends
from app.schemas.user import UserBase, UserInDB
from fastapi import Query, Depends, HTTPException, status
from app.services import get_current_active_user
from sqlalchemy.orm import Session
from app.database import get_db

from app.services import get_password_hash


router = fastapi.APIRouter()


@router.post("/users/", response_model=UserBase)
async def create_user(user: UserInDB, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_active_user)):
    from app.models.user import User
    try:
        hashed_password = get_password_hash(user.hashed_password)
        user.hashed_password = hashed_password
        user = User(**dict(user))
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        logging.error(f"Error occurred: {e}")


@router.get("/users/me", response_model=UserBase)
async def read_user(current_user: UserBase = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items")
async def read_own_items(current_user: UserBase = Depends(get_current_active_user)):
    return [{"owner": current_user}]