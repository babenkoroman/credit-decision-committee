from langchain_core.messages import SystemMessage

from src.agents.state import State, Vote
from src.infrastructure.llm.deepseek import get_llm
from src.rules.hard_stops import risk_decision


class RiskAgent:
    def __init__(self, application, llm=None):
        self._application = application
        self._llm = llm or get_llm()

    def __call__(self, state: State) -> dict:
        vote = risk_decision(self._application.credit_sum)

        result = self._llm.invoke(
            [
                SystemMessage(
                    content=(
                        f"Мы на модели рисков решили по заявке: {vote}. "
                        "Объясни это решение кратко в два предложения. "
                        "Не меняй само решение."
                    )
                )
            ]
        )

        return {
            "votes": [
                Vote(agent="risk", vote=vote, reason=result.content.strip())
            ]
        }
