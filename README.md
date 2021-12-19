## URL Shortener

### Objective

Implement a URL shortening service using Python and any framework.

### Brief

ShortLink is a URL shortening service where you enter a URL such as https://github.com/psf/requests, and it returns a short URL such as http://short.est/AbCdE.

### Tasks

-   Implementation details:
    -   Language: **Python**
    -   Framework: **FastAPI**
    -   Two endpoints are implemented:
        -   /encode - Encodes a URL to a shortened URL
        -   /decode - Decodes a shortened URL to its original URL.
    -   Both endpoints return JSON

### Details

- This application is written using [FastAPI framework](https://fastapi.tiangolo.com/) and run using [uvicorn](https://www.uvicorn.org/) ASGI server.
- Formatting, linting is done using [black](https://github.com/psf/black), [pylint](https://github.com/PyCQA/pylint), and [mypy](https://github.com/python/mypy).
- Testing is done [pytest](https://docs.pytest.org/en/6.2.x/) with the help of [requests](https://github.com/psf/requests).

**DISCLAIMER** - The page is not pretty but gets the job done.

### Setup instructions to run the application

- Clone the repository using the `git clone https://github.com/saranshsingh1/url-shortener.git` command.
- `cd` into `url-shortener` directory.
- Launch a virtual environment using the command `python3 -m venv venv`.
- Activate the virtual environment using `source venv/bin/activate`.
- Install the dependencies using `pip install -r requirements.txt`.

### Run the application

- Launch the `uvicorn` server using `uvicorn api.main:app --reload`.
- Go to a web browser and open `http://127.0.0.1:8000`.
- A page is rendered with the option to get a shortened URL or the original URL back (if it exists).
- As long as the `uvicorn` server is running, the URLs persist in memory. Once the server is shut down, all the data is lost.

### Run the tests

- Run `pytest` from the `url-shortener` directory.
- All the tests pass.
