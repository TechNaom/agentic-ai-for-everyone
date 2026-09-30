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
before.

How to run:
    python3 starter.py
It prints a score report. Fill in each # TODO, re-run, and watch your
score climb toward the total (19 points across 7 tasks).
"""

import math

EXPECTED_TRAJECTORY = ["search_registry", "check_record_authenticity", "cross_reference_deed", "generate_report"]
TOOLS = ["search_registry", "check_record_authenticity", "cross_reference_deed", "generate_report", "escalate_to_archivist"]


# ---------------------------------------------------------------------------
# Task 1: Map five RecordScout facts to the single BEST-matching eval
# concept from this list:
#   "task success", "trajectory correctness", "pass@k", "cost-per-success",
#   "multi-turn drift"
#
# Fact A: Across 20 identical repeated runs of the same record lookup, a
#         team computes the probability that at least one of any 3 randomly
#         chosen runs would have succeeded.
# Fact B: A run reaches a generated report at the end, but it got there by
#         calling cross_reference_deed BEFORE check_record_authenticity,
#         out of the expected order.
# Fact C: A team divides total spend across a batch of runs by the number
#         of runs that actually produced a usable report, not by the total
#         number of runs attempted.
# Fact D: A long research session's trajectory correctness measurably drops
#         in its later turns compared to its early turns.
# Fact E: A run's trace contains generate_report and search_registry
#         somewhere in it, regardless of what order they appeared in or
#         what else happened in between.
# ---------------------------------------------------------------------------

TASK_1_ANSWERS = {
    "fact_a": None,  # TODO 1
    "fact_b": None,  # TODO 2
    "fact_c": None,  # TODO 3
    "fact_d": None,  # TODO 4
    "fact_e": None,  # TODO 5
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
# A task-success check only verifies that generate_report and
# search_registry both appear somewhere in the trace. If the content
# generate_report produces is factually wrong (e.g. names the wrong deed
# owner) but every expected tool still fired, does task success catch that
# content error: YES or NO?

TASK_2_ANSWER = None  # TODO 6: "YES" | "NO"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): trajectory correctness for RecordScout.
# ---------------------------------------------------------------------------
def trajectory_correctness(trace, expected):
    """
    trace is a list of tool-name strings (already extracted from a
    tool_trace). Filter trace down to only names present in `expected`,
    collapse consecutive duplicates, then compare for exact equality
    against `expected`. Return True/False.
    """
    # TODO 7: implement as described above.
    return False


# ---------------------------------------------------------------------------
# Task 4 (production-gear): task success for RecordScout.
# ---------------------------------------------------------------------------
def task_success(trace):
    """
    Return True if BOTH "search_registry" and "generate_report" appear
    anywhere in trace (a list of tool-name strings), regardless of order
    or what else is in the trace. Otherwise return False.
    """
    # TODO 8: implement as described above.
    return False


# ---------------------------------------------------------------------------
# Task 5 (production-gear): pass@k.
# ---------------------------------------------------------------------------
def pass_at_k(successes, k):
    """
    successes is a list of True/False. n = len(successes), c = number of
    True values. If n - c < k, return 1.0. Otherwise return
    1.0 - C(n-c, k) / C(n, k), using math.comb.
    """
    # TODO 9: implement the unbiased pass@k estimator described above.
    return 0.0


# ---------------------------------------------------------------------------
# Task 6 (production-gear): diagnose an eval-maturity gap from a setup dict.
# ---------------------------------------------------------------------------
def diagnose_eval_gap(setup):
    """
    Given a dict with boolean keys "has_task_success_metric",
    "has_trajectory_metric", "multiple_runs_per_task", "tracks_cost":
    - if has_task_success_metric is False: return "no measurement"
    - elif has_trajectory_metric is False: return "task success only"
    - elif multiple_runs_per_task is False: return "single-run only"
    - elif tracks_cost is False: return "no cost tracking"
    - else: return "no known gap"
    """
    # TODO 10: implement the branching logic described above.
    return "no known gap"


# ---------------------------------------------------------------------------
# Task 7 (production-gear): cost-per-success.
# ---------------------------------------------------------------------------
def cost_per_success(n_runs, success_rate, cost_per_run):
    """
    Compute the number of successes as round(n_runs * success_rate).
    If successes is 0, return None. Otherwise return
    round((n_runs * cost_per_run) / successes, 5).
    """
    # TODO 11: implement as described above.
    return None


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
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

    # Task 3 (3 points)
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

    # Task 4 (3 points)
    ts1 = task_success(["search_registry", "check_record_authenticity", "generate_report"])
    ts2 = task_success(["check_record_authenticity", "cross_reference_deed"])
    ok4 = ts1 is True and ts2 is False
    results.append(("Task 4: task_success (True when both tools present, False otherwise)", ok4))
    if ok4:
        score += 3
    total += 3

    # Task 5 (3 points)
    successes = [True] * 18 + [False] * 2
    p1 = pass_at_k(successes, 1)
    p3 = pass_at_k(successes, 3)
    ok5 = abs(p1 - 0.9) < 0.001 and abs(p3 - 1.0) < 0.001
    results.append((f"Task 5: pass_at_k (pass@1={p1}, pass@3={p3}, expect 0.9 and 1.0)", ok5))
    if ok5:
        score += 3
    total += 3

    # Task 6 (2 points)
    d1 = diagnose_eval_gap({"has_task_success_metric": False})
    d2 = diagnose_eval_gap({"has_task_success_metric": True, "has_trajectory_metric": False})
    d3 = diagnose_eval_gap({"has_task_success_metric": True, "has_trajectory_metric": True, "multiple_runs_per_task": True, "tracks_cost": True})
    ok6 = d1 == "no measurement" and d2 == "task success only" and d3 == "no known gap"
    results.append(("Task 6: diagnose_eval_gap classifies all three cases correctly", ok6))
    if ok6:
        score += 2
    total += 2

    # Task 7 (2 points)
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
