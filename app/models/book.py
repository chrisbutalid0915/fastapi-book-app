from sqlalchemy.ext.declarative import declarative_base # process of definining SQLAlchemy models

# from app import engine
from sqlalchemy import Column, Integer, Float, String # import the class of SQLAlchemy that will define structure of data stored
from pydantic import confloat, field_validator, BaseModel # It a way to define data model with validating the incoming request

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
    @field_validator('latitude')
    def validate_latitude(cls, lat):
         if -90 < lat <= 90:
            return lat
         else:
            raise ValueError('Latitude must be between -90 and 90 degrees')
         
    @field_validator('longitude')
    def validate_longitude(cls, long):
         if -180 < long <= 180:
            return long
         else:
             raise ValueError('Longitude must be between -180 and 180 degrees')


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


