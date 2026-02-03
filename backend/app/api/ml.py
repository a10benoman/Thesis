from fastapi import APIRouter
from .. import ml
from ..ml_train import train_all_models, list_models

router = APIRouter()

@router.post("/train")
def trigger_train(async_task: bool = True):
    if async_task:
        # trigger celery task (lazy import to avoid hard dependency)
        try:
            from ...celery_worker import celery_app
            celery_app.send_task('ml.train_models')
        except Exception:
            # fallback: run training synchronously
            saved = train_all_models()
            return {"status": "done", "saved": saved}
        return {"status": "scheduled"}
    else:
        saved = train_all_models()
        return {"status": "done", "saved": saved}


@router.get("/models")
def get_models():
    return {"models": list_models()}
