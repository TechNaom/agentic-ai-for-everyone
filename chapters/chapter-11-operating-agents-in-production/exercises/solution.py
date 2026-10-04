"""
Chapter 11 Exercises: Operating Agents in Production
Scenario: Cindermoor Parcel Network, a fictional regional parcel
sorting cooperative. Its two PEER agents, SortScout and RouteScout,
must run unattended overnight -- which means every claim they make
needs an idempotency key, every call/agent/exchange needs a timeout
at the right layer, every event needs a structured log line, and the
night's run needs a summary computed from that log.

This is a fresh scenario, deliberately different from the lesson's
Harrowgate Logistics Exchange/DockScout-YardScout hook. The point is
applying this chapter's production-operating concepts (idempotency,
bounded retries, layered timeouts, structured logging, crash-
survivable run summaries) to a system you haven't seen before --
REFERENCE SOLUTION.

How to run:
    python3 solution.py
Prints a score report. Scores 19/19.
"""

import json
import threading
import time


# ---------------------------------------------------------------------------
# Task 1: Map five Cindermoor facts to the single BEST-matching
# production-operating concept.
# ---------------------------------------------------------------------------
TASK_1_ANSWERS = {
    "fact_a": "idempotency",
    "fact_b": "retries with backoff",
    "fact_c": "per-call timeout",
    "fact_d": "structured logging",
    "fact_e": "crash-survivable run summary",
}


def score_exercise_1():
    correct = {
        "fact_a": "idempotency",
        "fact_b": "retries with backoff",
        "fact_c": "per-call timeout",
        "fact_d": "structured logging",
        "fact_e": "crash-survivable run summary",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Reasoning question.
# ---------------------------------------------------------------------------
TASK_2_ANSWER = "NO"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): idempotency_key + commit_once -- a side
# effect commits exactly once even across a retried call.
# ---------------------------------------------------------------------------
def idempotency_key(agent, parcel_id, action):
    return f"{agent}:{parcel_id}:{action}"


_committed_keys = {}
_committed_lock = threading.Lock()


def commit_once(key, effect_fn):
    with _committed_lock:
        if key in _committed_keys:
            return {"ok": True, "result": _committed_keys[key], "replayed": True}
        result = effect_fn()
        _committed_keys[key] = result
        return {"ok": True, "result": result, "replayed": False}


# ---------------------------------------------------------------------------
# Task 4 (production-gear): call_with_retries -- bounded attempts,
# exponential backoff, never silently unbounded.
# ---------------------------------------------------------------------------
class RetriesExhausted(Exception):
    pass


def call_with_retries(fn, max_attempts=3, base_delay=0.0):
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn(), attempt
        except Exception as e:
            last_exc = e
            if attempt < max_attempts:
                time.sleep(base_delay * (2 ** (attempt - 1)))
    raise RetriesExhausted(f"{max_attempts} attempts failed: {last_exc}")


# ---------------------------------------------------------------------------
# Task 5 (production-gear): classify_timeout_layer -- which of the
# three layers a given failure description belongs to.
# ---------------------------------------------------------------------------
def classify_timeout_layer(description):
    d = description.lower()
    if "network" in d or "single call" in d or "one request" in d:
        return "per-call"
    if "own loop" in d or "internal retries" in d or "one agent" in d:
        return "per-agent"
    if "exchange" in d or "never converg" in d or "both agents waiting" in d:
        return "per-exchange"
    return "unknown"


# ---------------------------------------------------------------------------
# Task 6 (production-gear): event + run_summary_from_log.
# ---------------------------------------------------------------------------
def event(correlation_id, event_type, **fields):
    return json.dumps({"correlation_id": correlation_id, "event": event_type,
                        **fields}, sort_keys=True)


def run_summary_from_log(log_lines):
    parsed = [json.loads(line) for line in log_lines]
    dispatches = [e for e in parsed if e["event"] == "dispatch"]
    commits = [e for e in parsed if e["event"] == "commit"]
    duplicates = [e for e in parsed if e["event"] == "duplicate_skipped"]
    n_dispatch = len(dispatches)
    n_ok = sum(1 for e in dispatches if e.get("ok"))
    return {
        "dispatches": n_dispatch,
        "success_rate": (n_ok / n_dispatch) if n_dispatch else 0.0,
        "commits": len(commits),
        "duplicates_skipped": len(duplicates),
    }


# ---------------------------------------------------------------------------
# Task 7 (production-gear): production_report -- reuses Chapter 8's
# is_within_budget unchanged, applied to a whole run's cost.
# ---------------------------------------------------------------------------
def is_within_budget(steps_used, cost_used, max_steps, max_cost):
    # Reused unchanged from Chapter 8 (via Chapter 9).
    return steps_used <= max_steps and cost_used <= max_cost


def production_report(run_summary, total_cost, max_cost):
    return {**run_summary, "total_cost": total_cost,
            "within_cost_budget": is_within_budget(0, total_cost, 0, max_cost)}


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
    results.append((f"Task 2: validation reasoning ({s2}/{t2})", s2 == t2))

    global _committed_keys
    _committed_keys = {}
    key = idempotency_key("sortscout", "P-900", "confirm_sort")
    c1 = commit_once(key, lambda: "sorted-P-900")
    c2 = commit_once(key, lambda: "SHOULD NOT RUN AGAIN")
    ok3 = c1["replayed"] is False and c2["replayed"] is True and c2["result"] == c1["result"]
    results.append((f"Task 3: commit_once commits once, replays on retry (c1={c1}, c2={c2})", ok3))
    if ok3:
        score += 3
    total += 3

    attempts = {"n": 0}
    def flaky():
        attempts["n"] += 1
        if attempts["n"] < 2:
            raise RuntimeError("transient")
        return "ok"
    result, used = call_with_retries(flaky, max_attempts=3)
    ok4 = result == "ok" and used == 2
    results.append((f"Task 4: call_with_retries recovers within bound (result={result}, attempts={used})", ok4))
    if ok4:
        score += 3
    total += 3

    l1 = classify_timeout_layer("one network call hung")
    l2 = classify_timeout_layer("one agent's own loop with internal retries ran long")
    l3 = classify_timeout_layer("the exchange never converged, both agents waiting")
    ok5 = l1 == "per-call" and l2 == "per-agent" and l3 == "per-exchange"
    results.append((f"Task 5: classify_timeout_layer classifies all three (l1={l1}, l2={l2}, l3={l3})", ok5))
    if ok5:
        score += 3
    total += 3

    cid = "cindermoor-run-1"
    log = [
        event(cid, "dispatch", agent="sortscout", ok=True),
        event(cid, "dispatch", agent="routescout", ok=False),
        event(cid, "commit", agent="sortscout"),
        event(cid, "duplicate_skipped", agent="routescout"),
    ]
    summary = run_summary_from_log(log)
    ok6 = summary == {"dispatches": 2, "success_rate": 0.5, "commits": 1, "duplicates_skipped": 1}
    results.append((f"Task 6: run_summary_from_log computes from the log ({summary})", ok6))
    if ok6:
        score += 2
    total += 2

    report = production_report({"dispatches": 2, "success_rate": 0.5}, total_cost=0.03, max_cost=0.10)
    ok7 = report["within_cost_budget"] is True and report["total_cost"] == 0.03
    results.append((f"Task 7: production_report reuses is_within_budget ({report})", ok7))
    if ok7:
        score += 2
    total += 2

    print("Chapter 11 Exercises -- Structural Self-Check")
    print("=" * 70)
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("=" * 70)
    print(f"Score: {score}/{total}")


if __name__ == "__main__":
    self_check()
