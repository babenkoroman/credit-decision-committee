from src.infrastructure.db.repositories.application import ApplicationRepository
from src.schemas import ApplicationCreateRequest, ApplicationResponse
from src.tasks.application_task import add_to_process


class ApplicationService:
    def __init__(self, repo: ApplicationRepository) -> None:
        self._repo = repo

    def submit(self, application: ApplicationCreateRequest) -> int:
        obj = self._repo.create(application.model_dump())
        self._repo.commit()
        add_to_process.delay(obj.id)
        return obj.id

    def list(self) -> list[ApplicationResponse]:
        return [
            ApplicationResponse.model_validate(application)
            for application in self._repo.list()
        ]

    def get(self, application_id: int) -> ApplicationResponse | None:
        application = self._repo.get_by_id(application_id)
        if application is None:
            return None
        return ApplicationResponse.model_validate(application)
