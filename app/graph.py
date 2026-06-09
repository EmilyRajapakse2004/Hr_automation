from langgraph.graph import StateGraph, END

from app.classifier import classify_intent
from app.audit import log_request


def init_state(user_id, message):
    return {
        "user_id": user_id,
        "message": message,
        "intent": None,
        "confidence": None,
        "agent": None,
        "response": None
    }


def classify_node(state):
    intent, confidence = classify_intent(state["message"])
    state["intent"] = intent
    state["confidence"] = confidence
    return state


def route_node(state):
    from app.router import route_agent   # FIX: avoid import issues
    state["agent"] = route_agent(state["intent"])
    return state


def action_node(state):
    response = state["agent"].process(state["message"])
    state["response"] = response

    log_request(
        state["user_id"],
        state["message"],
        state["intent"],
        state["confidence"],
        state["agent"].__class__.__name__
    )

    return state


workflow = StateGraph(dict)

workflow.add_node("classify", classify_node)
workflow.add_node("route", route_node)
workflow.add_node("action", action_node)

workflow.set_entry_point("classify")

workflow.add_edge("classify", "route")
workflow.add_edge("route", "action")
workflow.add_edge("action", END)

app_graph = workflow.compile()


def run_graph(user_id: str, message: str):
    state = init_state(user_id, message)
    return app_graph.invoke(state)