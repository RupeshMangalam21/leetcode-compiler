from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import inspect 
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

def init_db():
    inspector = inspect(engine) 
    if not inspector.has_table("users"):  
        Base.metadata.create_all(bind=engine) 
        print("Database tables created successfully.")
    else:
        print("Users table already exists.")

if __name__ == "__main__":
    print("Starting database initialization...")
    init_db()
