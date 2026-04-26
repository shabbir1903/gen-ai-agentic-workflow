import os
from typing import List

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from backend import config


class ProductionRAG:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=config.OLLAMA_BASE_URL
        )

        self.vectorstore = None

    # ---------------------------
    # LOAD FILES (PDF + TXT SAFE)
    # ---------------------------
    def load_docs(self, folder="data"):
        if not os.path.exists(folder):
            raise ValueError(f"Data folder not found: {folder}")

        docs: List[Document] = []

        print(f"📁 Loading from: {os.path.abspath(folder)}")
        files = os.listdir(folder)
        print("📄 Files:", files)

        for file in files:
            path = os.path.join(folder, file)

            # ---- TXT FILE ----
            if file.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        docs.append(Document(page_content=content))

            # ---- PDF FILE ----
            elif file.endswith(".pdf"):
                try:
                    from langchain_community.document_loaders import PyPDFLoader
                    loader = PyPDFLoader(path)
                    pdf_docs = loader.load()
                    docs.extend(pdf_docs)
                except ImportError:
                    raise ImportError(
                        "❌ pypdf missing. Run: pip install pypdf"
                    )

        if not docs:
            raise ValueError("No valid documents found in /data")

        print(f"📚 Raw docs loaded: {len(docs)}")

        # ---------------------------
        # SPLIT TEXT
        # ---------------------------
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )

        chunks = splitter.split_documents(docs)

        # remove empty chunks (IMPORTANT FIX)
        chunks = [
            c for c in chunks
            if c.page_content and c.page_content.strip()
        ]

        print(f"✂️ Total chunks: {len(chunks)}")

        if len(chunks) == 0:
            raise ValueError("All chunks are empty after splitting")

        # ---------------------------
        # VECTOR STORE
        # ---------------------------
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="chroma_db"
        )

        print(f"✅ RAG loaded successfully with {len(chunks)} chunks")

    # ---------------------------
    # RETRIEVAL
    # ---------------------------
    def get_context(self, query: str):
        if not self.vectorstore:
            raise Exception("Vector DB not initialized")

        docs = self.vectorstore.similarity_search(query, k=4)

        # remove duplicates (VERY IMPORTANT FIX)
        seen = set()
        unique_docs = []

        for d in docs:
            text = d.page_content.strip()
            if text not in seen:
                seen.add(text)
                unique_docs.append(d)

        return unique_docs