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
survivable run summaries) to a system you haven't seen before.

How to run:
    python3 starter.py
Prints a score report. Fill in each # TODO, re-run, and watch your
score climb toward the total (19 points across 7 tasks).
"""

import json
import threading
import time


# ---------------------------------------------------------------------------
# Task 1: Map five Cindermoor facts to the single BEST-matching
# production-operating concept from this list:
#   "idempotency", "retries with backoff", "per-call timeout",
#   "structured logging", "crash-survivable run summary"
#
# Fact A: A retried "confirm this parcel sorted" call is keyed on
#         (agent, parcel_id, action) rather than its raw arguments, so
#         a retry can never commit the same confirmation twice.
# Fact B: A failed call to RouteScout's own routing tool is retried up
#         to 3 times, waiting longer between each attempt than the last.
# Fact C: A single network call to the sorting model is wrapped so it
#         cannot hang indefinitely if the connection stalls.
# Fact D: Every dispatch, retry, and commit is written as one JSON
#         line sharing the same correlation id for that night's run.
# Fact E: The night's success/failure counts are computed by re-reading
#         the log file the next morning, not from a counter that was
#         only ever held in the crashed process's memory.
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
        "fact_a": "idempotency",
        "fact_b": "retries with backoff",
        "fact_c": "per-call timeout",
        "fact_d": "structured logging",
        "fact_e": "crash-survivable run summary",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Should a retry system de-duplicate "the same" action by
# comparing the full raw argument JSON of each call? Answer "YES" or
# "NO".
# ---------------------------------------------------------------------------
TASK_2_ANSWER = None  # TODO 6: "YES" or "NO"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# TODO 7 (production-gear): idempotency_key + commit_once.
# idempotency_key(agent, parcel_id, action) should return the string
# f"{agent}:{parcel_id}:{action}". commit_once(key, effect_fn) should:
# if key is already in _committed_keys, return
# {"ok": True, "result": _committed_keys[key], "replayed": True}
# WITHOUT calling effect_fn again; otherwise call effect_fn(), store
# its result under key, and return
# {"ok": True, "result": result, "replayed": False}.
# ---------------------------------------------------------------------------
def idempotency_key(agent, parcel_id, action):
    # TODO 7a: implement as described above.
    return "not-implemented"


_committed_keys = {}
_committed_lock = threading.Lock()


def commit_once(key, effect_fn):
    # TODO 7b: implement as described above (hold _committed_lock while
    # checking and writing _committed_keys).
    return {"ok": True, "result": effect_fn(), "replayed": False}


# ---------------------------------------------------------------------------
# TODO 8 (production-gear): call_with_retries -- bounded attempts with
# exponential backoff. Call fn() up to max_attempts times; if it
# succeeds, return (result, attempt_number_used). If it raises, wait
# base_delay * (2 ** (attempt - 1)) seconds before the next attempt
# (skip the wait after the last attempt), then try again. If every
# attempt fails, raise RetriesExhausted.
# ---------------------------------------------------------------------------
class RetriesExhausted(Exception):
    pass


def call_with_retries(fn, max_attempts=3, base_delay=0.0):
    # TODO 8: implement as described above.
    try:
        return fn(), 1
    except Exception:
        return None, 1


# ---------------------------------------------------------------------------
# TODO 9 (production-gear): classify_timeout_layer -- given a plain-
# text description of a failure, return which of the three timeout
# layers it belongs to:
#   mentions "network", "single call", or "one request" -> "per-call"
#   mentions "own loop", "internal retries", or "one agent" -> "per-agent"
#   mentions "exchange", "never converg...", or "both agents waiting" -> "per-exchange"
#   otherwise -> "unknown"
# (Match case-insensitively.)
# ---------------------------------------------------------------------------
def classify_timeout_layer(description):
    # TODO 9: implement as described above.
    return "unknown"


# ---------------------------------------------------------------------------
# TODO 10 (production-gear): event + run_summary_from_log.
# event(correlation_id, event_type, **fields) should return a JSON
# string of {"correlation_id": correlation_id, "event": event_type,
# **fields} (use json.dumps with sort_keys=True).
# run_summary_from_log(log_lines) should parse each line with
# json.loads, then return:
#   {"dispatches": <count of event=="dispatch">,
#    "success_rate": <fraction of dispatches with ok truthy, 0.0 if none>,
#    "commits": <count of event=="commit">,
#    "duplicates_skipped": <count of event=="duplicate_skipped">}
# ---------------------------------------------------------------------------
def event(correlation_id, event_type, **fields):
    # TODO 10a: implement as described above.
    return "{}"


def run_summary_from_log(log_lines):
    # TODO 10b: implement as described above.
    return {"dispatches": 0, "success_rate": 0.0, "commits": 0, "duplicates_skipped": 0}


# ---------------------------------------------------------------------------
# TODO 11 (production-gear): production_report -- combine a run
# summary with a cost check, reusing is_within_budget (given below,
# unchanged from Chapter 8) rather than redefining the budget logic.
# Return {**run_summary, "total_cost": total_cost,
# "within_cost_budget": is_within_budget(0, total_cost, 0, max_cost)}.
# ---------------------------------------------------------------------------
def is_within_budget(steps_used, cost_used, max_steps, max_cost):
    # Reused unchanged from Chapter 8 (via Chapter 9) -- given, not a TODO.
    return steps_used <= max_steps and cost_used <= max_cost


def production_report(run_summary, total_cost, max_cost):
    # TODO 11: implement as described above.
    return dict(run_summary)


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
    ok7 = report.get("within_cost_budget") is True and report.get("total_cost") == 0.03
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
