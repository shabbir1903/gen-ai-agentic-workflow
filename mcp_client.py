import requests

class MCPClient:
    """Standardized interface for local AI to call enterprise APIs [cite: 177, 214]"""
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def get_enterprise_data(self, endpoint):
        # Security: Apply PII masking here before sending to local LLM [cite: 163]
        response = requests.get(f"{self.base_url}/{endpoint}")
        return response.json()