from src.schemas import ApplicationDTO
from src.infrastructure.llm.deepseek import get_llm
from src.agents.graph import build_graph


class ApplicationService:
    def __init__(self, application: ApplicationDTO, llm=None):
        self._application = application
        self._llm = llm or get_llm()

    def process(self):
        # тут сразу начну несколько обработчиков запускать в
        # langraph, потом попробую переделать это в celery

        graph = build_graph(self._application, llm=self._llm)

        result = graph.invoke({"summary": ""})

        return {
            "status": "Ok",
            "result": result["result"],
        }
