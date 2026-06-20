from fastapi import FastAPI
from .database import engine
from . import models
from .routes import api_router
import os

app = FastAPI(title="Inventory & Order Management API")

app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    # create tables if they don't exist - in production use migrations instead
    models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Inventory & Order Management API"}
