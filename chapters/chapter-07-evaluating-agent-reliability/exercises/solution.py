"""
Chapter 7 Exercises: Evaluating Agent Reliability
Scenario: Larkmoor Archive Service, a fictional historical-records
office. Its research agent, RecordScout, can search a property
registry, check a record's authenticity, cross-reference a deed
against the registry, generate a research report, or escalate an
uncertain record to a human archivist.

This is a fresh scenario, deliberately different from the lesson's
Greywick Dispatch/FactScout hook. The point is applying this chapter's
eval concepts (task success, trajectory correctness, pass@k,
cost-per-success, multi-turn drift) to a system you haven't seen
before -- REFERENCE SOLUTION.

How to run:
    python3 solution.py
It prints a score report. Scores 19/19.
"""

import math

EXPECTED_TRAJECTORY = ["search_registry", "check_record_authenticity", "cross_reference_deed", "generate_report"]
TOOLS = ["search_registry", "check_record_authenticity", "cross_reference_deed", "generate_report", "escalate_to_archivist"]


# ---------------------------------------------------------------------------
# Task 1: Map five RecordScout facts to the eval concept each is about.
# ---------------------------------------------------------------------------
TASK_1_ANSWERS = {
    "fact_a": "pass@k",
    "fact_b": "trajectory correctness",
    "fact_c": "cost-per-success",
    "fact_d": "multi-turn drift",
    "fact_e": "task success",
}


def score_exercise_1():
    correct = {
        "fact_a": "pass@k",
        "fact_b": "trajectory correctness",
        "fact_c": "cost-per-success",
        "fact_d": "multi-turn drift",
        "fact_e": "task success",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Dependency reasoning.
# ---------------------------------------------------------------------------
TASK_2_ANSWER = "NO"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): trajectory correctness for RecordScout.
# ---------------------------------------------------------------------------
def trajectory_correctness(trace, expected):
    filtered = [t for t in trace if t in expected]
    collapsed = []
    for t in filtered:
        if not collapsed or collapsed[-1] != t:
            collapsed.append(t)
    return collapsed == expected


# ---------------------------------------------------------------------------
# Task 4 (production-gear): task success for RecordScout.
# ---------------------------------------------------------------------------
def task_success(trace):
    return "search_registry" in trace and "generate_report" in trace


# ---------------------------------------------------------------------------
# Task 5 (production-gear): pass@k.
# ---------------------------------------------------------------------------
def pass_at_k(successes, k):
    n = len(successes)
    c = sum(successes)
    if n - c < k:
        return 1.0
    return 1.0 - (math.comb(n - c, k) / math.comb(n, k))


# ---------------------------------------------------------------------------
# Task 6 (production-gear): diagnose an eval-maturity gap from a setup dict.
# ---------------------------------------------------------------------------
def diagnose_eval_gap(setup):
    if setup.get("has_task_success_metric") is False:
        return "no measurement"
    if setup.get("has_trajectory_metric") is False:
        return "task success only"
    if setup.get("multiple_runs_per_task") is False:
        return "single-run only"
    if setup.get("tracks_cost") is False:
        return "no cost tracking"
    return "no known gap"


# ---------------------------------------------------------------------------
# Task 7 (production-gear): cost-per-success.
# ---------------------------------------------------------------------------
def cost_per_success(n_runs, success_rate, cost_per_run):
    successes = round(n_runs * success_rate)
    if successes == 0:
        return None
    return round((n_runs * cost_per_run) / successes, 5)


# ---------------------------------------------------------------------------
# Structural self-check (identical to starter.py)
# ---------------------------------------------------------------------------

def self_check():
    results = []
    score = 0
    total = 0

    s1, t1 = score_exercise_1()
    score += s1; total += t1
    results.append((f"Task 1: fact-to-concept mapping ({s1}/{t1})", s1 == t1))

    s2, t2 = score_exercise_2()
    score += s2; total += t2
    results.append((f"Task 2: dependency reasoning ({s2}/{t2})", s2 == t2))

    tc1 = trajectory_correctness(
        ["search_registry", "check_record_authenticity", "cross_reference_deed", "generate_report"],
        EXPECTED_TRAJECTORY,
    )
    tc2 = trajectory_correctness(
        ["search_registry", "cross_reference_deed", "check_record_authenticity", "generate_report"],
        EXPECTED_TRAJECTORY,
    )
    ok3 = tc1 is True and tc2 is False
    results.append(("Task 3: trajectory_correctness (correct-order True, wrong-order False)", ok3))
    if ok3:
        score += 3
    total += 3

    ts1 = task_success(["search_registry", "check_record_authenticity", "generate_report"])
    ts2 = task_success(["check_record_authenticity", "cross_reference_deed"])
    ok4 = ts1 is True and ts2 is False
    results.append(("Task 4: task_success (True when both tools present, False otherwise)", ok4))
    if ok4:
        score += 3
    total += 3

    successes = [True] * 18 + [False] * 2
    p1 = pass_at_k(successes, 1)
    p3 = pass_at_k(successes, 3)
    ok5 = abs(p1 - 0.9) < 0.001 and abs(p3 - 1.0) < 0.001
    results.append((f"Task 5: pass_at_k (pass@1={p1}, pass@3={p3}, expect 0.9 and 1.0)", ok5))
    if ok5:
        score += 3
    total += 3

    d1 = diagnose_eval_gap({"has_task_success_metric": False})
    d2 = diagnose_eval_gap({"has_task_success_metric": True, "has_trajectory_metric": False})
    d3 = diagnose_eval_gap({"has_task_success_metric": True, "has_trajectory_metric": True, "multiple_runs_per_task": True, "tracks_cost": True})
    ok6 = d1 == "no measurement" and d2 == "task success only" and d3 == "no known gap"
    results.append(("Task 6: diagnose_eval_gap classifies all three cases correctly", ok6))
    if ok6:
        score += 2
    total += 2

    cps = cost_per_success(20, 0.8, 0.002)
    ok7 = cps is not None and abs(cps - 0.0025) < 0.0001
    results.append((f"Task 7: cost_per_success(20, 0.8, 0.002) == 0.0025 (got {cps})", ok7))
    if ok7:
        score += 2
    total += 2

    print("Chapter 7 Exercises -- Structural Self-Check")
    print("=" * 70)
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("=" * 70)
    print(f"Score: {score}/{total}")


if __name__ == "__main__":
    self_check()
