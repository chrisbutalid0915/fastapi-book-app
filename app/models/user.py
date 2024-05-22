from sqlalchemy import (  # import the class of SQLAlchemy that will define structure of data stored
    Boolean, Column, Integer, String)
from sqlalchemy.ext.declarative import \
    declarative_base  # process of definining SQLAlchemy models

from ..database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email_address = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disable = Column(Boolean, default=False)


Base.metadata.create_all(
    bind=engine
)  # create the database tables on the defined models
