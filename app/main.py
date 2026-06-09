from fastapi import FastAPI

from app.models import UserRequest
from app.graph import run_graph
from app.audit import get_logs

from app.audit import create_table
from app.memory import (
    add_to_stm,
    get_stm,
    add_to_ltm,
    extract_fact,
    get_ltm
)

app = FastAPI(title="HR Automation Platform")

create_table()


@app.get("/")
def root():
    return {"message": "HR Automation Platform Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/request")
def handle_request(request: UserRequest):

    # memory
    add_to_stm(request.user_id, request.message)

    fact = extract_fact(request.message)
    if fact:
        add_to_ltm(request.user_id, fact)

    # LangGraph
    result = run_graph(request.user_id, request.message)

    return {
        "intent": result["intent"],
        "confidence": result["confidence"],
        "response": result["response"],
        "stm": get_stm(request.user_id),
        "ltm": get_ltm(request.user_id)
    }

@app.get("/audit")
def audit_logs():
    return {"logs": get_logs()}