from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    StockOperation
)
from app.controllers.product_controller import ProductController

product_router = APIRouter()

@product_router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return ProductController.get_products(db, skip, limit)

@product_router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return ProductController.get_product(db, product_id)

@product_router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return ProductController.create_product(db, product)

@product_router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    return ProductController.update_product(db, product_id, product)

@product_router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return ProductController.delete_product(db, product_id)

@product_router.post("/{product_id}/stock", response_model=ProductResponse)
def add_stock(
    product_id: int,
    stock: StockOperation,
    db: Session = Depends(get_db)
):
    return ProductController.handle_stock_operation(
        db, product_id, stock.quantity, "add"
    )

@product_router.put("/{product_id}/stock", response_model=ProductResponse)
def update_stock(
    product_id: int,
    stock: StockOperation,
    db: Session = Depends(get_db)
):
    return ProductController.handle_stock_operation(
        db, product_id, stock.quantity, "update"
    )

@product_router.delete("/{product_id}/stock", response_model=ProductResponse)
def remove_stock(
    product_id: int,
    stock: StockOperation,
    db: Session = Depends(get_db)
):
    return ProductController.handle_stock_operation(
        db, product_id, stock.quantity, "remove"
    )