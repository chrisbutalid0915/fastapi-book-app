from sqlalchemy import (  # import the class of SQLAlchemy that will define structure of data stored
    Boolean, Column, Float, Integer, String)
from sqlalchemy.ext.declarative import \
    declarative_base  # process of definining SQLAlchemy models

from ..database import engine

Base = declarative_base()


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)


Base.metadata.create_all(
    bind=engine
)  # create the database tables on the defined models
