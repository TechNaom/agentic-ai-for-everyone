"""
Chapter 9 Project (Chapter Mini-Project): A Supervisor Harness for
CityScout. Scenario: Ashgrove Municipal Services, a fictional
municipal building-services office, wants CityScout built the same
way the lesson's TripScout was coordinated -- a fresh scenario you
build yourself, combining this chapter's three pillars (fail-closed
routing, per-worker failure isolation, and an idempotent supervisor
harness that attributes failure to a specific agent) into one real,
reusable coordination layer.

CityScout dispatches building-related requests to two workers:
  - inspectionscout: site/safety/structural/fire inspections.
  - zonescout: zoning/variance/setback questions.

This is a chapter mini-project, NOT the course's L3 Independent
project (which the project ladder still owes the repo -- deferred past
Chapter 8, not yet built as of this chapter, and NOT built this
chapter either; see PROJECT_STATE.md). It is gradable offline with a
deterministic seeded simulation (no live model call needed), matching
this chapter's own lesson harness and this course's project grading
policy from Chapters 2-3, 7-8.

How to run:
    python3 starter.py
It prints a structural self-check: 9 checks across routing, failure
isolation, and the aggregate supervisor harness.
"""

import random

WORKER_KEYWORDS = {
    "inspectionscout": {"inspect", "inspection", "site", "safety", "structural", "fire"},
    "zonescout": {"zoning", "variance", "setback", "zone"},
}

CASES = [
    {"id": "C1", "subtasks": [
        "Inspect the site for structural issues.",
        "Check the zoning variance for the setback.",
    ]},
    {"id": "C2", "subtasks": [
        "Inspect for fire safety compliance.",
    ]},
    {"id": "C3", "subtasks": [
        "Verify the zoning setback distance.",
        "Verify the zoning setback distance.",   # deliberate duplicate
    ]},
    {"id": "C4", "subtasks": [
        "I have a general question about my property.",   # deliberately unroutable
    ]},
]


# ---------------------------------------------------------------------------
# Given -- the two worker functions and their dispatch table. No need
# to edit either of these. Each has a 20% chance of raising, matching
# this chapter's own disclosed, illustrative error rate.
# ---------------------------------------------------------------------------
def inspectionscout_worker(subtask, rng):
    if rng.random() < 0.2:
        raise RuntimeError("inspectionscout could not reach the site record")
    return f"inspected: {subtask}"


def zonescout_worker(subtask, rng):
    if rng.random() < 0.2:
        raise RuntimeError("zonescout could not verify the parcel record")
    return f"zoned: {subtask}"


WORKER_FNS = {"inspectionscout": inspectionscout_worker, "zonescout": zonescout_worker}


# ---------------------------------------------------------------------------
# TODO 1: route_subtask -- a fail-closed keyword router.
# ---------------------------------------------------------------------------
def route_subtask(subtask):
    """
    Tokenize subtask (lowercase, strip periods, split on whitespace).
    Score each worker in WORKER_KEYWORDS by how many of its keywords
    appear in the subtask's words. Return the highest-scoring worker's
    name -- UNLESS the highest score is 0, in which case return None
    (fail-closed: never guess a worker for an unroutable subtask).
    """
    # TODO 1: implement as described above.
    return "inspectionscout"


# ---------------------------------------------------------------------------
# TODO 2: dispatch_isolated -- a per-worker failure isolation boundary.
# ---------------------------------------------------------------------------
def dispatch_isolated(worker_fn, subtask, rng):
    """
    Call worker_fn(subtask, rng) inside a try/except. On success,
    return {"ok": True, "result": <worker_fn's return value>}. On any
    Exception, return {"ok": False, "error": str(exception)} -- the
    caller must NEVER see the worker's own exception propagate.
    """
    # TODO 2: implement as described above.
    return {"ok": True, "result": None}


# ---------------------------------------------------------------------------
# Given -- cross-agent attribution, reused from the lesson's own
# pattern. No need to edit.
# ---------------------------------------------------------------------------
def which_agent_responsible(trace):
    for agent, tool, ok in trace:
        if not ok:
            return agent
    return None


# ---------------------------------------------------------------------------
# TODO 3: run_city_scout_harness -- the assembled supervisor harness.
# ---------------------------------------------------------------------------
def run_city_scout_harness(cases=CASES, seed=11):
    """
    For each case in `cases`: create an empty `dispatched` set (for
    idempotency) and an empty `trace` list. For each subtask in
    case["subtasks"]:
      1. Route it with route_subtask(subtask). If the result is None,
         append ("unrouted", subtask, False) to trace and continue to
         the next subtask (do NOT dispatch).
      2. Otherwise, build key = (subtask, worker). If key is already
         in `dispatched`, SKIP this subtask entirely (idempotent skip
         -- do not append anything to trace, do not call the worker
         again).
      3. Otherwise, add key to `dispatched`, call
         dispatch_isolated(WORKER_FNS[worker], subtask, rng), and
         append (worker, subtask, outcome["ok"]) to trace.
    After walking all of a case's subtasks, compute:
      - success_rate: (number of trace entries with ok==True) divided
        by (total trace entries), or 0.0 if trace is empty.
      - first_failed_agent: which_agent_responsible(trace).
    Return a dict keyed by case id:
        {case_id: {"trace": [...], "success_rate": float,
                    "first_failed_agent": str or None}}
    Use a single shared rng = random.Random(seed) across ALL cases and
    subtasks, in the order they're walked (not a fresh Random per case).
    """
    # TODO 3: implement as described above.
    return {}


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

def self_check():
    results = []

    r1 = route_subtask("Inspect the site for structural issues.")
    r2 = route_subtask("I have a general question about my property.")
    results.append(("route_subtask routes a clear inspection request to inspectionscout", r1 == "inspectionscout"))
    results.append(("route_subtask returns None for an unroutable request (fail-closed)", r2 is None))

    iso_ok = dispatch_isolated(lambda st, rng: "fine", "x", random.Random(1))
    def boom(st, rng):
        raise ValueError("boom")
    iso_bad = dispatch_isolated(boom, "x", random.Random(1))
    results.append(("dispatch_isolated returns ok=True on a normal call", iso_ok["ok"] is True))
    results.append(("dispatch_isolated catches an exception and returns ok=False, no crash", iso_bad["ok"] is False))

    harness = run_city_scout_harness()
    results.append(("run_city_scout_harness returns results for all 4 cases", set(harness.keys()) == {"C1", "C2", "C3", "C4"}))
    results.append(("C1 (two distinct routable subtasks) has 2 trace entries", len(harness.get("C1", {}).get("trace", [])) == 2))
    results.append(("C3's duplicate subtask is skipped via idempotent dispatch (1 trace entry, not 2)", len(harness.get("C3", {}).get("trace", [])) == 1))
    results.append(("C4's unroutable subtask is attributed to 'unrouted', not silently dropped", harness.get("C4", {}).get("first_failed_agent") == "unrouted"))
    results.append(("every case's success_rate is a valid rate in [0, 1]", all(0.0 <= harness[c]["success_rate"] <= 1.0 for c in harness) if harness else False))

    print("Chapter 9 Project -- Structural Self-Check")
    print("=" * 60)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 60)
    print(f"{passed}/{len(results)} checks passed")


if __name__ == "__main__":
    self_check()
