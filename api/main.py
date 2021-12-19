"""
File contains all the API and HTML page related code.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.schema import DBShortLink, DBMainLink, URLSchema

# Instantiate an instance of FastAPI.
app = FastAPI()

# Create the object that can be re-used later by
# multiple routes.
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home():
    """
    Test endpoint.
    Returns:
        JSONResponse: `Hello World`
    """

    return {"message": "Hello World"}


@app.post("/encode", response_model=DBShortLink, status_code=201)
async def shorten_url(user_link: URLSchema):
    """
    API route that handles returning the shortened
    version of the link provided by ``user_link``.
    Args:
        user_link (URLSchema): The URL provided by the user.
    Returns:
        JSONResponse: Shortened version of the original URL.
    """

    return {"shortened_url": user_link.url}


@app.post("/decode", response_model=DBMainLink)
async def original_url(user_link: URLSchema):
    """
    API route that handles returning the original
    version of the short link provided by ``user_link``.
    Args:
        user_link (URLSchema): The short URL provided by the user.
    Returns:
        JSONResponse: Original version of the shortened URL.
    """

    return {"longer_url": user_link.url}


@app.get("/url-coder", response_class=HTMLResponse)
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

    return templates.TemplateResponse(
        name="landing_page.html", context={"request": request}
    )
