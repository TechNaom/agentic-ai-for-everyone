"""
Chapter 11 Project (Chapter Mini-Project): An Overnight Operating
Harness for Wrenfield Dispatch Alliance -- REFERENCE SOLUTION. See
starter.py for the full scenario description.

Not the L3 Independent project (which the course's project ladder
still owes the repo, per PROJECT_STATE.md -- deferred past Chapter 8,
9, and 10; this session's decision on it is recorded in
quality-audits/chapter-11-audit.md) -- a chapter mini-project,
matching Chapters 7-10's own pattern.

How to run:
    python3 solution.py
Prints the structural self-check: 9/9.
"""

import json
import threading
import time

ALL_AGENTS = ["claimscout", "shipscout"]

CASES = [
    {"id": "C1", "agent": "claimscout", "shipment_id": "W-100", "action": "confirm_dispatch", "flaky": False},
    {"id": "C2", "agent": "shipscout", "shipment_id": "W-200", "action": "confirm_dispatch", "flaky": True},
    {"id": "C3", "agent": "shipscout", "shipment_id": "W-200", "action": "confirm_dispatch", "flaky": False},  # retry-shaped repeat of C2's key
    {"id": "C4", "agent": "claimscout", "shipment_id": "W-300", "action": "confirm_dispatch", "flaky": "always"},
]

# ---------------------------------------------------------------------------
# TODO 1 (production-gear, given filled in): idempotency_key +
# commit_once -- a side effect commits exactly once even across a
# retried call with drifted arguments.
# ---------------------------------------------------------------------------
_committed_keys = {}
_committed_lock = threading.Lock()


def idempotency_key(agent, shipment_id, action):
    return f"{agent}:{shipment_id}:{action}"


def commit_once(key, effect_fn):
    with _committed_lock:
        if key in _committed_keys:
            return {"ok": True, "result": _committed_keys[key], "replayed": True}
        result = effect_fn()
        _committed_keys[key] = result
        return {"ok": True, "result": result, "replayed": False}


# ---------------------------------------------------------------------------
# TODO 2 (production-gear, given filled in): call_with_retries --
# bounded attempts, exponential backoff, every attempt logged.
# ---------------------------------------------------------------------------
class RetriesExhausted(Exception):
    pass


def event(correlation_id, event_type, **fields):
    return json.dumps({"correlation_id": correlation_id, "event": event_type,
                        **fields}, sort_keys=True)


def call_with_retries(fn, max_attempts, base_delay, log, correlation_id, agent):
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            result = fn()
            log.append(event(correlation_id, "retry_attempt", agent=agent,
                              attempt=attempt, ok=True))
            return result
        except Exception as e:
            last_exc = e
            log.append(event(correlation_id, "retry_attempt", agent=agent,
                              attempt=attempt, ok=False, error=str(e)))
            if attempt < max_attempts:
                time.sleep(base_delay * (2 ** (attempt - 1)))
    log.append(event(correlation_id, "retries_exhausted", agent=agent, attempts=max_attempts))
    raise RetriesExhausted(f"{max_attempts} attempts failed: {last_exc}")


# ---------------------------------------------------------------------------
# TODO 3 (production-gear, given filled in): run_summary_from_log --
# a crash-survivable summary computed by re-parsing the log.
# ---------------------------------------------------------------------------
def run_summary_from_log(log_lines):
    parsed = [json.loads(line) for line in log_lines]
    dispatches = [e for e in parsed if e["event"] == "dispatch"]
    commits = [e for e in parsed if e["event"] == "commit"]
    retries = [e for e in parsed if e["event"] == "retry_attempt" and e.get("ok") is False]
    exhausted = [e for e in parsed if e["event"] == "retries_exhausted"]
    n_dispatch = len(dispatches)
    n_ok = sum(1 for e in dispatches if e.get("ok"))
    return {
        "dispatches": n_dispatch,
        "success_rate": (n_ok / n_dispatch) if n_dispatch else 0.0,
        "commits": len(commits),
        "failed_retry_attempts": len(retries),
        "exhausted": len(exhausted),
    }


# ---------------------------------------------------------------------------
# The assembled overnight harness.
# ---------------------------------------------------------------------------
def _confirm_with_flakiness(case, attempt_counter):
    """Simulates the real tool call. 'flaky': True fails once then
    succeeds (recoverable); 'always' fails every attempt (unrecoverable)."""
    key = (case["id"],)
    attempt_counter[key] = attempt_counter.get(key, 0) + 1
    if case["flaky"] == "always":
        raise RuntimeError(f"{case['agent']} could not reach the dispatch record")
    if case["flaky"] is True and attempt_counter[key] < 2:
        raise RuntimeError(f"{case['agent']} transient dispatch error")
    return f"{case['agent']}:{case['shipment_id']}:confirmed"


def run_wrenfield_night(cases=CASES, correlation_id="wrenfield-run-001"):
    log = []
    attempt_counter = {}
    outcomes = {}
    for case in cases:
        agent, shipment_id, action = case["agent"], case["shipment_id"], case["action"]
        key = idempotency_key(agent, shipment_id, action)

        def do_confirm():
            return _confirm_with_flakiness(case, attempt_counter)

        try:
            raw_result = call_with_retries(do_confirm, max_attempts=3, base_delay=0.0,
                                            log=log, correlation_id=correlation_id, agent=agent)
            log.append(event(correlation_id, "dispatch", agent=agent, case=case["id"], ok=True))
            commit = commit_once(key, lambda r=raw_result: r)
            log.append(event(correlation_id, "commit", agent=agent, case=case["id"],
                              replayed=commit["replayed"]))
            outcomes[case["id"]] = {"ok": True, "replayed": commit["replayed"], "result": commit["result"]}
        except RetriesExhausted as e:
            log.append(event(correlation_id, "dispatch", agent=agent, case=case["id"], ok=False))
            outcomes[case["id"]] = {"ok": False, "error": str(e)}
    return {"log": log, "outcomes": outcomes, "summary": run_summary_from_log(log)}


def self_check():
    global _committed_keys
    results = []

    _committed_keys = {}

    k1 = idempotency_key("claimscout", "W-900", "confirm_dispatch")
    c1 = commit_once(k1, lambda: "first")
    c2 = commit_once(k1, lambda: "SHOULD NOT RUN")
    results.append(("idempotency_key + commit_once: second call replays, never re-runs the effect",
                     c1["replayed"] is False and c2["replayed"] is True and c2["result"] == "first"))

    attempts = {"n": 0}
    def flaky():
        attempts["n"] += 1
        if attempts["n"] < 2:
            raise RuntimeError("transient")
        return "ok"
    test_log = []
    r = call_with_retries(flaky, max_attempts=3, base_delay=0.0, log=test_log,
                           correlation_id="t", agent="claimscout")
    results.append(("call_with_retries recovers within bound and logs every attempt",
                     r == "ok" and len(test_log) == 2))

    try:
        call_with_retries(lambda: (_ for _ in ()).throw(RuntimeError("boom")),
                           max_attempts=2, base_delay=0.0, log=[], correlation_id="t", agent="x")
        exhausted_raised = False
    except RetriesExhausted:
        exhausted_raised = True
    results.append(("call_with_retries raises RetriesExhausted after max_attempts, no silent swallow", exhausted_raised))

    _committed_keys = {}
    night = run_wrenfield_night()
    results.append(("run_wrenfield_night returns outcomes for all 4 cases", set(night["outcomes"].keys()) == {"C1", "C2", "C3", "C4"}))
    results.append(("C1 (healthy call) commits successfully, not replayed", night["outcomes"]["C1"]["ok"] is True and night["outcomes"]["C1"]["replayed"] is False))
    results.append(("C2 (one transient failure) still commits via retry", night["outcomes"]["C2"]["ok"] is True))
    results.append(("C3 (same idempotency key as C2) is REPLAYED, not double-committed", night["outcomes"]["C3"]["ok"] is True and night["outcomes"]["C3"]["replayed"] is True))
    results.append(("C4 (always fails) exhausts retries and is reported as a failure, not a crash", night["outcomes"]["C4"]["ok"] is False))
    results.append(("run_summary_from_log's success_rate reflects C1-C3 success and C4 failure",
                     0.0 < night["summary"]["success_rate"] < 1.0))

    print("Chapter 11 Project -- Structural Self-Check")
    print("=" * 60)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 60)
    print(f"{passed}/{len(results)} checks passed")


if __name__ == "__main__":
    self_check()
