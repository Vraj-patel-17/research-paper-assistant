from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import hash_password,verify_password

async def create_user(db: AsyncSession, username, email, password):
    user = User(username=username, email=email, hashed_password=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_email(db: AsyncSession, email):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def update_username(db: AsyncSession, email, new_username):
    user = await get_user_by_email(db, email)
    if user:
        user.username = new_username
        await db.commit()
        await db.refresh(user)
        return user

async def delete_user(db: AsyncSession, email):
    user = await get_user_by_email(db, email)
    if user:
        await db.delete(user)
        await db.commit()
    return user

async def authenticate_user(db: AsyncSession, email, password):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user