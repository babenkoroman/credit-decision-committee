from typing import Annotated

import operator
from pydantic import BaseModel, Field

from src.schemas import Vote

__all__ = ["State", "Vote"]


class State(BaseModel):
    votes: Annotated[list[Vote], operator.add] = Field(default_factory=list)
    decision: str = ""
    memo: str = ""
