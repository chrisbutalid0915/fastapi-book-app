from fastapi import FastAPI
from app.routers import api_book


def create_app():
    """Construct the core application"""
    app = FastAPI()
    app.include_router(api_book.router)

    return app
