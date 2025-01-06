from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.factory.stock_operations import StockOperationFactory
from sqlalchemy import or_

class ProductController:
    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def get_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    def create_product(db: Session, product: ProductCreate):
        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def update_product(db: Session, product_id: int, product: ProductUpdate):
        db_product = ProductController.get_product(db, product_id)
        update_data = product.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_product, field, value)
            
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def delete_product(db: Session, product_id: int):
        product = ProductController.get_product(db, product_id)
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}

    @staticmethod
    def handle_stock_operation(
        db: Session,
        product_id: int,
        quantity: int,
        operation_type: str
    ):
        operation = StockOperationFactory.create_operation(
            operation_type,
            db,
            product_id
        )
        return operation.execute(quantity)
    @staticmethod
    def search_products(db: Session, search_term: str, skip: int = 0, limit: int = 100):
        products = db.query(Product).filter(
            or_(
                Product.name.ilike(f"%{search_term}%"),
                Product.description.ilike(f"%{search_term}%")
            )
        ).offset(skip).limit(limit).all()

        if not products:
            raise HTTPException(status_code=404, detail="No products found matching the search criteria")

        return products