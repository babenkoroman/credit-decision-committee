from pydantic import BaseModel, Field


class ApplicationDTO(BaseModel):
    first_name: str | None = None
    second_name: str | None = None
    applicant_id: int | None = None
    credit_sum: float | None = None


class ApplicationCreatedResponse(BaseModel):
    id: int


class Vote(BaseModel):
    agent: str
    vote: str
    reason: str


class DecisionResponse(BaseModel):
    decision: str = Field(description="approve | reject | manual_review")
    memo: str
    votes: list[Vote]
