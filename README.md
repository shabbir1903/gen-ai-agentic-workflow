`# Agentic AI: Production-Ready RAG System (Ollama + LangGraph)

This project is a high-performance, local Agentic RAG system built with **Python 3.13**, **LangGraph**, and **Ollama (Llama 3)**. It transitions a standard linear RAG pipeline into a stateful, iterative reasoning engine capable of self-correction and high-precision retrieval.

---

## 🏗️ System Architecture

The system follows the **Agentic Loop** pattern (**Perceive → Reason → Act → Learn**), distinguishing it from traditional linear RAG systems.

### Core Components:

1. **Orchestrator (LangGraph)**
   Manages the stateful flow between reasoning nodes:
   `Retrieve → Grade → Generate → Reflect`

2. **RAG Engine (ChromaDB + Flashrank)**

   * Hybrid search (semantic + keyword)
   * Re-ranking to reduce **Top-K Noise**
   * Improves precision before LLM consumption

3. **Local LLM (Ollama - Llama 3)**

   * Handles embeddings + generation
   * Runs fully local → **data privacy + zero API cost**

4. **Interface Layer (FastAPI)**

   * Async API for real-time querying
   * Scalable entry point for UI or services

---

## 🔁 Agentic Workflow

```text
User Query
   ↓
Retrieve Documents
   ↓
Grade Relevance
   ↓
Generate Answer
   ↓
Self-Check / Reflection
   ↓
Refine (if needed)
```

Unlike traditional RAG, the system can **loop and improve responses** dynamically.

---

## 🚀 Step-by-Step Local Setup

### 1. Prerequisites

* **Python:** 3.13+
* **Ollama:** https://ollama.com/

---

### 2. Prepare the Local Model

```bash
ollama pull llama3:latest
ollama serve
```

---

### 3. Clone the Repository

```bash
git clone https://github.com/your-username/agentic-rag.git
cd agentic-rag
```

---

### 4. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

Example dependencies:

```txt
langgraph
langchain
chromadb
fastapi
uvicorn
ollama
flashrank
tiktoken
pydantic
```

---

### 6. Run the Application

```bash

/opt/homebrew/opt/python@3.11/bin/python3.11 -m venv .venv
source .venv/bin/activate
pip uninstall -y langchain langchain-core langchain-community langgraph langchain-text-splitters langchain-ollama langchain-chroma chromadb
pip cache purge
pip install -U pip

pip install \
  langchain==0.2.17 \
  langchain-core==0.2.43 \
  langchain-community==0.2.17 \
  langchain-text-splitters==0.2.4 \
  langgraph==0.2.35 \
  langchain-ollama==0.1.0 \
  langchain-chroma \
  chromadb \
  numpy==1.26.4
  python -c "from langchain_ollama import ChatOllama; print('OLLAMA OK')"
  python -c "from langchain_chroma import Chroma; print('CHROMA OK')"
  python -c "from langgraph.graph import StateGraph; print('LANGGRAPH OK')"
  
  pip install -r requirements.txt
  pip freeze > requirements.lock.txt
  pip-compile requirements.txt
  python -c "from backend.rag_engine import ProductionRAG; print('RAG OK')"
  python -c "from backend.agent_graph import create_agent; print('GRAPH OK')"
uvicorn backend.main:app --reload --port 8001
```

API will be available at:

```
http://localhost:8001/ask?q=What is RAG?
```

---

## 📡 API Usage

### Endpoint: `/query`

#### Request

```json
{
  "question": "What is Agentic RAG?"
}
```

#### Response

```json
{
  "answer": "Agentic RAG is an iterative retrieval system...",
  "sources": ["doc1", "doc2"]
}
```

---

## 🧠 Key Features

* ✅ Fully local (no external API dependency)
* ✅ Stateful multi-step reasoning
* ✅ Self-correcting responses
* ✅ Hybrid retrieval + re-ranking
* ✅ Production-ready FastAPI backend
* ✅ Modular LangGraph architecture

---

## 📊 Performance Optimizations

* Flashrank re-ranking → reduces irrelevant chunks
* Chunking strategies → improves retrieval quality
* Prompt tuning → minimizes hallucinations
* Async FastAPI → low-latency responses

---

## 🔐 Security & Privacy

* 100% local inference (Ollama)
* No data leaves your machine
* Ideal for **enterprise / sensitive workloads**

---

## 🛠️ Future Enhancements

* UI Dashboard (React / Next.js)
* Streaming responses
* Multi-agent collaboration
* Tool-augmented reasoning (web, DB, APIs)
* Vector DB scaling (Weaviate / Pinecone optional)

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Commit changes
4. Open a PR

---

## 📄 License

MIT License

---

## ⭐ Acknowledgements

* LangGraph for agent orchestration
* Ollama for local LLM runtime
* ChromaDB for vector storage
* Flashrank for re-ranking

---

## 💡 Summary

This project demonstrates how to move from:

```
Traditional RAG → Agentic RAG → Production AI System
```

If you're building **next-gen AI systems**, this architecture is a strong foundation.
