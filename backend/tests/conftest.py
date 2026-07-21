import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.dependencies.database import get_db
from app.main import app

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest_asyncio.fixture
async def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
@pytest_asyncio.fixture
async def authenticated_client(client):
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "testanalyst@example.com",
            "password": "SecurePassword123!",
            "full_name": "Test SOC Analyst",
        },
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "testanalyst@example.com",
            "password": "SecurePassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    client.headers.update(
        {
            "Authorization": f"Bearer {token}",
        }
    )

    return client