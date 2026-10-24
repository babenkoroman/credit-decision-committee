from celery import Celery

app = Celery(
    "credit-committee",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["src.services.application"],
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    enable_utc=True,
)
