from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email_address: str
    disable: bool or False = False


class UserInDB(UserBase):
    hashed_password: str