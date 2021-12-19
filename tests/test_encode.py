"""
File contains all tests related to the '/encode' endpoint API.
"""


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
    assert response.json() == {"detail": "Method Not Allowed"}


def test_post_shorten_url(test_api):
    """
    Test to make a valid POST request to the
    '/encode' API endpoint.
    Args:
        test_api: Client for making requests.
    """

    request_payload = {"url": "https://www.google.com"}
    response_payload = {"shortened_url": request_payload["url"]}

    response = test_api.post(url="/encode", json=request_payload)

    assert response.status_code == 201
    assert response.json() == response_payload


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
    assert response.json() == response_payload
