from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Instantiate an instance of FastAPI.
app = FastAPI()


@app.get("/")
async def home():
    """
    Test endpoint.
    Returns:
        JSONResponse: `Hello World`
    """

    return {"message": "Hello World"}

