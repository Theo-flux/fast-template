from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from src.db.base import get_session
from src.main import app

mock_session: Mock = Mock()
mock_auth_service: Mock = Mock()
mock_user_service: Mock = Mock()


def mock_get_session():
    yield mock_session


app.dependency_overrides[get_session] = mock_get_session


@pytest.fixture
def fake_session():
    return mock_session


@pytest.fixture
def fake_auth_service():
    return mock_auth_service()


@pytest.fixture
def fake_user_service():
    return mock_user_service()


@pytest.fixture
def test_client():
    return TestClient(app)
