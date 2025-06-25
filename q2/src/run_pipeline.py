import json
from pathlib import Path
from generate_paths import generate_paths
from evaluate_paths import aggregate_answers
from optimize_prompt import optimize_prompt
from utils import call_ollama

# Load tasks and base prompt
TASKS = json.loads(Path("../tasks/tasks.json").read_text())
BASE_PROMPT_PATH = Path("../prompts/base_prompt.txt")
ORIGINAL_PROMPT = BASE_PROMPT_PATH.read_text()

# Track overall results
results_summary = []

# Utility to rerun with optimized prompt
def generate_with_custom_prompt(task, new_prompt, num_paths=5):
    filled_prompt = new_prompt.replace("{{input}}", task["input"])
    paths = []
    for i in range(num_paths):
        output = call_ollama(filled_prompt)
        paths.append({
            "path_id": f"retry_{i}",
            "response": output.strip()
        })
    return paths

# Loop over tasks
for task in TASKS:
    print(f"\n🧠 Processing Task: {task['task_id']}")
    print(f"📘 Input: {task['input']}")

    # Step 1: Generate Reasoning Paths
    paths = generate_paths(task, num_paths=5)

    # Step 2: Aggregate Answer using Self-Consistency
    result = aggregate_answers(paths)

    received = result["aggregated_answer"]
    expected = task["expected_output"]

    print("\n🧠 Reasoning Paths:")
    for p in paths:
        print(f"\n-- Path {p['path_id']} --\n{p['response']}")

    print(f"\n🔎 Aggregated Answer: {received}")
    print(f"✅ Expected Answer:   {expected}")
    print(f"📊 Votes: {result['votes']}")

    # Save logs for this task
    log = {
        "task_id": task["task_id"],
        "input": task["input"],
        "expected": expected,
        "received": received,
        "votes": result["votes"],
        "paths": paths,
        "correct": received == expected
    }

    # Step 3: Check if wrong → optimize prompt
    if received != expected:
        print("\n❌ Mismatch detected. Triggering prompt optimization...\n")
        improved_prompt = optimize_prompt(
            task_input=task["input"],
            expected_output=expected,
            received_output=received,
            original_prompt=ORIGINAL_PROMPT
        )

        # Save improved prompt
        versioned_path = Path(f"../prompts/optimized_prompt_{task['task_id']}.txt")
        versioned_path.write_text(improved_prompt)

        print("✨ Improved Prompt:\n")
        print(improved_prompt)

        # Step 4: Retry with optimized prompt
        print("\n🔁 Retrying with improved prompt...")
        retry_paths = generate_with_custom_prompt(task, improved_prompt)
        retry_result = aggregate_answers(retry_paths)
        retry_answer = retry_result["aggregated_answer"]

        print(f"\n🔁 Retry Aggregated Answer: {retry_answer}")
        print(f"📊 Retry Votes: {retry_result['votes']}")

        # Save retry results
        log["retry"] = {
            "received": retry_answer,
            "votes": retry_result["votes"],
            "paths": retry_paths,
            "correct": retry_answer == expected
        }
    else:
        print("\n✅ Correct answer. No prompt optimization needed.")

    results_summary.append(log)

# Save logs
Path("../logs").mkdir(exist_ok=True)
Path("../logs/run_1.json").write_text(json.dumps(results_summary, indent=2))

# Accuracy report
num_correct_first_try = sum(1 for r in results_summary if r["correct"])
num_correct_after_retry = sum(
    1 for r in results_summary if r.get("correct") or (r.get("retry") and r["retry"]["correct"])
)

print(f"\n📈 Accuracy before retry: {num_correct_first_try}/{len(results_summary)}")
print(f"✅ Final accuracy (after retry): {num_correct_after_retry}/{len(results_summary)}")
