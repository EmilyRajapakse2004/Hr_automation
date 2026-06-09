from langgraph.graph import StateGraph, END

from app.classifier import classify_intent
from app.router import route_agent
from app.audit import log_request


# -----------------------------
# State definition (dict-based)
# -----------------------------
def init_state(user_id, message):
    return {
        "user_id": user_id,
        "message": message,
        "intent": None,
        "confidence": None,
        "agent": None,
        "response": None
    }


# -----------------------------
# Nodes
# -----------------------------

def classify_node(state):
    intent, confidence = classify_intent(state["message"])
    state["intent"] = intent
    state["confidence"] = confidence
    return state


def route_node(state):
    agent = route_agent(state["intent"])
    state["agent"] = agent
    return state


def action_node(state):
    response = state["agent"].process(state["message"])
    state["response"] = response

    # audit log
    log_request(
        state["user_id"],
        state["message"],
        state["intent"],
        state["confidence"],
        state["agent"].__class__.__name__
    )

    return state


# -----------------------------
# Build Graph
# -----------------------------
workflow = StateGraph(dict)

workflow.add_node("classify", classify_node)
workflow.add_node("route", route_node)
workflow.add_node("action", action_node)

workflow.set_entry_point("classify")

workflow.add_edge("classify", "route")
workflow.add_edge("route", "action")
workflow.add_edge("action", END)

app_graph = workflow.compile()


# -----------------------------
# Runner function
# -----------------------------
def run_graph(user_id: str, message: str):

    state = init_state(user_id, message)

    result = app_graph.invoke(state)

    return result