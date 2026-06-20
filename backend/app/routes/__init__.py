from fastapi import APIRouter

api_router = APIRouter()

from . import products, customers, orders  # noqa: F401

api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
