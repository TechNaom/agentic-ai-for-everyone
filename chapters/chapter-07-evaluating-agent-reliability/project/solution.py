"""
Chapter 7 Project (Chapter Mini-Project): An Eval Harness for TriageScout
Scenario: Emberlyn Underwriting, a fictional insurance claims office --
REFERENCE SOLUTION. See starter.py for the full scenario description.

How to run:
    python3 solution.py
Prints the structural self-check: 8/8.
"""

import math
import random
import statistics

CLAIMS = {
    "CLM-1": {"claim_id": "CLM-1", "fraud_flag": False, "missing_docs": False, "amount": 1200},
    "CLM-2": {"claim_id": "CLM-2", "fraud_flag": True, "missing_docs": False, "amount": 9000},
    "CLM-3": {"claim_id": "CLM-3", "fraud_flag": False, "missing_docs": True, "amount": 3400},
}

TASKS = [
    {"id": "T1", "claim_id": "CLM-1",
     "expected_trajectory": ["pull_claim_record", "check_fraud_flags", "calculate_payout_estimate"],
     "success_tools": {"calculate_payout_estimate"}},
    {"id": "T2", "claim_id": "CLM-2",
     "expected_trajectory": ["pull_claim_record", "check_fraud_flags", "escalate_to_senior_adjuster"],
     "success_tools": {"escalate_to_senior_adjuster"}},
    {"id": "T3", "claim_id": "CLM-3",
     "expected_trajectory": ["pull_claim_record", "check_fraud_flags", "request_supporting_documents"],
     "success_tools": {"request_supporting_documents"}},
]
TOOLS = ["pull_claim_record", "check_fraud_flags", "calculate_payout_estimate",
         "request_supporting_documents", "escalate_to_senior_adjuster"]

STEP_ERROR_RATE = 0.15


def task_success(trace, task):
    return "pull_claim_record" in trace and bool(set(trace) & task["success_tools"])


def trajectory_correctness(trace, expected):
    filtered = [t for t in trace if t in expected]
    collapsed = []
    for t in filtered:
        if not collapsed or collapsed[-1] != t:
            collapsed.append(t)
    return collapsed == expected


def simulate_agent_run(task, rng):
    trace = []
    for step in task["expected_trajectory"]:
        roll = rng.random()
        if roll < STEP_ERROR_RATE * 0.4:
            continue
        elif roll < STEP_ERROR_RATE * 0.7:
            distractor = rng.choice([t for t in TOOLS if t != step])
            trace.append(distractor)
            trace.append(step)
        else:
            trace.append(step)
    return trace


def run_harness(n_runs_per_task=20, seed=3):
    rng = random.Random(seed)
    results = {}
    for task in TASKS:
        successes = []
        traj_correct = []
        for _ in range(n_runs_per_task):
            trace = simulate_agent_run(task, rng)
            successes.append(task_success(trace, task))
            traj_correct.append(trajectory_correctness(trace, task["expected_trajectory"]))
        results[task["id"]] = {
            "task_success_rate": sum(successes) / len(successes),
            "trajectory_correctness_rate": sum(traj_correct) / len(traj_correct),
            "successes": successes,
        }
    return results


def pass_at_k(successes, k):
    n = len(successes)
    c = sum(successes)
    if n - c < k:
        return 1.0
    return 1.0 - (math.comb(n - c, k) / math.comb(n, k))


def self_check():
    results = []

    ok1a = task_success(["pull_claim_record", "check_fraud_flags", "calculate_payout_estimate"], TASKS[0]) is True
    ok1b = task_success(["check_fraud_flags", "calculate_payout_estimate"], TASKS[0]) is False
    results.append(("task_success is True with pull_claim_record + an ending tool present", ok1a))
    results.append(("task_success is False when pull_claim_record is missing", ok1b))

    exp = TASKS[0]["expected_trajectory"]
    ok2a = trajectory_correctness(["pull_claim_record", "check_fraud_flags", "calculate_payout_estimate"], exp) is True
    ok2b = trajectory_correctness(["check_fraud_flags", "pull_claim_record", "calculate_payout_estimate"], exp) is False
    results.append(("trajectory_correctness is True for the correct order", ok2a))
    results.append(("trajectory_correctness is False for a scrambled order", ok2b))

    harness_results = run_harness()
    ok3 = set(harness_results.keys()) == {"T1", "T2", "T3"}
    results.append(("run_harness returns results for all 3 tasks", ok3))

    ok4 = ok3 and all(0.0 <= harness_results[t]["task_success_rate"] <= 1.0 for t in harness_results)
    results.append(("run_harness task_success_rate values are valid rates in [0, 1]", ok4))

    ok5 = ok3 and all("successes" in harness_results[t] and len(harness_results[t]["successes"]) == 20 for t in harness_results)
    results.append(("run_harness includes a 20-entry raw successes list per task", ok5))

    ok6 = False
    if ok5:
        p1 = pass_at_k(harness_results["T1"]["successes"], 1)
        p3 = pass_at_k(harness_results["T1"]["successes"], 3)
        ok6 = p3 >= p1
        results.append((f"pass@3 >= pass@1 for T1 (pass@1={p1}, pass@3={p3})", ok6))
    else:
        results.append(("pass@3 >= pass@1 for T1 (skipped -- run_harness incomplete)", False))

    print("Chapter 7 Project -- Structural Self-Check")
    print("=" * 60)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 60)
    print(f"{passed}/{len(results)} checks passed")


if __name__ == "__main__":
    self_check()
