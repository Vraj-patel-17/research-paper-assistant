import os

os.environ["ENV_FILE"] = ".env.test"

from dotenv import load_dotenv

load_dotenv(".env.test")
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import sys
print("PYTHON PATH:", sys.path)
import app
print("APP:", app.__file__)
print("APP PATH:", app.__path__)
from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.paper import Paper
from app.core.security import hash_password
from app.core.rate_limiter import limiter
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)

TestingSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


async def override_get_db():
    async with TestingSessionLocal() as db:
        yield db


app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture()
async def db_session():
    async with engine.connect() as connection:
        transaction = await connection.begin()

        session_factory = async_sessionmaker(
            bind=connection,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

        async with session_factory() as db:
            yield db

        await transaction.rollback()

@pytest.fixture()
def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    limiter.enabled = False

    with TestClient(app) as client:
        yield client
    limiter.enabled = True
    app.dependency_overrides.clear()

@pytest_asyncio.fixture()
async def test_user(db_session):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user

@pytest.fixture()
def auth_headers(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest_asyncio.fixture()
async def test_paper(db_session):
    paper = Paper(
        title="Test Paper",
        abstract="Test Abstract",
        authors="John Doe",
        source="arXiv",
        external_id="test123",
        pdf_url="https://example.com/test.pdf",
    )

    db_session.add(paper)
    await db_session.commit()
    await db_session.refresh(paper)

    return paper