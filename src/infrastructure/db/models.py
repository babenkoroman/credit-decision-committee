from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.base import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    second_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    applicant_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    credit_sum: Mapped[float | None] = mapped_column(Float, nullable=True)

    decision: Mapped[str | None] = mapped_column(String(32), nullable=True)
    memo: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    votes: Mapped[list["AgentVote"]] = relationship(
        back_populates="application",
        cascade="all, delete-orphan",
    )


class AgentVote(Base):
    __tablename__ = "agent_votes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
    )

    agent: Mapped[str] = mapped_column(String(64), nullable=False)
    vote: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    application: Mapped["Application"] = relationship(back_populates="votes")
