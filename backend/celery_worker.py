import os
from celery import Celery

REDIS = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("worker", broker=REDIS, backend=REDIS)

# configure a simple daily schedule (can be run with celery beat)
celery_app.conf.beat_schedule = {
    "train-models-daily": {
        "task": "ml.train_models",
        "schedule": 86400.0,
    }
}


@celery_app.task(name="ml.train_models")
def train_models_task():
    # Import here to avoid heavy imports at module load
    try:
        from app.ml_train import train_all_models

        train_all_models()
        return True
    except Exception as e:
        print("Error training models:", e)
        return False
