from fastapi import FastAPI
# from app.routers import api_book
from app.api.endpoint import swagger, address, token, user
from app import models
from .database import Base, engine

Base.metadata.create_all(bind=engine) 

# Address()
# User()
def create_app():
    """Construct the core application"""
    app = FastAPI(
        docs_url="/api/v1/docs",
    )
    app.include_router(swagger.router, prefix="/api/v1", tags=["Swagger"])
    app.include_router(token.router, prefix="/api/v1", tags=["Token"])
    app.include_router(address.router, prefix="/api/v1", tags=["Address"])
    app.include_router(user.router, prefix="/api/v1", tags=["User"])

    return app
