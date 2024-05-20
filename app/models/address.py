from sqlalchemy import Column, Integer, Float, String # import the class of SQLAlchemy that will define structure of data stored
from ..database import Base, engine


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)


Base.metadata.create_all(bind=engine) # create the database tables on the defined models