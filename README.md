# HR Automation Multi-Agent System (FastAPI + LangGraph)

## Project Overview

This project is a **multi-agent HR automation system** built using **FastAPI and LangGraph**. It processes natural language HR requests and routes them to specialized agents using an orchestration pipeline with memory, audit logging, and intent classification.

---

# 1. Backend Stack

- Python 3.11+
- FastAPI framework
- LangGraph (agent orchestration)
- SQLite database integration
- LLM APIs / Open-source model support (extensible)
- Environment configuration using `.env`

---

#  2. Core Functionality (REST API)

##  Request Handling
- `POST /request`
- Processes user HR queries through full AI pipeline

---

##  Audit Retrieval
- `GET /audit`
- Returns all logged system interactions from SQLite

---

##  Memory Management
- `GET /memory/{user_id}`
- Returns:
  - Short-Term Memory (STM)
  - Long-Term Memory (LTM)

---

##  Health Monitoring
- `GET /health`
- Checks system status

---

##  Root Endpoint
- `GET /`
- Confirms API is running

---

#  3. Automated Orchestration System

## Pipeline Flow

```text
User Request
   ↓
Memory Layer (STM + LTM update)
   ↓
Intent Classification
   ↓
Routing Engine (Agent selection)
   ↓
Agent Execution
   ↓
Audit Logging (SQLite)
   ↓

```
#  4. Key Features

##  Intent Classification
Outputs:
- intent type
- confidence score

---

##  Agent Routing
Routes requests to:

- Leave Agent
- Scheduling Agent
- Compliance Agent
- Clarification Agent

---

##  Memory System

###  Short-Term Memory (STM)
- Stores last 5 messages per user
- Maintains conversation context

###  Long-Term Memory (LTM)
- Stores user preferences
- Extracted from meaningful patterns (e.g., “prefer”, “always”)

---

##  Audit Logging System
Append-only SQLite logging

Stores:
- user_id
- message
- intent
- confidence
- agent used

---

#  5. System Modules

## 1. Intent Classification Engine
- Rule-based classification (extensible to LLMs)

---

## 2. Agent Router
Handles routing logic between sub-agents.

---

## 3. Sub-Agent System

- Leave Agent → handles leave requests  
- Scheduling Agent → handles meetings/scheduling  
- Compliance Agent → handles policy requests  
- Clarification Agent → handles unclear inputs  

---

## 4. Memory System
- STM (session-based context)
- LTM (persistent user preferences)

---

## 5. Audit System
- SQLite-based logging
- Ensures traceability of every request

---

## 6. LangGraph Orchestrator
- Node-based execution pipeline

### Flow:
```text
classify → route → execute → log
```

#  6. Error Handling Strategy

- Unknown inputs → routed to Clarification Agent  
- Safe fallback responses  
- No raw stack traces exposed to users  
- Graceful failure handling  

---

#  7. How to Run the Project

## Step 1: Install dependencies

```bash
pip install fastapi uvicorn pydantic python-dotenv sqlalchemy langchain langgraph
```

## Step 2: Start server

```bash
uvicorn app.main:app --reload
```

## Step 3: Open API Docs

```bash
http://127.0.0.1:8000/docs
```

# 8. Future Improvements
- Replace rule-based classifier with LLM-based model
- Add vector database (FAISS / Chroma)
- Add authentication layer
- Dockerize system
- Deploy on cloud (AWS / Render)

## License

This project is developed for **educational and academic use only**.  
Commercial or clinical use is not permitted without proper validation.