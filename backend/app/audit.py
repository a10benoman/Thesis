from sqlalchemy.orm import Session
from .models import AuditLog


def last_hash(db: Session) -> str:
    last = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
    return last.record_hash if last else None


def log(db: Session, data: str):
    prev = last_hash(db)
    record_hash = AuditLog.compute_hash(prev or "", data)
    rec = AuditLog(prev_hash=prev, record_hash=record_hash, data=data)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
