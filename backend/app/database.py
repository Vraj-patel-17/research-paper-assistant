from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
class Base(DeclarativeBase):
    pass
engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
try:
    with engine.connect() as conn:
        conn.execute(text("Select 1"))
        print("Databse connected successfullty!")

except Exception as e:
    print("Database connection failed!")
    print(e)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        