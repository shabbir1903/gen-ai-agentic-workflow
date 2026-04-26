from typing import TypedDict, List

from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

from backend.rag_engine import ProductionRAG
from backend import config


# ---------------------------
# STATE
# ---------------------------
class AgentState(TypedDict):
    messages: List[str]
    context: List[str]


# ---------------------------
# GLOBALS (initialized later)
# ---------------------------
rag = None
llm = None


# ---------------------------
# INIT FUNCTION (IMPORTANT FIX)
# ---------------------------
def init_rag():
    global rag, llm

    if rag is None:
        rag = ProductionRAG()
        rag.load_docs()

    if llm is None:
        llm = ChatOllama(
            model=config.MODEL_NAME,
            base_url=config.OLLAMA_BASE_URL,
            temperature=0
        )

    print("🧠 RAG initialized")


# ---------------------------
# NODES
# ---------------------------
def retrieve(state: AgentState):
    question = state["messages"][-1]

    docs = rag.get_context(question)
    context = [d.page_content for d in docs]

    return {
        "messages": state["messages"],  # ✅ IMPORTANT FIX
        "context": context
    }


def generate(state: AgentState):
    question = state["messages"][-1]
    context = "\n\n".join(state.get("context", []))

    if not context.strip():
        return {
            "messages": state["messages"] + ["Not found in documents"]
        }

    prompt = f"""
You are a RAG assistant.

Context:
{context}

Question:
{question}

Answer ONLY using context.
"""

    response = llm.invoke(prompt)

    return {
        "messages": state["messages"] + [response.content],
        "context": state["context"]
    }

# ---------------------------
# GRAPH
# ---------------------------
def create_agent():
    init_rag()

    graph = StateGraph(AgentState)

    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)

    graph.set_entry_point("retrieve")

    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()