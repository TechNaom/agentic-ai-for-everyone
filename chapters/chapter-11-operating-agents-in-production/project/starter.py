"""
Chapter 11 Project (Chapter Mini-Project): An Overnight Operating
Harness for Wrenfield Dispatch Alliance.

Wrenfield Dispatch Alliance, a fictional regional freight alliance,
runs two peer agents, ClaimScout and ShipScout, that confirm shipment
dispatches overnight. Nobody is watching. A confirmation call can be
retried after a transient failure, and once it succeeds it must NEVER
be committed twice -- even if the retried call's own arguments drift,
the way this chapter's own live Section 4 result showed a real retried
call can. Some calls fail every time and must be reported as a clean
failure, not a crash.

Not the L3 Independent project -- a chapter mini-project, matching
Chapters 7-10's own pattern.

How to run:
    python3 starter.py
Prints a score report. Fill in each # TODO, re-run, and watch your
score climb toward 9/9.
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
# TODO 1: idempotency_key + commit_once.
# idempotency_key(agent, shipment_id, action) should return the string
# f"{agent}:{shipment_id}:{action}" -- the fields that DEFINE the side
# effect, not any raw call argument.
# commit_once(key, effect_fn): if key is already in _committed_keys,
# return {"ok": True, "result": _committed_keys[key], "replayed": True}
# WITHOUT calling effect_fn again. Otherwise call effect_fn(), store its
# result under key, and return {"ok": True, "result": result,
# "replayed": False}. Hold _committed_lock for the whole check-and-write.
# ---------------------------------------------------------------------------
_committed_keys = {}
_committed_lock = threading.Lock()


def idempotency_key(agent, shipment_id, action):
    # TODO 1a: implement as described above.
    return "not-implemented"


def commit_once(key, effect_fn):
    # TODO 1b: implement as described above.
    return {"ok": True, "result": effect_fn(), "replayed": False}


# ---------------------------------------------------------------------------
# TODO 2: call_with_retries -- bounded attempts with exponential
# backoff. Call fn() up to max_attempts times. On success, log a
# "retry_attempt" event (ok=True) and return the result. On an
# exception, log a "retry_attempt" event (ok=False, error=str(e)),
# sleep base_delay * (2 ** (attempt - 1)) seconds if more attempts
# remain, and try again. If every attempt fails, log a
# "retries_exhausted" event and raise RetriesExhausted.
# ---------------------------------------------------------------------------
class RetriesExhausted(Exception):
    pass


def event(correlation_id, event_type, **fields):
    return json.dumps({"correlation_id": correlation_id, "event": event_type,
                        **fields}, sort_keys=True)


def call_with_retries(fn, max_attempts, base_delay, log, correlation_id, agent):
    # TODO 2: implement as described above.
    return fn()


# ---------------------------------------------------------------------------
# TODO 3: run_summary_from_log -- a crash-survivable summary computed
# by RE-PARSING the log lines (json.loads each one), not from any
# in-memory counter. Return:
#   {"dispatches": <count of event=="dispatch">,
#    "success_rate": <fraction of dispatches with ok truthy, 0.0 if none>,
#    "commits": <count of event=="commit">,
#    "failed_retry_attempts": <count of event=="retry_attempt" with ok False>,
#    "exhausted": <count of event=="retries_exhausted">}
# ---------------------------------------------------------------------------
def run_summary_from_log(log_lines):
    # TODO 3: implement as described above.
    return {"dispatches": 0, "success_rate": 0.0, "commits": 0,
            "failed_retry_attempts": 0, "exhausted": 0}


# ---------------------------------------------------------------------------
# The assembled overnight harness (given -- do not need to edit).
# ---------------------------------------------------------------------------
def _confirm_with_flakiness(case, attempt_counter):
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
        except Exception as e:
            # Starter's un-retried fn() can raise directly; keep the
            # harness itself from crashing so the score report always
            # prints even before TODO 2 is implemented.
            log.append(event(correlation_id, "dispatch", agent=agent, case=case["id"], ok=False))
            outcomes[case["id"]] = {"ok": False, "error": str(e)}
    return {"log": log, "outcomes": outcomes, "summary": run_summary_from_log(log)}


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

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
    try:
        r = call_with_retries(flaky, max_attempts=3, base_delay=0.0, log=test_log,
                               correlation_id="t", agent="claimscout")
    except Exception:
        r = None
    results.append(("call_with_retries recovers within bound and logs every attempt",
                     r == "ok" and len(test_log) == 2))

    try:
        call_with_retries(lambda: (_ for _ in ()).throw(RuntimeError("boom")),
                           max_attempts=2, base_delay=0.0, log=[], correlation_id="t", agent="x")
        exhausted_raised = False
    except RetriesExhausted:
        exhausted_raised = True
    except Exception:
        exhausted_raised = False
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
