from celery import Celery

from src.infrastructure.no_proxy import disable_system_proxies

disable_system_proxies()

app = Celery(
    "credit-committee",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["src.tasks.application_task"],
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    enable_utc=True,
)
