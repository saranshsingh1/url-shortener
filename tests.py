"""
File contains all the test suites for the main.py file.
"""

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_home():
    """
    Tests for the ``home`` route in ``main.py``.
    """

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello Finn"}


def test_url_coder():
    """
    Tests for the ``url_coder`` route in ``main.py``.
    """

    response = client.get("/url-coder")

    assert response.status_code == 200
    assert response.template.name == "landing_page.html"  # type: ignore
    assert "request" in response.context  # type: ignore
