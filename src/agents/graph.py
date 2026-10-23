from langgraph.graph import StateGraph, START, END

from src.agents.state import State
from src.agents.policy import PolicyAgent
from src.agents.risk import RiskAgent
from src.agents.advocat import AdvocatAgent
from src.agents.antifrod import AntifrodAgent
from src.agents.chair import ChairAgent
from src.infrastructure.llm.deepseek import get_llm


def build_graph(app, llm=None):
    llm = llm or get_llm()

    builder = StateGraph(State)

    builder.add_node("policy", PolicyAgent(app, llm=llm))
    builder.add_node("risk", RiskAgent(app, llm=llm))
    builder.add_node("antifrod", AntifrodAgent(app, llm=llm))
    builder.add_node("advocate", AdvocatAgent(app, llm=llm))
    builder.add_node("chair", ChairAgent(app, llm=llm))

    builder.add_edge(START, "policy")
    builder.add_edge(START, "risk")
    builder.add_edge(START, "antifrod")
    builder.add_edge("antifrod", "advocate")
    builder.add_edge("policy", "chair")
    builder.add_edge("risk", "chair")
    builder.add_edge("advocate", "chair")
    builder.add_edge("chair", END)

    return builder.compile()
