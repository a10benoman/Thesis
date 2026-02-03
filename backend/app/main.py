
from fastapi import FastAPI
from .db import init_db, get_db
from .ml import forecast_endpoint
from .api import products, movements, ml

app = FastAPI(title="Inventory ML System")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ml/forecast")
def ml_forecast(product_id: int, horizon: int = 7):
    return forecast_endpoint(product_id, horizon)


app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(movements.router, prefix="/movements", tags=["movements"])
app.include_router(ml.router, prefix="/ml", tags=["ml"])
