from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.db.repositories.application import ApplicationRepository
from src.infrastructure.db.session import get_db
from src.services.application import ApplicationService


def get_application_repo(
    db: Session = Depends(get_db),
) -> ApplicationRepository:
    return ApplicationRepository(db)


def get_application_service(
    repo: ApplicationRepository = Depends(get_application_repo),
) -> ApplicationService:
    return ApplicationService(repo=repo)
