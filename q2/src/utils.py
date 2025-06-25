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

    try:
        result = response.json()
    except Exception as e:
        print("❌ Failed to parse JSON from Ollama response")
        print(response.text)
        return "ERROR: Failed to parse response."

    if "response" in result:
        return result["response"]
    else:
        print("❌ 'response' key missing in Ollama reply:")
        print(result)
        return "ERROR: No valid output."
