"""
File contains the fixture used by all the other test modules
by initializing the test functions.
Use a scope of "module" to re-use the same connection
across all the test functions.
References -
- https://docs.pytest.org/en/6.2.x/fixture.html
- https://docs.pytest.org/en/6.2.x/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session
"""

import pytest

from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture(scope="session")
def test_api():
    """
    Provides the test client for running
    pytest.
    """

    client = TestClient(app)

    yield client  # use this client everytime
