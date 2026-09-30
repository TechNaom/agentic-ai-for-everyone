"""
Chapter 8 Exercises: Cost and Latency Control of Agent Loops
Scenario: Brambleford Analytics, a fictional business-intelligence
office. Its query agent, InsightScout, can fetch a dataset, validate
its freshness, compute a summary, flag an anomaly, or escalate an
uncertain result to a human analyst.

This is a fresh scenario, deliberately different from the lesson's
Greywick Dispatch/FactScout hook. The point is applying this chapter's
cost/latency-control concepts (accounting, budgets, early exit, model
routing, caching, percentiles) to a system you haven't seen before.

How to run:
    python3 starter.py
Prints a score report. Fill in each # TODO, re-run, and watch your
score climb toward the total (19 points across 7 tasks).
"""

import math

EXPECTED_TRAJECTORY = ["fetch_dataset", "validate_freshness", "compute_summary"]
TOOLS = ["fetch_dataset", "validate_freshness", "compute_summary", "flag_anomaly", "escalate_to_analyst"]

MODEL_RATES = {
    "cheap": {"in": 0.05, "out": 0.15},
    "strong": {"in": 1.00, "out": 3.00},
}


# ---------------------------------------------------------------------------
# Task 1: Map five InsightScout facts to the single BEST-matching
# cost/latency-control concept from this list:
#   "model routing", "caching", "early termination", "fail-closed budget",
#   "latency percentile"
#
# Fact A: After a cache is added, a repeat query for the same dataset
#         returns instantly with zero new cost or model call.
# Fact B: A loop stops the moment its output already satisfies the
#         task's success condition, even though more steps remain
#         available in its trajectory.
# Fact C: A team finds that 1 in 20 requests takes more than 3x as
#         long as the typical request -- a fact invisible from the
#         average latency alone.
# Fact D: A dispatcher sends simple validation lookups to a smaller
#         model and reserves a larger model for anomaly analysis.
# Fact E: Once a run's running cost crosses a configured dollar
#         ceiling, every subsequent step is denied rather than merely
#         logged.
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
        "fact_a": "caching",
        "fact_b": "early termination",
        "fact_c": "latency percentile",
        "fact_d": "model routing",
        "fact_e": "fail-closed budget",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Dependency/staleness reasoning.
# ---------------------------------------------------------------------------
# A cache with no invalidation is used to store validate_freshness's
# result for a dataset whose actual freshness changes hourly. Does the
# cache remain SAFE indefinitely (i.e., will it keep returning a
# correct freshness verdict forever, with no added risk): YES or NO?

TASK_2_ANSWER = None  # TODO 6: "YES" | "NO"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): per-step token/cost accounting.
# ---------------------------------------------------------------------------
def step_cost(tokens_in, tokens_out, model="cheap"):
    """
    Look up MODEL_RATES[model], a dict with "in" and "out" keys (dollars
    per 1000 tokens). Return round((tokens_in / 1000) * rate_in +
    (tokens_out / 1000) * rate_out, 6).
    """
    # TODO 7: implement as described above.
    return 0.0


# ---------------------------------------------------------------------------
# Task 4 (production-gear): fail-closed budget check.
# ---------------------------------------------------------------------------
def is_within_budget(steps_used, cost_used, max_steps, max_cost):
    """
    Return True only if steps_used <= max_steps AND cost_used <=
    max_cost. Return False if EITHER cap is exceeded (fail-closed: any
    single exceeded cap denies the step).
    """
    # TODO 8: implement as described above.
    return True


# ---------------------------------------------------------------------------
# Task 5 (production-gear): latency percentile.
# ---------------------------------------------------------------------------
def percentile(values, p):
    """
    Standard linear-interpolation percentile. Sort values. Compute
    k = (len(sorted) - 1) * (p / 100). Let f = floor(k), c = ceil(k).
    If f == c, return sorted[int(k)]. Otherwise return
    sorted[f] + (sorted[c] - sorted[f]) * (k - f). Return None for an
    empty list.
    """
    # TODO 9: implement as described above.
    return None


# ---------------------------------------------------------------------------
# Task 6 (production-gear): diagnose a cost-control-maturity gap.
# ---------------------------------------------------------------------------
def classify_cost_control_gap(setup):
    """
    Given a dict with boolean keys "tracks_per_step_cost",
    "has_hard_budget", "has_early_exit", "has_model_routing",
    "has_caching":
    - if tracks_per_step_cost is False: return "no per-step accounting"
    - elif has_hard_budget is False: return "no fail-closed budget"
    - elif has_early_exit is False: return "no early termination"
    - elif has_model_routing is False: return "no model routing"
    - elif has_caching is False: return "no caching"
    - else: return "no known gap"
    """
    # TODO 10: implement the branching logic described above.
    return "no known gap"


# ---------------------------------------------------------------------------
# Task 7 (production-gear): cache hit rate.
# ---------------------------------------------------------------------------
def cache_hit_rate(hits, misses):
    """
    Return round(hits / (hits + misses), 4). If hits + misses == 0,
    return None.
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
    results.append((f"Task 2: staleness/dependency reasoning ({s2}/{t2})", s2 == t2))

    # Task 3 (3 points)
    c1 = step_cost(20, 30, "strong")
    c2 = step_cost(20, 3, "cheap")
    ok3 = abs(c1 - 0.11) < 0.0001 and abs(c2 - 0.00145) < 0.00001
    results.append((f"Task 3: step_cost (strong={c1}, cheap={c2}, expect 0.11 and 0.00145)", ok3))
    if ok3:
        score += 3
    total += 3

    # Task 4 (3 points)
    b1 = is_within_budget(2, 0.005, 3, 0.01)
    b2 = is_within_budget(4, 0.005, 3, 0.01)
    b3 = is_within_budget(2, 0.02, 3, 0.01)
    ok4 = b1 is True and b2 is False and b3 is False
    results.append(("Task 4: is_within_budget (True only when BOTH steps and cost are within cap)", ok4))
    if ok4:
        score += 3
    total += 3

    # Task 5 (3 points)
    latencies = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    p50 = percentile(latencies, 50)
    p95 = percentile(latencies, 95)
    ok5 = p50 is not None and p95 is not None and abs(p50 - 0.75) < 0.001 and abs(p95 - 1.155) < 0.001
    results.append((f"Task 5: percentile (p50={p50}, p95={p95}, expect 0.75 and 1.155)", ok5))
    if ok5:
        score += 3
    total += 3

    # Task 6 (2 points)
    d1 = classify_cost_control_gap({"tracks_per_step_cost": False})
    d2 = classify_cost_control_gap({"tracks_per_step_cost": True, "has_hard_budget": False})
    d3 = classify_cost_control_gap({"tracks_per_step_cost": True, "has_hard_budget": True, "has_early_exit": True, "has_model_routing": True, "has_caching": True})
    ok6 = d1 == "no per-step accounting" and d2 == "no fail-closed budget" and d3 == "no known gap"
    results.append(("Task 6: classify_cost_control_gap classifies all three cases correctly", ok6))
    if ok6:
        score += 2
    total += 2

    # Task 7 (2 points)
    hr = cache_hit_rate(15, 5)
    ok7 = hr is not None and abs(hr - 0.75) < 0.0001
    results.append((f"Task 7: cache_hit_rate(15, 5) == 0.75 (got {hr})", ok7))
    if ok7:
        score += 2
    total += 2

    print("Chapter 8 Exercises -- Structural Self-Check")
    print("=" * 70)
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("=" * 70)
    print(f"Score: {score}/{total}")


if __name__ == "__main__":
    self_check()
