from pathlib import Path
from utils import call_ollama

OPTIMIZER_PROMPT_TEMPLATE = Path("../prompts/optimizer_prompt.txt").read_text()

def optimize_prompt(task_input, expected_output, received_output, original_prompt, model="qwen3:0.6b"):
    prompt = OPTIMIZER_PROMPT_TEMPLATE
    prompt = prompt.replace("{{input}}", task_input)
    prompt = prompt.replace("{{expected}}", expected_output)
    prompt = prompt.replace("{{received}}", received_output)
    prompt = prompt.replace("{{original_prompt}}", original_prompt.strip())

    improved_prompt = call_ollama(prompt, model=model)
    return improved_prompt.strip()
