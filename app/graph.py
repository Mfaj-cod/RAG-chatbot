from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from retriever import retrieve


class State(TypedDict):
    question: str
    contexts: List[str]
    scores: List[float]
    history: List[str]


def retrieve_node(state: State):
    ctx, scores = retrieve(state["question"])
    return {
        "contexts": ctx,
        "scores": scores
    }


graph = StateGraph(State)

graph.add_node("retrieve", retrieve_node)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", END)

app_graph = graph.compile()
