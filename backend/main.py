from fastapi import FastAPI, Query
from backend.agent_graph import create_agent

app = FastAPI()

agent_app = None


@app.on_event("startup")
def startup_event():
    global agent_app
    print("🧠 Creating agent graph...")
    agent_app = create_agent()
    print("✅ System ready!")


@app.get("/ask")
async def ask(q: str = Query(...)):

    inputs = {
        "messages": [q],
        "context": []
    }

    result = await agent_app.ainvoke(inputs, {"configurable": {"thread_id": "1"}})

    raw_context = result.get("context", [])

    # clean + deduplicate sources
    clean_sources = list(dict.fromkeys(raw_context))

    return {
        "question": q,
        "answer": result["messages"][-1],
        "sources": clean_sources
    }