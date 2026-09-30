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
system you haven't seen before.

How to run:
    python3 starter.py
Prints a score report. Fill in each # TODO, re-run, and watch your
score climb toward the total (19 points across 7 tasks).
"""

WORKER_KEYWORDS = {
    "permitscout": {"permit", "building", "construction", "renovation"},
    "licensescout": {"license", "business", "vendor", "registration"},
    "zoningscout": {"zoning", "variance", "setback", "land"},
}


# ---------------------------------------------------------------------------
# Task 1: Map five CaseScout facts to the single BEST-matching
# multi-agent coordination concept from this list:
#   "failure isolation", "idempotent dispatch", "cross-agent attribution",
#   "content verification", "fail-closed routing"
#
# Fact A: One worker raises an exception mid-run, but the supervisor's
#         per-worker try/except boundary still returns the other two
#         workers' already-completed results.
# Fact B: A retry on a malformed dispatch response is checked against
#         a set of already-dispatched (subtask, worker) pairs before
#         being sent again, so it is never sent twice.
# Fact C: When a run produces a wrong final result, a function walks
#         the (agent, tool, ok) trace and reports which SPECIFIC
#         worker's step first failed, not just that something failed.
# Fact D: A worker returns a well-formed, confident-looking result,
#         but the city field doesn't match the city that was actually
#         requested -- caught only by checking the result's content.
# Fact E: A sub-task's keywords don't clearly match any worker's
#         domain, so the router returns None instead of guessing.
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
        "fact_a": "failure isolation",
        "fact_b": "idempotent dispatch",
        "fact_c": "cross-agent attribution",
        "fact_d": "content verification",
        "fact_e": "fail-closed routing",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Should a supervisor dispatch a sub-task to a worker whenever
# the router's best-scoring worker has a score of 0 (no keyword match
# at all)? Answer "YES" or "NO".
# ---------------------------------------------------------------------------
TASK_2_ANSWER = None  # TODO 6: "YES" or "NO"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# TODO 7 (production-gear): route_subtask -- a fail-closed keyword router.
# Tokenize the subtask (lowercase, strip periods, split on whitespace),
# score each worker by how many of its keywords appear in the subtask's
# words, and return the highest-scoring worker's name -- UNLESS the
# highest score is 0, in which case return None.
# ---------------------------------------------------------------------------
def route_subtask(subtask):
    # TODO 7: implement as described above.
    return "permitscout"


# ---------------------------------------------------------------------------
# TODO 8 (production-gear): verify_worker_result -- content verification.
# Return {"ok": False, "reason": ...} if result[expected_field] !=
# expected_value, else return {"ok": True}.
# ---------------------------------------------------------------------------
def verify_worker_result(result, expected_field, expected_value):
    # TODO 8: implement as described above.
    return {"ok": True}


# ---------------------------------------------------------------------------
# TODO 9 (production-gear): which_agent_responsible -- cross-agent
# trajectory attribution. trace is a list of (agent, tool, ok) tuples.
# Return the name of the FIRST agent whose step has ok == False, or
# None if every step passed.
# ---------------------------------------------------------------------------
def which_agent_responsible(trace):
    # TODO 9: implement as described above.
    return None


# ---------------------------------------------------------------------------
# TODO 10 (production-gear): classify_coordination_gap. Check, in this
# exact order, and return the first matching string:
#   "checks_tool_calls_before_trusting_dispatch" is False -> "no tool_calls check"
#   "routes_to_none_when_ambiguous" is False -> "no fail-closed routing"
#   "isolates_worker_failures" is False -> "no failure isolation"
#   "verifies_worker_content" is False -> "no content verification"
#   "dispatch_is_idempotent" is False -> "no idempotent dispatch"
#   otherwise -> "no known gap"
# ---------------------------------------------------------------------------
def classify_coordination_gap(setup):
    # TODO 10: implement as described above.
    return "no known gap"


# ---------------------------------------------------------------------------
# TODO 11 (production-gear): is_duplicate_dispatch -- idempotency check.
# dispatched is a set of (subtask, worker) tuples already sent. Return
# True if (subtask, worker) is already in dispatched, else False.
# ---------------------------------------------------------------------------
def is_duplicate_dispatch(dispatched, subtask, worker):
    # TODO 11: implement as described above.
    return False


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
