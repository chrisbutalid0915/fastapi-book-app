# from sqlalchemy import Column, Integer, Float, String, Boolean # import the class of SQLAlchemy that will define structure of data stored
# from .database import Base


# class Address(Base):
#     __tablename__ = "addresses"
#     id = Column(Integer, primary_key=True, index=True)
#     location = Column(String, index=True)
#     latitude = Column(Float)
#     longitude = Column(Float)


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True,index=True)
#     first_name = Column(String, index=True)
#     last_name = Column(String, index=True)
#     email_address = Column(String, unique=True,index=True)
#     hashed_password = Column(String)
#     disable = Column(Boolean, default=False)
