from sqlalchemy.orm import Session

from src.infrastructure.db.models import Application

from src.schemas import ApplicationDTO

class ApplicationRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, id: int) -> Application | None:
        return self._db.get(Application, id)

    def create(self, application: ApplicationDTO) -> Application:
        obj = Application(**application.model_dump())
        self._db.add(obj)
        self._db.flush()
        return obj

    def commit(self) -> None:
        self._db.commit()
