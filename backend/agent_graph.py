from typing import TypedDict, List
from langgraph.graph import StateGraph
try:
    from langchain_ollama import ChatOllama
except ImportError:
    from langchain_community.chat_models import ChatOllama
from backend import config
from backend.rag_engine import ProductionRAG  # Assuming your RAG class is here

# Initialize with the specific name 'llama3:latest'
llm = ChatOllama(
    model=config.MODEL_NAME,
    base_url=config.OLLAMA_BASE_URL,
    temperature=0 # Set to 0 for consistent, grounded production responses
)
from typing import TypedDict, List
from langgraph.graph import StateGraph, END


# ... other imports (Ollama, etc.)

# 1. Define the State first
class AgentState(TypedDict):
    messages: List[str]
    context: List[str]
    is_relevant: bool


# 2. Define the Node Functions BEFORE the graph assembly


rag_engine = ProductionRAG()
rag_engine.load_docs()  # Initialize the vector store


def retrieve_node(state: AgentState):
    print("---RETRIEVING FROM KNOWLEDGE BASE---")
    question = state["messages"][-1]

    # Call the actual search method
    search_results = rag_engine.get_context(question)

    # Extract text from the retrieved documents
    context_data = [doc.page_content for doc in search_results]

    return {"context": context_data}


from langchain_community.chat_models import ChatOllama
from backend import config

llm = ChatOllama(model=config.MODEL_NAME, base_url=config.OLLAMA_BASE_URL)


def generate_node(state: AgentState):
    print("---GENERATING RESPONSE VIA LLAMA 3---")
    context = "\n".join(state["context"])
    question = state["messages"][-1]

    prompt = f"""
    Answer the following question based ONLY on the provided context.
    If the context doesn't contain the answer, say you don't know.

    CONTEXT:
    {context}

    QUESTION:
    {question}
    """

    response = llm.invoke(prompt)

    # Return the real response content
    return {"messages": state["messages"] + [response.content]}


# 3. Assemble the Graph
def create_agent():
    workflow = StateGraph(AgentState)

    # Now Python knows what 'retrieve_node' is
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)

    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()