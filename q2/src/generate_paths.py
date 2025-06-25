import json
import random
from pathlib import Path
from utils import call_ollama

BASE_PROMPT = Path("../prompts/base_prompt.txt").read_text()

def generate_paths(task, num_paths=5):
    input_text = task["input"]
    prompt_template = BASE_PROMPT.replace("{{input}}", input_text)
    
    paths = []
    for i in range(num_paths):
        output = call_ollama(prompt_template)
        paths.append({
            "path_id": i,
            "response": output.strip()
        })
    
    return paths
