"""
Chapter 9 Exercises: Multi-Agent Orchestration Patterns
Scenario: Hadleigh Civic Records Bureau, a fictional municipal records
office. Its supervisor agent, CaseScout, decomposes an incoming case
request and dispatches sub-tasks to three specialist workers:
PermitScout (building permits), LicenseScout (business licenses), and
ZoningScout (zoning/variance questions).

This is a fresh scenario, deliberately different from the lesson's
Quillmark Journeys/TripScout hook. The point is applying this
chapter's supervisor/worker concepts (dispatch, routing, failure
isolation, verification, idempotency, cross-agent attribution) to a
system you haven't seen before -- REFERENCE SOLUTION.

How to run:
    python3 solution.py
Prints a score report. Scores 19/19.
"""

WORKER_KEYWORDS = {
    "permitscout": {"permit", "building", "construction", "renovation"},
    "licensescout": {"license", "business", "vendor", "registration"},
    "zoningscout": {"zoning", "variance", "setback", "land"},
}


# ---------------------------------------------------------------------------
# Task 1: Map five CaseScout facts to the single BEST-matching
# multi-agent coordination concept.
# ---------------------------------------------------------------------------
TASK_1_ANSWERS = {
    "fact_a": "failure isolation",
    "fact_b": "idempotent dispatch",
    "fact_c": "cross-agent attribution",
    "fact_d": "content verification",
    "fact_e": "fail-closed routing",
}


def score_exercise_1():
    correct = {
        "fact_a": "failure isolation",
        "fact_b": "idempotent dispatch",
        "fact_c": "cross-agent attribution",
        "fact_d": "content verification",
        "fact_e": "fail-closed routing",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Routing/reasoning question.
# ---------------------------------------------------------------------------
TASK_2_ANSWER = "NO"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): route_subtask -- a fail-closed keyword router.
# ---------------------------------------------------------------------------
def route_subtask(subtask):
    words = set(subtask.lower().replace(".", "").split())
    scores = {w: len(words & kws) for w, kws in WORKER_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return None
    return best


# ---------------------------------------------------------------------------
# Task 4 (production-gear): verify_worker_result -- content verification,
# not just shape-checking.
# ---------------------------------------------------------------------------
def verify_worker_result(result, expected_field, expected_value):
    if result.get(expected_field) != expected_value:
        return {"ok": False,
                "reason": f"expected {expected_field}={expected_value!r}, got {result.get(expected_field)!r}"}
    return {"ok": True}


# ---------------------------------------------------------------------------
# Task 5 (production-gear): which_agent_responsible -- cross-agent
# trajectory attribution.
# ---------------------------------------------------------------------------
def which_agent_responsible(trace):
    for agent, tool, ok in trace:
        if not ok:
            return agent
    return None


# ---------------------------------------------------------------------------
# Task 6 (production-gear): classify_coordination_gap.
# ---------------------------------------------------------------------------
def classify_coordination_gap(setup):
    if setup.get("checks_tool_calls_before_trusting_dispatch") is False:
        return "no tool_calls check"
    if setup.get("routes_to_none_when_ambiguous") is False:
        return "no fail-closed routing"
    if setup.get("isolates_worker_failures") is False:
        return "no failure isolation"
    if setup.get("verifies_worker_content") is False:
        return "no content verification"
    if setup.get("dispatch_is_idempotent") is False:
        return "no idempotent dispatch"
    return "no known gap"


# ---------------------------------------------------------------------------
# Task 7 (production-gear): is_duplicate_dispatch -- idempotency check.
# ---------------------------------------------------------------------------
def is_duplicate_dispatch(dispatched, subtask, worker):
    return (subtask, worker) in dispatched


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
    results.append((f"Task 2: fail-closed routing reasoning ({s2}/{t2})", s2 == t2))

    r1 = route_subtask("I need a building permit for a renovation.")
    r2 = route_subtask("I'd like to talk about my property, please.")
    ok3 = r1 == "permitscout" and r2 is None
    results.append((f"Task 3: route_subtask (permit='{r1}', ambiguous='{r2}', expect 'permitscout' and None)", ok3))
    if ok3:
        score += 3
    total += 3

    v1 = verify_worker_result({"worker": "licensescout", "city": "Hadleigh"}, "city", "Hadleigh")
    v2 = verify_worker_result({"worker": "licensescout", "city": "Wrong Town"}, "city", "Hadleigh")
    ok4 = v1["ok"] is True and v2["ok"] is False
    results.append(("Task 4: verify_worker_result catches a mismatched field", ok4))
    if ok4:
        score += 3
    total += 3

    t_fail = [("permitscout", "x", True), ("zoningscout", "y", False), ("licensescout", "z", True)]
    t_pass = [("permitscout", "x", True), ("licensescout", "z", True)]
    w1 = which_agent_responsible(t_fail)
    w2 = which_agent_responsible(t_pass)
    ok5 = w1 == "zoningscout" and w2 is None
    results.append((f"Task 5: which_agent_responsible (fail='{w1}', pass='{w2}', expect 'zoningscout' and None)", ok5))
    if ok5:
        score += 3
    total += 3

    d1 = classify_coordination_gap({"checks_tool_calls_before_trusting_dispatch": False})
    d2 = classify_coordination_gap({"checks_tool_calls_before_trusting_dispatch": True, "routes_to_none_when_ambiguous": False})
    d3 = classify_coordination_gap({"checks_tool_calls_before_trusting_dispatch": True, "routes_to_none_when_ambiguous": True,
                                     "isolates_worker_failures": True, "verifies_worker_content": True, "dispatch_is_idempotent": True})
    ok6 = d1 == "no tool_calls check" and d2 == "no fail-closed routing" and d3 == "no known gap"
    results.append(("Task 6: classify_coordination_gap classifies all three cases correctly", ok6))
    if ok6:
        score += 2
    total += 2

    dispatched = {("find permit", "permitscout")}
    dup = is_duplicate_dispatch(dispatched, "find permit", "permitscout")
    new = is_duplicate_dispatch(dispatched, "find license", "licensescout")
    ok7 = dup is True and new is False
    results.append(("Task 7: is_duplicate_dispatch distinguishes a repeat from a new sub-task", ok7))
    if ok7:
        score += 2
    total += 2

    print("Chapter 9 Exercises -- Structural Self-Check")
    print("=" * 70)
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("=" * 70)
    print(f"Score: {score}/{total}")


if __name__ == "__main__":
    self_check()
