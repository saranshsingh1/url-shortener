"""
File contains schemas used for various routes.
"""

from pydantic import BaseModel


# Create a dataclass like class for validation
# and attribute access in various routes.
class URLSchema(BaseModel):
    """
    Class that provides validation and attribute access
    to the URL provided by the user.
    """

    url: str


class DBShortLink(BaseModel):
    """
    Class that returns the short URL requested
    by the user.
    """

    shortened_url: str


class DBMainLink(BaseModel):
    """
    Class that returns the original URL requested
    by the user.
    """

    longer_url: str
