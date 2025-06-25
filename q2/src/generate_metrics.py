import json
from pathlib import Path

# Load log
run_log = json.loads(Path("../logs/run_1.json").read_text())

total_tasks = len(run_log)
correct_first = sum(1 for r in run_log if r["correct"])
correct_after_retry = sum(
    1 for r in run_log if r["correct"] or (r.get("retry") and r["retry"]["correct"])
)
solved_on_retry = sum(
    1 for r in run_log if not r["correct"] and r.get("retry") and r["retry"]["correct"]
)

metrics = {
    "total_tasks": total_tasks,
    "correct_on_first_try": correct_first,
    "correct_after_retry": correct_after_retry,
    "solved_by_optimization": solved_on_retry,
    "accuracy_before_retry": round(correct_first / total_tasks, 2),
    "final_accuracy": round(correct_after_retry / total_tasks, 2),
    "optimization_success_rate": round(solved_on_retry / (total_tasks - correct_first + 1e-5), 2)
}

# Save
Path("../evaluation").mkdir(exist_ok=True)
Path("../evaluation/metrics.json").write_text(json.dumps(metrics, indent=2))

print("✅ Metrics generated in evaluation/metrics.json")
