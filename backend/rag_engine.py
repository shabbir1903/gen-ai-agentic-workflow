# backend/rag_engine.py
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_compressors import FlashrankRerank
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os


class ProductionRAG:
    def __init__(self):
        print("🛡️  RAG Engine: Initializing...")
        self.embeddings = OllamaEmbeddings(model="llama3")
        # Ensure the directory exists
        if not os.path.exists("./chroma_db"):
            os.makedirs("./chroma_db")
        self.vector_db = Chroma(persist_directory="./chroma_db", embedding_function=self.embeddings)
        self.compressor = FlashrankRerank()

    def load_docs(self):
        """
        ACTUAL IMPLEMENTATION:
        Reads PDFs from a 'data' folder and indexes them.
        """
        print("📂 RAG Engine: Starting ingestion pipeline...")

        # 1. Load Documents (Create a folder named 'data' and put your PDFs there)
        if not os.path.exists("./data"):
            os.makedirs("./data")
            print("⚠️ Created 'data' folder. Please put your PDF roadmap there and restart.")
            return False

        loader = DirectoryLoader("./data", glob="./*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()

        if not docs:
            print("❌ No documents found in ./data folder.")
            return False

        # 2. Chunking (Critical for context window management)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)

        # 3. Ingest into ChromaDB
        print(f"Indexing {len(chunks)} chunks into Vector Store...")
        self.vector_db.add_documents(chunks)
        print("✅ Ingestion complete.")
        return True

    def search(self, query: str):
        return self.get_context(query)

    def get_context(self, query: str):
        # We search for 10 chunks, then let Flashrank narrow it down to the best ones
        base_retriever = self.vector_db.as_retriever(search_kwargs={"k": 10})
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=self.compressor,
            base_retriever=base_retriever
        )
        return compression_retriever.invoke(query)