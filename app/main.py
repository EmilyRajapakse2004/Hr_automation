from fastapi import FastAPI

from app.models import UserRequest
from app.graph import run_graph

from app.memory import (
    add_to_stm,
    get_stm,
    add_to_ltm,
    extract_fact,
    get_ltm
)

app = FastAPI(title="HR Automation Platform")


# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {"message": "HR Automation Platform Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# -----------------------------
# Core Request Endpoint
# -----------------------------
@app.post("/request")
def handle_request(request: UserRequest):

    # -------------------------
    # Memory Layer (STM + LTM)
    # -------------------------
    add_to_stm(request.user_id, request.message)

    fact = extract_fact(request.message)
    if fact:
        add_to_ltm(request.user_id, fact)

    # -------------------------
    # LangGraph Execution
    # -------------------------
    result = run_graph(request.user_id, request.message)

    # -------------------------
    # Response
    # -------------------------
    return {
        "intent": result.get("intent"),
        "confidence": result.get("confidence"),
        "response": result.get("response"),
        "stm": get_stm(request.user_id),
        "ltm": get_ltm(request.user_id)
    }


# -----------------------------
# Optional: Health Debug View
# -----------------------------
@app.get("/memory/{user_id}")
def view_memory(user_id: str):
    return {
        "stm": get_stm(user_id),
        "ltm": get_ltm(user_id)
    }