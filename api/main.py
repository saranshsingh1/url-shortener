"""
File contains all the API and HTML page related code.
"""

from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.datastructures import URL

from api.schema import DBShortLink, DBMainLink, URLSchema
from api.helper import db, get_long_url_code, get_url_id


# Instantiate an instance of FastAPI.
app = FastAPI()

# Create the object that can be re-used later by
# multiple routes.
templates = Jinja2Templates(directory="templates")


@app.post("/encode", response_model=DBShortLink, status_code=201)
async def shorten_url(user_link: URLSchema, request: Request):
    """
    API route that handles returning the shortened
    version of the link provided by ``user_link``.
    Args:
        user_link (URLSchema): The URL provided by the user.
        request (Request): Data sent from the client side.
    Returns:
        JSONResponse: Shortened version of the original URL.
    """

    long_url: str = user_link.url

    # TODO: Validate the long_url to be valid URL.

    # Representation -> base_url = http://127.0.0.1:8000/
    base_url: URL = request.base_url

    # Get the unique value, save it to the hash
    # with the long URL as the value and the
    # unique value as the key.
    unique_id: str = get_url_id()
    db[unique_id] = long_url

    return {"shortened_url": f"{str(base_url)}{unique_id}"}


@app.post("/decode", response_model=DBMainLink)
async def original_url(user_link: URLSchema, request: Request):
    """
    API route that handles returning the original
    version of the short link provided by ``user_link``.
    Args:
        user_link (URLSchema): The short URL provided by the user.
        request (Request): Data sent from the client side.
    Returns:
        JSONResponse: Original version of the shortened URL.
    """

    short_url: str = user_link.url

    try:
        url_code: str = get_long_url_code(
            base_url=str(request.base_url), short_url=short_url
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400, detail="Invalid Short URL sent."
        ) from error

    long_url: Optional[str] = db.get(url_code)

    if long_url is None:
        raise HTTPException(status_code=404, detail="Could not find the URL.")

    return {"longer_url": long_url}


@app.get("/", response_class=HTMLResponse)
async def url_coder(request: Request):
    """
    This route provides the page where a user can input
    his desired URL and request a shorter version of
    the URL or request the original URL back from the
    shorter version.
    Args:
        request (Request): Data sent from the client side.
            Example - a browser sending data to the backend.
    Returns:
        TemplateResponse: Rendering the HTML page as provided
            by the 'name' parameter of TemplateResponse.
    """

    # Send the URL that will be used by the `fetch` call
    # of the JS language.
    shorten_url_post_link = request.url_for("shorten_url")
    original_url_post_link = request.url_for("original_url")

    return templates.TemplateResponse(
        name="landing_page.html",
        context={
            "request": request,
            "shorten_url_post_link": shorten_url_post_link,
            "original_url_post_link": original_url_post_link,
        },
    )


@app.get("/{short_code}")
async def final_destination(short_code: str):
    """
    This route redirects the user the main link for which
    there was a short link generated.
    - This route only works when a valid ``short_code``
      is found.
    - Otherwise, it renders a generic HTML page stating
      that the page was not found.
    Args:
        short_code (str): The unique id that refers to the
            original link stored in the database.
    Returns:
        RedirectResponse: Redirects the user to the main link
            if it is found else renders an HTML template.
    """

    # Send the same response as FastAPI if a GET request
    # is made to the `/encode` and `/decode` endpoints.
    if short_code in {"encode", "decode"}:
        raise HTTPException(status_code=405, detail="Method Not Allowed")

    # Get the original link from the database.
    original_link = db.get(short_code)

    # Display a generic message if the link is
    # not found anymore.
    if original_link is None:
        html_content = """<html lang="en"><head><title>Unknown Page</title></head><body><h1>This page does not exist</h1></body></html>"""
        return HTMLResponse(content=html_content, status_code=404)

    # Redirect the user to the main page.
    return RedirectResponse(original_link)
