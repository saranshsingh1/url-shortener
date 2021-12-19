"""
File contains tests for the general routes.
"""


def test_url_coder(test_api):
    """
    Tests for the ``/`` route in ``main.py``.
    Args:
        test_api: Client for making requests.
    """

    response = test_api.get("/")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.template.name == "landing_page.html"  # type: ignore
    assert "request" in response.context  # type: ignore
    assert "shorten_url_post_link" in response.context  # type: ignore
    assert "original_url_post_link" in response.context  # type: ignore


def test_failed_final_destination(test_api):
    """
    Tests for the ``final_destination`` route in ``main.py``
    where the ``short_code`` is not found in the database.
    Args:
        test_api: Client for making requests.
    """

    response = test_api.get("/dashke")

    html_content = """<html lang="en"><head><title>Unknown Page</title></head><body><h1>This page does not exist</h1></body></html>"""

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.content.decode() == html_content


def test_encode_api_final_destination(test_api):
    """
    Tests for the ``final_destination`` route in ``main.py``
    where the ``short_code`` value is ``encode``.
    Args:
        test_api: Client for making requests.
    """

    response = test_api.get("/encode")

    assert response.status_code == 405
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"detail": "Method Not Allowed"}


def test_decode_api_final_destination(test_api):
    """
    Test for the ``final_destination`` route in ``main.py``
    where the ``short_code`` value is ``decode``.
    Args:
        test_api: Client for making requests.
    """

    response = test_api.get("/decode")

    assert response.status_code == 405
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"detail": "Method Not Allowed"}
