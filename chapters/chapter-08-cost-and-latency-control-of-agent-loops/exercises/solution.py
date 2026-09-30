"""
Chapter 8 Exercises: Cost and Latency Control of Agent Loops
Scenario: Brambleford Analytics, a fictional business-intelligence
office. Its query agent, InsightScout, can fetch a dataset, validate
its freshness, compute a summary, flag an anomaly, or escalate an
uncertain result to a human analyst.

This is a fresh scenario, deliberately different from the lesson's
Greywick Dispatch/FactScout hook. The point is applying this chapter's
cost/latency-control concepts (accounting, budgets, early exit, model
routing, caching, percentiles) to a system you haven't seen before --
REFERENCE SOLUTION.

How to run:
    python3 solution.py
Prints a score report. Scores 19/19.
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
# cost/latency-control concept.
# ---------------------------------------------------------------------------
TASK_1_ANSWERS = {
    "fact_a": "caching",
    "fact_b": "early termination",
    "fact_c": "latency percentile",
    "fact_d": "model routing",
    "fact_e": "fail-closed budget",
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
TASK_2_ANSWER = "NO"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): per-step token/cost accounting.
# ---------------------------------------------------------------------------
def step_cost(tokens_in, tokens_out, model="cheap"):
    rates = MODEL_RATES[model]
    return round((tokens_in / 1000) * rates["in"] + (tokens_out / 1000) * rates["out"], 6)


# ---------------------------------------------------------------------------
# Task 4 (production-gear): fail-closed budget check.
# ---------------------------------------------------------------------------
def is_within_budget(steps_used, cost_used, max_steps, max_cost):
    return steps_used <= max_steps and cost_used <= max_cost


# ---------------------------------------------------------------------------
# Task 5 (production-gear): latency percentile.
# ---------------------------------------------------------------------------
def percentile(values, p):
    if not values:
        return None
    s = sorted(values)
    k = (len(s) - 1) * (p / 100)
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return s[int(k)]
    return s[f] + (s[c] - s[f]) * (k - f)


# ---------------------------------------------------------------------------
# Task 6 (production-gear): diagnose a cost-control-maturity gap.
# ---------------------------------------------------------------------------
def classify_cost_control_gap(setup):
    if setup.get("tracks_per_step_cost") is False:
        return "no per-step accounting"
    if setup.get("has_hard_budget") is False:
        return "no fail-closed budget"
    if setup.get("has_early_exit") is False:
        return "no early termination"
    if setup.get("has_model_routing") is False:
        return "no model routing"
    if setup.get("has_caching") is False:
        return "no caching"
    return "no known gap"


# ---------------------------------------------------------------------------
# Task 7 (production-gear): cache hit rate.
# ---------------------------------------------------------------------------
def cache_hit_rate(hits, misses):
    total = hits + misses
    if total == 0:
        return None
    return round(hits / total, 4)


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
    results.append((f"Task 2: staleness/dependency reasoning ({s2}/{t2})", s2 == t2))

    c1 = step_cost(20, 30, "strong")
    c2 = step_cost(20, 3, "cheap")
    ok3 = abs(c1 - 0.11) < 0.0001 and abs(c2 - 0.00145) < 0.00001
    results.append((f"Task 3: step_cost (strong={c1}, cheap={c2}, expect 0.11 and 0.00145)", ok3))
    if ok3:
        score += 3
    total += 3

    b1 = is_within_budget(2, 0.005, 3, 0.01)
    b2 = is_within_budget(4, 0.005, 3, 0.01)
    b3 = is_within_budget(2, 0.02, 3, 0.01)
    ok4 = b1 is True and b2 is False and b3 is False
    results.append(("Task 4: is_within_budget (True only when BOTH steps and cost are within cap)", ok4))
    if ok4:
        score += 3
    total += 3

    latencies = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    p50 = percentile(latencies, 50)
    p95 = percentile(latencies, 95)
    ok5 = abs(p50 - 0.75) < 0.001 and abs(p95 - 1.155) < 0.001
    results.append((f"Task 5: percentile (p50={p50}, p95={p95}, expect 0.75 and 1.155)", ok5))
    if ok5:
        score += 3
    total += 3

    d1 = classify_cost_control_gap({"tracks_per_step_cost": False})
    d2 = classify_cost_control_gap({"tracks_per_step_cost": True, "has_hard_budget": False})
    d3 = classify_cost_control_gap({"tracks_per_step_cost": True, "has_hard_budget": True, "has_early_exit": True, "has_model_routing": True, "has_caching": True})
    ok6 = d1 == "no per-step accounting" and d2 == "no fail-closed budget" and d3 == "no known gap"
    results.append(("Task 6: classify_cost_control_gap classifies all three cases correctly", ok6))
    if ok6:
        score += 2
    total += 2

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
