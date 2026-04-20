import sys
import os

# Get the path to your .venv site-packages
venv_site_packages = os.path.abspath(".venv/lib/python3.13/site-packages")

# Insert it at the very beginning of the search path
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

print(f"--- 🛡️  Path Isolation Active: {sys.path[0]} ---")
# Normal imports proceed below

from fastapi import FastAPI, Query
from backend.agent_graph import create_agent

app = FastAPI()
# Initialize the compiled LangGraph agent once at startup
agent_app = create_agent()


@app.get("/ask")
async def ask(q: str = Query(..., description="The user question")):
    # 1. Initialize the state for the LangGraph
    inputs = {"messages": [q], "context": [], "is_relevant": False}

    # 2. Run the agentic loop
    # The agent will move through retrieve -> grade -> generate nodes
    config = {"configurable": {"thread_id": "1"}}  # Essential for state memory
    result = await agent_app.ainvoke(inputs, config)

    # 3. Return the final state's context and message
    return {
        "question": q,
        "answer": result["messages"][-1],  # The last message is the LLM's response
        "sources": result["context"]
    }