import fastapi
from app.schemas.user import Token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from datetime import timedelta
from app.services import authenticate_user, create_access_token
from app.database import get_db
from sqlalchemy.orm import Session


router = fastapi.APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES=30

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect username or password", 
                            headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}