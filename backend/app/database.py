from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from app.core.config import settings
DATABASE_URL=settings.database_url
class Base(DeclarativeBase):
    pass
engine=create_async_engine(DATABASE_URL)
SessionLocal=async_sessionmaker(autoflush=False,autocommit=False,bind=engine,expire_on_commit=False)
async def check_db_connection():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            print("Database connected successfully!")
    except Exception as e:
        print("Database connection failed!")
        print(e)


async def get_db():
    async with SessionLocal() as db:
        yield db
        