from src.infrastructure.db.repositories.application import ApplicationRepository
from src.infrastructure.llm.deepseek import get_llm
from src.schemas import ApplicationCreatedResponse, ApplicationDTO

from typing import List

from src.infrastructure.db.models import Application

from src.tasks.application_task import add_to_process

class ApplicationService:
    def __init__(self, repo: ApplicationRepository, llm=None) -> None:
        self._repo = repo
        self._llm = llm or get_llm()

    def process(self, application: ApplicationDTO) -> ApplicationCreatedResponse:
        obj = self._repo.create(application)
        self._repo.commit()
        add_to_process.delay(obj.id)
        return ApplicationCreatedResponse(id=obj.id)

    def get_list(self) -> List[Application]: 
        return self._repo.all()