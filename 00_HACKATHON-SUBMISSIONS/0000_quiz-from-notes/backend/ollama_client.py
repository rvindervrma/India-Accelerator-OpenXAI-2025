import json
import os
import requests


OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")


class OllamaClient:
    def __init__(self, model: str):
        # self.model = model
        self.model = "phi3:mini"


    def generate_json(self, prompt: str, system: str | None = None) -> str:
        """Call Ollama /api/generate to get a single JSON string response."""
        url = f"{OLLAMA_HOST}/api/generate"
        print(f"🌐 [DEBUG] Sending request to Ollama at {url} with model={self.model}")
        payload = {
        "model": self.model,
        "prompt": (system + "\n\n" + prompt) if system else prompt,
        "stream": False
        }
        resp = requests.post(url, json=payload, timeout=3000)
        resp.raise_for_status()
        data = resp.json()
        # Ollama returns { response: "..." }
        return data.get("response", "")

