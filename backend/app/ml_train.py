"""Training helpers to build per-product forecasting models and persist them."""
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Movement
import os
import pickle
from sklearn.linear_model import LinearRegression
import numpy as np
from collections import defaultdict


MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models_artifacts")
os.makedirs(MODELS_DIR, exist_ok=True)


def _gather_history(db: Session):
    # return dict product_id -> list of historical OUT quantities (ordered by time)
    q = db.query(Movement).filter(Movement.type == 'OUT').order_by(Movement.timestamp.asc()).all()
    data = defaultdict(list)
    for m in q:
        data[m.product_id].append(int(m.quantity))
    return data


def train_model_for_series(series):
    # simple linear regression on index -> quantity
    if len(series) < 2:
        return None
    X = np.arange(len(series)).reshape(-1, 1)
    y = np.array(series)
    model = LinearRegression()
    model.fit(X, y)
    return model


def train_all_models():
    db = SessionLocal()
    try:
        histories = _gather_history(db)
        saved = []
        for pid, series in histories.items():
            model = train_model_for_series(series)
            if model is None:
                continue
            path = os.path.join(MODELS_DIR, f"model_product_{pid}.pkl")
            with open(path, "wb") as f:
                pickle.dump(model, f)
            saved.append(path)
        return saved
    finally:
        db.close()


def list_models():
    paths = []
    for fn in os.listdir(MODELS_DIR):
        if fn.endswith('.pkl'):
            paths.append(os.path.join(MODELS_DIR, fn))
    return paths


def load_model_for_product(product_id: int):
    path = os.path.join(MODELS_DIR, f"model_product_{product_id}.pkl")
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return pickle.load(f)
