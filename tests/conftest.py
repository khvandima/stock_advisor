import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.db.models import Base
from app.db.session import get_db
from app.config import settings


@pytest.fixture(scope="function")
async def prepare_database():
    engine_test = create_async_engine(settings.TEST_DATABASE_URL)
    session_factory = async_sessionmaker(engine_test, expire_on_commit=False)

    async def override_get_db():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine_test.dispose()
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def client(prepare_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac