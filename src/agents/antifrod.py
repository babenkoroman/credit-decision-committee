from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.parse import parse_vote_response
from src.agents.state import State, Vote
from src.infrastructure.llm.deepseek import get_llm


class AntifrodAgent:
    def __init__(self, application, llm=None):
        self._application = application
        self._llm = llm or get_llm()

    def __call__(self, state: State) -> dict:
        application_json = self._application.model_dump_json(indent=2)

        result = self._llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Ты — антифрод-аналитик кредитного комитета.\n"
                        "Оцени заявку на признаки мошенничества. Не выдумывай факты.\n"
                        "Маппинг: низкий риск → approve, средний → manual_review, высокий → reject.\n"
                        "Ответь ТОЛЬКО JSON без markdown:\n"
                        '{"vote":"approve"|"reject"|"manual_review","reason":"обоснование с сигналами"}'
                    )
                ),
                HumanMessage(
                    content=(
                        "Данные заявки и заявителя (JSON):\n"
                        f"{application_json}"
                    )
                ),
            ]
        )

        vote, reason = parse_vote_response(result.content)
        return {"votes": [Vote(agent="antifrod", vote=vote, reason=reason)]}
