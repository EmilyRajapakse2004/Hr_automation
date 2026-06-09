from fastapi import FastAPI

from app.models import UserRequest
from app.classifier import classify_intent
from app.router import route_agent

from app.audit import create_table, log_request, get_logs

from app.memory import (
    add_to_stm,
    get_stm,
    add_to_ltm,
    extract_fact,
    get_ltm
)

app = FastAPI(title="HR Automation Platform")

# -----------------------------
# Initialize DB
# -----------------------------
create_table()


# -----------------------------
# Root endpoints
# -----------------------------
@app.get("/")
def root():
    return {"message": "HR Automation Platform Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# -----------------------------
# Core endpoint
# -----------------------------
@app.post("/request")
def handle_request(request: UserRequest):

    # -------------------------
    # 1. STM Memory update
    # -------------------------
    add_to_stm(request.user_id, request.message)

    # -------------------------
    # 2. LTM extraction
    # -------------------------
    fact = extract_fact(request.message)
    if fact:
        add_to_ltm(request.user_id, fact)

    # -------------------------
    # 3. Intent classification
    # -------------------------
    intent, confidence = classify_intent(request.message)

    # -------------------------
    # 4. Route to agent
    # -------------------------
    agent = route_agent(intent)

    response = agent.process(request.message)

    # -------------------------
    # 5. Audit logging
    # -------------------------
    log_request(
        request.user_id,
        request.message,
        intent,
        confidence,
        agent.__class__.__name__
    )

    # -------------------------
    # 6. Return response
    # -------------------------
    return {
        "intent": intent,
        "confidence": confidence,
        "response": response,
        "stm": get_stm(request.user_id),
        "ltm": get_ltm(request.user_id)
    }


# -----------------------------
# Audit endpoint
# -----------------------------
@app.get("/audit")
def audit_logs():
    return {"logs": get_logs()}