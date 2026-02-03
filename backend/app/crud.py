from sqlalchemy.orm import Session
from . import models, schemas


def create_product(db: Session, product: schemas.ProductCreate):
    db_obj = models.Product(**product.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()
