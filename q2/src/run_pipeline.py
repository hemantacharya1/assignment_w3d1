import json
from pathlib import Path
from generate_paths import generate_paths
from evaluate_paths import aggregate_answers

TASKS = json.loads(Path("../tasks/tasks.json").read_text())
task = TASKS[0]  # pick one task to start

print(f"\n🔍 Task: {task['input']}")
paths = generate_paths(task, num_paths=5)

print("\n🧠 Reasoning Paths:")
for p in paths:
    print(f"\n-- Path {p['path_id']} --\n{p['response']}")

result = aggregate_answers(paths)

print("\n✅ Aggregated Answer:")
print(f"Answer: {result['aggregated_answer']}")
print("Votes:", result["votes"])
