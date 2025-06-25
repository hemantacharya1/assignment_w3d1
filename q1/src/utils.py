import requests

def call_ollama(prompt: str, model: str = "qwen3:0.6b", stream: bool = False):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["response"]
