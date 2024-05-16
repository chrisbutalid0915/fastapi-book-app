from sqlalchemy.ext.declarative import declarative_base # process of definining SQLAlchemy models

# from app import engine
from sqlalchemy import Column, Integer, Float, String # import the class of SQLAlchemy that will define structure of data stored

# create a base from declarative class definitions
Base = declarative_base()


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)