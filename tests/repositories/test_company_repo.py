import pytest

from sqlalchemy import text
from app.repositories.company_repo import company_repo
from app.models.companies_model import Company


@pytest.mark.asyncio
async def test_add_success(session):
    company = Company(name="test", company_id=1)
    await company_repo.add(company=company, session=session)


@pytest.mark.asyncio
async def test_add_duplicate(session):
    await session.execute(
        text("INSERT INTO companies (name, company_id) VALUES ('test', 1)")
    )
    company = Company(name="test", company_id=1)
    with pytest.raises(Exception):
        await company_repo.add(company=company, session=session)


@pytest.mark.asyncio
async def test_get_all(session):
    await session.execute(
        text("INSERT INTO companies (name, company_id) VALUES ('test', 1)")
    )
    companies = await company_repo.get_all(session=session)
    assert len(companies) == 1


@pytest.mark.asyncio
async def test_get_all_empty(session):
    companies = await company_repo.get_all(session=session)
    assert len(companies) == 0
