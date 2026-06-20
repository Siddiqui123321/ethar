from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .database import engine
from . import models
from .routes import api_router
import os

app = FastAPI(title="Inventory & Order Management API")

app.include_router(api_router)

# CORS - allow frontend to call APIs (adjust origins for production)
origins = os.getenv("CORS_ORIGINS", "*")
if origins == "*":
    allow_origins = ["*"]
else:
    allow_origins = [o.strip() for o in origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Rely on Alembic migrations to manage the schema. Do not create tables here
    # to avoid conflicts when migrations are applied at container startup.
    return


@app.get("/")
def root():
    return {"message": "Inventory & Order Management API"}
