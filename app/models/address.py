from sqlalchemy import Column, Integer, Float, String, Boolean # import the class of SQLAlchemy that will define structure of data stored
from ..database import engine
from sqlalchemy.ext.declarative import declarative_base  # process of definining SQLAlchemy models


Base = declarative_base()


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    disable = Column(Boolean)


Base.metadata.create_all(bind=engine) # create the database tables on the defined models