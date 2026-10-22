from langgraph.graph import StateGraph, START, END

from src.agents.state import State
from src.agents.policy import PolicyAgent
from src.agents.risk import RiskAgent
from src.agents.advocat import AdvocatAgent
from src.agents.antifrod import AntifrodAgent
from src.agents.summarizer import SummarizerAgent
from src.infrastructure.llm.deepseek import get_llm


def build_graph(app, llm=None):
    llm = llm or get_llm()

    builder = StateGraph(State)

    # экземпляры, не классы: LangGraph вызывает node(state)
    builder.add_node("node_1", PolicyAgent(app, llm=llm))
    builder.add_node("node_2", RiskAgent(app, llm=llm))
    builder.add_node("node_3", AntifrodAgent(app, llm=llm))
    builder.add_node("node_4", AdvocatAgent(app, llm=llm))
    builder.add_node("node_5", SummarizerAgent(llm=llm))

    builder.add_edge(START, "node_1")
    builder.add_edge(START, "node_2")
    builder.add_edge(START, "node_3")
    builder.add_edge("node_3", "node_4")
    builder.add_edge("node_1", "node_5")
    builder.add_edge("node_2", "node_5")
    builder.add_edge("node_4", "node_5")
    builder.add_edge("node_5", END)

    return builder.compile()
