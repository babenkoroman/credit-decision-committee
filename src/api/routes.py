import logging
import time

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_application_service
from src.schemas import (
    ApplicationCreateRequest,
    ApplicationCreatedResponse,
    ApplicationResponse,
)
from src.services.application import ApplicationService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
def index() -> dict[str, str]:
    return {"message": "OK"}


@router.post(
    "/applications",
    response_model=ApplicationCreatedResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def create_application(
    body: ApplicationCreateRequest,
    service: ApplicationService = Depends(get_application_service),
) -> ApplicationCreatedResponse:
    start = time.perf_counter()
    application_id = service.submit(body)
    elapsed = time.perf_counter() - start
    logger.info("POST /applications completed in %.4f seconds", elapsed)
    return ApplicationCreatedResponse(id=application_id)


@router.get("/applications", response_model=list[ApplicationResponse])
def list_applications(
    service: ApplicationService = Depends(get_application_service),
) -> list[ApplicationResponse]:
    return service.list()


@router.get(
    "/applications/{application_id}",
    response_model=ApplicationResponse,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Application not found"}},
)
def get_application(
    application_id: int,
    service: ApplicationService = Depends(get_application_service),
) -> ApplicationResponse:
    application = service.get(application_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    return application
