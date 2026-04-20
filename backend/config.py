import os

# Ollama Local Configuration
MODEL_NAME = "llama3:latest" # Updated to match your 'curl' output
OLLAMA_BASE_URL = "http://localhost:11434"

# Observability remains critical even for local models
LANGCHAIN_TRACING_V2 = "true"
LANGCHAIN_API_KEY = "your-langsmith-key" # Recommended for debugging [cite: 162, 197]