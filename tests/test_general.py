"""
File contains tests for the general routes.
"""


def test_home(test_api):
    """
    Tests for the ``home`` route in ``main.py``.
    Args:
        test_api: Client for making requests.
    """

    response = test_api.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello Finn"}


def test_url_coder(test_api):
    """
    Tests for the ``url_coder`` route in ``main.py``.
    Args:
        test_api: Client for making requests.
    """

    response = test_api.get("/url-coder")

    assert response.status_code == 200
    assert response.template.name == "landing_page.html"  # type: ignore
    assert "request" in response.context  # type: ignore
