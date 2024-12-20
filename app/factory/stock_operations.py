from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.models.product import Product
from fastapi import HTTPException

class StockOperation(ABC):
    def __init__(self, db: Session, product_id: int):
        self.db = db
        self.product_id = product_id
        self.product = self._get_product()

    def _get_product(self) -> Product:
        product = self.db.query(Product).filter(Product.id == self.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @abstractmethod
    def execute(self, quantity: int) -> Product:
        pass

class AddStock(StockOperation):
    def execute(self, quantity: int) -> Product:
        self.product.quantity += quantity
        self.db.commit()
        return self.product

class RemoveStock(StockOperation):
    def execute(self, quantity: int) -> Product:
        if self.product.quantity < quantity:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock available"
            )
        self.product.quantity -= quantity
        self.db.commit()
        return self.product

class UpdateStock(StockOperation):
    def execute(self, quantity: int) -> Product:
        self.product.quantity = quantity
        self.db.commit()
        return self.product

class StockOperationFactory:
    @staticmethod
    def create_operation(operation_type: str, db: Session, product_id: int) -> StockOperation:
        operations = {
            "add": AddStock,
            "remove": RemoveStock,
            "update": UpdateStock
        }
        
        operation_class = operations.get(operation_type.lower())
        if not operation_class:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid operation type: {operation_type}"
            )
        
        return operation_class(db, product_id)