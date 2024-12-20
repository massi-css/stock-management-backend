from fastapi import APIRouter
from app.routes.product_routes import product_router

api_router = APIRouter()

@api_router.get("/")
def hellowolrd():
    return "hello world"



api_router.include_router(product_router, prefix="/products", tags=["products"])