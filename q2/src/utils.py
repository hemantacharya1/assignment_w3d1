import requests

def call_ollama(prompt: str, model: str = "qwen3:0.6b"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["response"]
