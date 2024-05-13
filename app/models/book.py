from sqlalchemy.ext.declarative import declarative_base

# from app import engine
from sqlalchemy import Column, Integer, Float, String
from pydantic import BaseModel # It a way to define data model with validation and serialization 

# create a base from declarative class definitions
Base = declarative_base()


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)


# Base.metadata.create_all(bind=engine) # create the database tables on the defined models


class AddressBase(BaseModel):
    location: str
    latitude: float
    longitude: float


class AddressID(BaseModel):
    id: int


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class GetAddress(AddressBase,AddressID):
    pass


class DeleteAddress(AddressBase, AddressID):
    pass


class DistanceRequest(BaseModel):
    distance: float
    latitude: float
    longitude: float

    # class Config:
    #     orm_mode = True
