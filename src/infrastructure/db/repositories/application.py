from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from src.infrastructure.db.models import Application


class ApplicationRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, application_id: int) -> Application | None:
        stmt = self._with_votes().where(Application.id == application_id)
        return self._db.scalar(stmt)

    def create(self, data: dict[str, object]) -> Application:
        obj = Application(**data)
        self._db.add(obj)
        self._db.flush()
        return obj

    def commit(self) -> None:
        self._db.commit()

    def list(self) -> list[Application]:
        stmt = self._with_votes().order_by(Application.created_at.desc())
        return list(self._db.scalars(stmt).all())

    def _with_votes(self) -> Select[tuple[Application]]:
        return select(Application).options(selectinload(Application.votes))
