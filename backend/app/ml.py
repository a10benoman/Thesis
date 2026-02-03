"""Simple ML helpers: moving average and linear regression forecasting."""
from typing import List
import numpy as np
from sklearn.linear_model import LinearRegression


def forecast_moving_average(history: List[float], horizon: int = 7) -> List[float]:
    if len(history) == 0:
        return [0.0] * horizon
    window = min(7, len(history))
    ma = np.mean(history[-window:])
    return [float(ma) for _ in range(horizon)]


def forecast_linear_regression(history: List[float], horizon: int = 7) -> List[float]:
    if len(history) < 2:
        return forecast_moving_average(history, horizon)
    X = np.arange(len(history)).reshape(-1, 1)
    y = np.array(history)
    model = LinearRegression()
    model.fit(X, y)
    future_X = np.arange(len(history), len(history) + horizon).reshape(-1, 1)
    preds = model.predict(future_X)
    return [float(max(0.0, p)) for p in preds]


def forecast_endpoint(product_id: int, horizon: int = 7):
    # Placeholder: in real app we'd load historical OUT movements from DB
    # For scaffold provide deterministic synthetic data for demo
    np.random.seed(product_id)
    history = list(np.maximum(0, np.random.poisson(5, size=60)))
    ma = forecast_moving_average(history, horizon)
    lr = forecast_linear_regression(history, horizon)
    return {"product_id": product_id, "horizon": horizon, "moving_average": ma, "linear_regression": lr}
