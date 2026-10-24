from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from src.infrastructure.db.models import Application

from src.schemas import ApplicationDTO

from typing import List

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

    def all(self) -> List[Application]:
        stmt = select(Application).options(selectinload(Application.votes))
        return list(self._db.scalars(stmt).all())