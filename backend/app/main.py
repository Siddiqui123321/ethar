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
    # In development this will create tables automatically, but in production
    # prefer using Alembic migrations. To create the DB schema with Alembic:
    #   alembic -c alembic.ini revision --autogenerate -m "init"
    #   alembic -c alembic.ini upgrade head
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception:
        # if DB isn't available on startup, continue; migrations should be applied separately
        pass


@app.get("/")
def root():
    return {"message": "Inventory & Order Management API"}
