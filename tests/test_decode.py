"""
File contains all tests related to the '/decode' endpoint API.
"""

from api.helper import db


def test_get_original_url(test_api):
    """
    Test to make GET request to the '/decode'
    endpoint when only POST requests are
    allowed.
    Args:
        test_api: Client for making requests.
    """

    response = test_api.get("/decode")

    # Should not be able to make a GET request.
    assert response.status_code == 405
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"detail": "Method Not Allowed"}


def test_post_incorrect_base_url(test_api):
    """
    Test to make a POST request to the '/decode'
    API endpoint using the wrong domain address.
    Args:
        test_api: Client for making requests.
    """

    # web address does not match base_url: http://127.0.0.1:8000
    request_payload = {"url": "http://webserver/sfhjkwe"}

    response = test_api.post(url="/decode", json=request_payload)

    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"detail": "Invalid Short URL sent."}


def test_post_missing_short_url(test_api):
    """
    Test to make a POST request to the '/decode'
    API endpoint when the unique code is missing
    from the database.
    Args:
        test_api: Client for making requests.
    """

    # The code 'sfhjkwe' is not present in the database.
    request_payload = {"url": "http://127.0.0.1:8000/sfhjkwe"}

    response = test_api.post(url="/decode", json=request_payload)

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"detail": "Could not find the URL."}


def test_post_valid_short_url(test_api, monkeypatch):
    """
    Test to make a POST request to the '/decode'
    API endpoint when the unique code is missing
    from the database.
    - Monkey patch dictionary
      - https://docs.pytest.org/en/latest/how-to/monkeypatch.html#monkeypatching-dictionaries
    Args:
        test_api: Client for making requests.
    """

    request_payload = {"url": "http://127.0.0.1:8000/sfhjkwe"}

    # patch the dictionary for test purposes only.
    monkeypatch.setitem(db, "sfhjkwe", "https://www.example.com")

    response = test_api.post(url="/decode", json=request_payload)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"longer_url": "https://www.example.com"}


def test_invalid_post_original_url(test_api):
    """
    Test to make an invalid POST request to the
    '/decode' API endpoint.
    Args:
        test_api: Client for making requests.
    """

    request_payload = {"something_else": "https://www.google.com"}
    response_payload = {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

    response = test_api.post(url="/decode", json=request_payload)

    assert response.status_code == 422
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == response_payload
