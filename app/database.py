from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# CONSTANT
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLAlchemy Database URL
db_path = f"sqlite:///{BASE_DIR}/db.sqlite3"
SQLALCHEMY_DATABASE_URL = db_path

# Create database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmake to manage database sessions
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to get a database session
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
