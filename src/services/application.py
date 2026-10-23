from src.agents.graph import build_graph
from src.infrastructure.db.repositories.application import ApplicationRepository
from src.infrastructure.llm.deepseek import get_llm
from src.schemas import (
    ApplicationCreatedResponse,
    ApplicationDTO,
    DecisionResponse,
    Vote,
)


class ApplicationService:
    def __init__(self, repo: ApplicationRepository, llm=None) -> None:
        self._repo = repo
        self._llm = llm or get_llm()

    def process(self, application: ApplicationDTO) -> ApplicationCreatedResponse:
        obj = self._repo.create(application)
        self._repo.commit()
        return ApplicationCreatedResponse(id=obj.id)
