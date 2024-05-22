from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email_address: str
    disable: Optional[bool] = False


class UserInDB(UserBase):
    hashed_password: str
