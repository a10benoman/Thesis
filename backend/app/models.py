from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base
import hashlib


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    unit_cost = Column(Float, nullable=True)
    selling_price = Column(Float, nullable=True)
    min_stock = Column(Integer, default=0)
    reorder_point = Column(Integer, default=0)
    lead_time_days = Column(Integer, default=0)


class Movement(Base):
    __tablename__ = "movements"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    type = Column(String, nullable=False)  # IN, OUT, MOVE, ADJUST
    quantity = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    prev_hash = Column(String, nullable=True)
    record_hash = Column(String, nullable=False)
    data = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def compute_hash(prev_hash: str, data: str) -> str:
        h = hashlib.sha256()
        if prev_hash:
            h.update(prev_hash.encode())
        h.update(data.encode())
        return h.hexdigest()
