from fastapi.testclient import TestClient
from unittest import mock
import pytest

@mock.patch("app.repositories.company_repo.CompanyRepo.add")
@pytest.mark.asyncio
async def test_create_company(add_mock, client: TestClient, session):
    add_mock.return_value = None
    company_data = {
        "company_id": 1,
        "name": "Test Company",
    }
    response = client.post("/companies", json=company_data)
    assert response.status_code == 201
