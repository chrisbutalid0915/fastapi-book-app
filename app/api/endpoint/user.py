import logging
import os

import fastapi
from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserBase, UserInDB
from app.services import get_current_active_user, get_password_hash

router = fastapi.APIRouter()


# Create a folder for logs if it doesn't exist
log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)


# Configure logging settings
log_file_path = os.path.join(log_folder, "app.log")
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define log message format
    filename=log_file_path,  # Specify the log file
    filemode="a",  # Append mode for the log file
)


@router.post("/users/", response_model=UserBase)
async def create_user(user: UserInDB, db: Session = Depends(get_db)):
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
