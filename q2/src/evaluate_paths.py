import re
from collections import Counter

def extract_answer(text):
    """
    Try to extract a final answer (e.g., number or Yes/No) from the model's reasoning.
    Adjust based on your prompt format.
    """
    # Look for common patterns like "Answer: 42" or "Final Answer: 42"
    match = re.search(r"(?:Answer|Final Answer)[:\s]*([\w\.\-]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Fallback: take last line if no explicit marker
    return text.strip().split("\n")[-1].strip()

def aggregate_answers(paths):
    """
    Aggregate answers using Self-Consistency (majority vote).
    """
    answers = [extract_answer(p["response"]) for p in paths]
    freq = Counter(answers)
    most_common = freq.most_common(1)[0]

    return {
        "answers": answers,
        "aggregated_answer": most_common[0],
        "votes": freq
    }
