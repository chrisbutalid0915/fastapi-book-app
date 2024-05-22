import logging

import fastapi
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.models import OpenAPI
from fastapi.responses import HTMLResponse

router = fastapi.APIRouter()  # create a new router instance


@router.get("/openapi.json")
async def get_open_api_endpoint():
    """
    Returns the OPENAPI schema in JSON Format
    """
    logging.info("GET /openapi.json")
    return HTMLResponse(OpenAPI().dict())


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    Serves a customized Swagger UI HTML page
    """
    logging.info("GET /docs")
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Swagger UI")


@router.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serves the root URL ("/") with a custom HTML response
    """
    logging.info("GET /")
    return """
    <html>
        <head>
            <title>Custom Swagger UI</title>
        </head>
        <body>
            <h1>Custom Swagger UI</h1>
            <p>Find the API documentation <a href="/api/v1/docs">here</a>.</p>
        </body>
    </html>
    """
