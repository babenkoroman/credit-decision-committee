from pydantic import BaseModel


class State(BaseModel):
    result: str = ""
    summary: str = ""
    antifrod_agent_decision: str = ""
    advocate_agent_decision: str = ""
