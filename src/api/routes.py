import time

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.api.dependencies import get_application_service
from src.infrastructure.db.session import get_db
from src.schemas import ApplicationCreatedResponse, ApplicationDTO
from src.services.application import ApplicationService

router = APIRouter()


@router.get("/")
def index():
    return {"message": "OK"}


@router.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "ok"}


@router.post("/application", response_model=ApplicationCreatedResponse)
def application(
    body: ApplicationDTO,
    service: ApplicationService = Depends(get_application_service),
) -> ApplicationCreatedResponse:
    start = time.perf_counter()
    result = service.process(body)
    elapsed = time.perf_counter() - start
    print(f"POST /application: {elapsed:.4f} сек.")
    return result

@router.get("/applications")
def applications(
    service: ApplicationService = Depends(get_application_service),
):
    return service.get_list()