"""
File contains all tests related to the '/encode' endpoint API.
"""

import secrets


def test_get_shorten_url(test_api):
    """
    Test to make GET request to the '/encode'
    endpoint when only POST requests are
    allowed.
    Args:
        test_api: Client for making requests.
    """

    response = test_api.get("/encode")

    # Should not be able to make a GET request.
    assert response.status_code == 405
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"detail": "Method Not Allowed"}


def test_post_shorten_url(test_api, monkeypatch):
    """
    Test to make a valid POST request to the
    '/encode' API endpoint.
    Args:
        test_api: Client for making requests.
        monkeypatch: Monkey patch fixture of pytest.
    """

    request_payload = {"url": "https://www.google.com"}

    # mock the `token_urlsafe` method of secrets module
    # to return the token we want.
    def mock_token_urlsafe(nbytes):
        return "jflew9"

    # hijack the method with out mocked method
    monkeypatch.setattr(secrets, "token_urlsafe", mock_token_urlsafe)

    response = test_api.post(url="/encode", json=request_payload)

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert "shortened_url" in response.json()
    assert "http://127.0.0.1:8000/" in response.json()["shortened_url"]
    assert response.json() == {"shortened_url": "http://127.0.0.1:8000/jflew9"}


def test_invalid_post_shorten_url(test_api):
    """
    Test to make an invalid POST request to the
    '/encode' API endpoint.
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

    response = test_api.post(url="/encode", json=request_payload)

    assert response.status_code == 422
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == response_payload
