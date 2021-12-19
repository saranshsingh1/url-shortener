"""
File contains all tests related to the '/decode' endpoint API.
"""


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
    assert response.json() == {"detail": "Method Not Allowed"}


def test_post_original_url(test_api):
    """
    Test to make a valid POST request to the
    '/decode' API endpoint.
    Args:
        test_api: Client for making requests.
    """

    request_payload = {"url": "https://www.google.com"}
    response_payload = {"longer_url": request_payload["url"]}

    response = test_api.post(url="/decode", json=request_payload)

    assert response.status_code == 200
    assert response.json() == response_payload


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
    assert response.json() == response_payload
