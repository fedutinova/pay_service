import pytest

from sqlalchemy import text
from app.models.payments_model import Payment
from app.repositories.payment_repo import payment_repo


@pytest.mark.asyncio
async def test_get_all_one(session):
    await session.execute(
        text("INSERT INTO companies (name, company_id) VALUES ('test', 1)")
    )
    await session.execute(
        text(
            "INSERT INTO payments (user_id, payment_id, amount, email, type, payment_status, company_id, created_at, updated_at) VALUES ('test', 'test', 100, 'test', 'test', 'PENDING', 1, '2022-01-01', '2022-01-01')"
        )
    )

    payments = await payment_repo.get_all(session=session)
    assert len(payments) == 1


@pytest.mark.asyncio
async def test_get_all_some(session):
    await session.execute(
        text("INSERT INTO companies (name, company_id) VALUES ('test', 1)")
    )
    await session.execute(
        text(
            "INSERT INTO payments (user_id, payment_id, amount, email, type, payment_status, company_id, created_at, updated_at) VALUES ('test', 'test', 100, 'test', 'test', 'PENDING', 1, '2022-01-01', '2022-01-01')"
        )
    )
    await session.execute(
        text(
            "INSERT INTO payments (user_id, payment_id, amount, email, type, payment_status, company_id, created_at, updated_at) VALUES ('test', 'test2', 100, 'test', 'test', 'PENDING', 1, '2022-01-01', '2022-01-01')"
        )
    )

    payments = await payment_repo.get_all(session=session)
    assert len(payments) == 2


@pytest.mark.asyncio
async def test_get_all_empty(session):
    payments = await payment_repo.get_all(session=session)
    assert len(payments) == 0


@pytest.mark.asyncio
async def test_get_payment_by_payment_id(session):
    await session.execute(
        text("INSERT INTO companies (name, company_id) VALUES ('test', 1)")
    )
    await session.execute(
        text(
            "INSERT INTO payments (user_id, payment_id, amount, email, type, payment_status, company_id, created_at, updated_at) VALUES ('test', 'test', 100, 'test', 'test', 'PENDING', 1, '2022-01-01', '2022-01-01')"
        )
    )

    payment = await payment_repo.get_payment_by_payment_id(
        payment_id="test", session=session
    )
    assert payment


@pytest.mark.asyncio
async def test_get_payment_by_payment_id_none(session):
    payment = await payment_repo.get_payment_by_payment_id(
        payment_id="test", session=session
    )
    assert not payment


@pytest.mark.asyncio
async def test_add_payment(session):
    await session.execute(
        text("INSERT INTO companies (name, company_id) VALUES ('test', 1)")
    )

    payment = Payment(
        user_id="test",
        payment_id="test",
        amount=100,
        email="test",
        type="test",
        payment_status="PENDING",
        company_id=1,
    )
    await payment_repo.add(payment=payment, session=session)
    assert True


@pytest.mark.asyncio
async def test_add_payment_exception(session):
    await session.execute(
        text("INSERT INTO companies (name, company_id) VALUES ('test', 1)")
    )
    await session.execute(
        text("INSERT INTO payments (user_id, payment_id, amount, email, type, payment_status, company_id, created_at, updated_at) VALUES ('test', 'test', 100, 'test', 'test', 'PENDING', 1, '2022-01-01', '2022-01-01')")
    )

    payment = Payment(
        user_id="test",
        payment_id="test",
        amount=100,
        email="test",
        type="test",
        payment_status="PENDING",
        company_id=1,
    )
    with pytest.raises(Exception):
        await payment_repo.add(payment=payment, session=session)


async def test_update_payment_status(session):
    await session.execute(
        text("INSERT INTO companies (name, company_id) VALUES ('test', 1)")
    )
    await session.execute(
        text("INSERT INTO payments (user_id, payment_id, amount, email, type, payment_status, company_id, created_at, updated_at) VALUES ('test', 'test', 100, 'test', 'test', 'PENDING', 1, '2022-01-01', '2022-01-01')")
    )

    await payment_repo.update_payment_status(
        payment_id="test", payment_status="COMPLETED", session=session
    )
