"""
Chapter 9 Project (Chapter Mini-Project): A Supervisor Harness for
CityScout. Scenario: Ashgrove Municipal Services, a fictional
municipal building-services office -- REFERENCE SOLUTION. See
starter.py for the full scenario description.

Not the L3 Independent project (which the course's project ladder
still owes the repo, per PROJECT_STATE.md -- deferred past Chapter 8,
still not yet built as of this chapter) -- a chapter mini-project,
matching Chapters 7-8's own pattern.

How to run:
    python3 solution.py
Prints the structural self-check: 9/9.
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


def inspectionscout_worker(subtask, rng):
    if rng.random() < 0.2:
        raise RuntimeError("inspectionscout could not reach the site record")
    return f"inspected: {subtask}"


def zonescout_worker(subtask, rng):
    if rng.random() < 0.2:
        raise RuntimeError("zonescout could not verify the parcel record")
    return f"zoned: {subtask}"


WORKER_FNS = {"inspectionscout": inspectionscout_worker, "zonescout": zonescout_worker}


def route_subtask(subtask):
    words = set(subtask.lower().replace(".", "").split())
    scores = {w: len(words & kws) for w, kws in WORKER_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return None
    return best


def dispatch_isolated(worker_fn, subtask, rng):
    try:
        return {"ok": True, "result": worker_fn(subtask, rng)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def which_agent_responsible(trace):
    for agent, tool, ok in trace:
        if not ok:
            return agent
    return None


def run_city_scout_harness(cases=CASES, seed=11):
    rng = random.Random(seed)
    results = {}
    for case in cases:
        dispatched = set()
        trace = []
        for subtask in case["subtasks"]:
            worker = route_subtask(subtask)
            if worker is None:
                trace.append(("unrouted", subtask, False))
                continue
            key = (subtask, worker)
            if key in dispatched:
                continue
            dispatched.add(key)
            outcome = dispatch_isolated(WORKER_FNS[worker], subtask, rng)
            trace.append((worker, subtask, outcome["ok"]))
        n = len(trace)
        n_ok = sum(1 for _, _, ok in trace if ok)
        results[case["id"]] = {
            "trace": trace,
            "success_rate": (n_ok / n) if n else 0.0,
            "first_failed_agent": which_agent_responsible(trace),
        }
    return results


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
    results.append(("C1 (two distinct routable subtasks) has 2 trace entries", len(harness["C1"]["trace"]) == 2))
    results.append(("C3's duplicate subtask is skipped via idempotent dispatch (1 trace entry, not 2)", len(harness["C3"]["trace"]) == 1))
    results.append(("C4's unroutable subtask is attributed to 'unrouted', not silently dropped", harness["C4"]["first_failed_agent"] == "unrouted"))
    results.append(("every case's success_rate is a valid rate in [0, 1]", all(0.0 <= harness[c]["success_rate"] <= 1.0 for c in harness)))

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
