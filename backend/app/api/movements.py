from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..models import Movement, Product
from .. import audit

router = APIRouter()


@router.post("/", response_model=dict)
def create_movement(product_id: int, type: str, quantity: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    mv = Movement(product_id=product_id, type=type, quantity=quantity)
    db.add(mv)
    db.commit()
    db.refresh(mv)
    # audit
    audit.log(db, data=f"movement:{mv.id}:{type}:{quantity}")
    return {"id": mv.id, "status": "ok"}


@router.get("/", response_model=List[dict])
def list_movements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    q = db.query(Movement).offset(skip).limit(limit).all()
    return [{"id": m.id, "product_id": m.product_id, "type": m.type, "quantity": m.quantity, "timestamp": m.timestamp} for m in q]
