"""
File contains all tests related to the helper functions.
"""

import pytest
from api.helper import get_long_url_code, get_url_id


def test_get_url_id():
    """
    Test to check that the ``get_url_id`` function
    returns a unique id not found in the database.
    """

    # Fake a database with the url code and the long urls.
    test_db = {
        "sdhfkjkwe": "https://www.google.com",
        "948rhfkwe": "https://www.yahoo.com",
    }

    assert get_url_id() not in test_db


def test_get_long_url_code():
    """
    Test to check if the ``get_long_url_code`` function
    returns the correct value of the url code if the
    correct base URL is provided.
    """

    # NOTE: base url always has a trailing slash.
    test_base_url = "http://test-webserver.com/"
    test_short_url_id = "948rh"

    test_short_url = f"{test_base_url}{test_short_url_id}"

    assert test_short_url_id == get_long_url_code(
        base_url=test_base_url, short_url=test_short_url
    )


def test_invalid_get_long_url_code():
    """
    Test to ensure that the ``get_long_url_code`` function
    throws a ``ValueError`` exception if an invalid
    ``short_url`` is sent.
    """

    test_base_url = "http://test-webserver.com/"
    test_short_url = "https://zerver.com/948rh"

    # Reference -
    # - https://docs.pytest.org/en/stable/reference.html?highlight=raises#pytest.raises
    with pytest.raises(ValueError):
        get_long_url_code(base_url=test_base_url, short_url=test_short_url)
