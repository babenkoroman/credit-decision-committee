from src.agents.graph import build_graph
from src.agents.state import State
from src.infrastructure.celery import app as celery_app
from src.infrastructure.db.models import AgentVote, Application
from src.infrastructure.db.repositories.application import ApplicationRepository
from src.infrastructure.db.session import SessionLocal
from src.infrastructure.llm.deepseek import get_llm
from src.schemas import ApplicationCreatedResponse, ApplicationDTO


@celery_app.task
def add_to_process(application_id: int) -> None:
    db = SessionLocal()
    try:
        application = db.get(Application, application_id)
        if application is None:
            return

        result = build_graph(application).invoke(State())

        application.decision = result["decision"]
        application.memo = result["memo"]
        application.votes.clear()
        for vote in result["votes"]:
            data = vote.model_dump() if hasattr(vote, "model_dump") else vote
            application.votes.append(
                AgentVote(
                    agent=data["agent"],
                    vote=data["vote"],
                    reason=data["reason"],
                )
            )
        db.commit()
    finally:
        db.close()


class ApplicationService:
    def __init__(self, repo: ApplicationRepository, llm=None) -> None:
        self._repo = repo
        self._llm = llm or get_llm()

    def process(self, application: ApplicationDTO) -> ApplicationCreatedResponse:
        obj = self._repo.create(application)
        self._repo.commit()
        add_to_process.delay(obj.id)
        return ApplicationCreatedResponse(id=obj.id)
