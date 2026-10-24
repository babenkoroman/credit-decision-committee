from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationCreateRequest(BaseModel):
    first_name: str | None = None
    second_name: str | None = None
    applicant_id: int | None = None
    credit_sum: float | None = None


class ApplicationCreatedResponse(BaseModel):
    id: int


class Vote(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    agent: str
    vote: str
    reason: str


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str | None
    second_name: str | None
    applicant_id: int | None
    credit_sum: float | None
    decision: str | None
    memo: str | None
    votes: list[Vote]
    created_at: datetime
    updated_at: datetime
