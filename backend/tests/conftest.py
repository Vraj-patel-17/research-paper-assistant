import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

os.environ["ENV_FILE"] = ".env.test"

from dotenv import load_dotenv

load_dotenv(".env.test")

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("GEMINI_API_KEY", "test-gemini-key")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.paper import Paper
from app.core.security import hash_password
from app.core.rate_limiter import limiter

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Define it in .env.test or as an "
        "environment variable before running the tests."
    )

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def run_async(fn):
    """Run an async callable to completion on a fresh event loop.

    Runs in a worker thread so it never collides with any event loop
    pytest-asyncio may have set up on the main thread.
    """
    with ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(lambda: asyncio.run(fn())).result()


async def override_get_db():
    async with TestingSessionLocal() as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    async def create():
        async with engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            # Start from a clean schema in case a previous run crashed.
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def drop():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

    run_async(create)

    yield

    run_async(drop)


@pytest.fixture(autouse=True)
def clean_tables():
    """Empty every table after each test so tests stay independent."""

    async def truncate():
        tables = ", ".join(
            f'"{table.name}"' for table in Base.metadata.sorted_tables
        )
        async with engine.begin() as conn:
            await conn.execute(
                text(f"TRUNCATE TABLE {tables} RESTART IDENTITY CASCADE")
            )

    yield

    run_async(truncate)


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    limiter.enabled = False

    with TestClient(app) as test_client:
        yield test_client

    limiter.enabled = True
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user():
    async def create():
        async with TestingSessionLocal() as db:
            user = User(
                username="testuser",
                email="test@example.com",
                hashed_password=hash_password("password123"),
            )

            db.add(user)
            await db.commit()
            await db.refresh(user)

            return user

    return run_async(create)


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


@pytest.fixture()
def test_paper():
    async def create():
        async with TestingSessionLocal() as db:
            paper = Paper(
                title="Test Paper",
                abstract="Test Abstract",
                authors="John Doe",
                source="arXiv",
                external_id="test123",
                pdf_url="https://example.com/test.pdf",
            )

            db.add(paper)
            await db.commit()
            await db.refresh(paper)

            return paper

    return run_async(create)