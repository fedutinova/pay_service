import pytest_asyncio

from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config


from app.db import Base


@pytest_asyncio.fixture(scope="session")
async def db():
    postgres = PostgresContainer("postgres:16-alpine", driver="asyncpg")
    postgres.start()
    yield postgres
    postgres.stop()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database(db: PostgresContainer):
    engine = create_async_engine(db.get_connection_url(), echo=True)
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db.get_connection_url())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(db):
    engine = create_async_engine(db.get_connection_url(), echo=True)
    session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        yield session
