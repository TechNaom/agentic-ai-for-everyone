"""
Chapter 10 Project (Chapter Mini-Project): A Peer Coordination Harness
for Ravenshollow Talent Agency -- REFERENCE SOLUTION. See starter.py
for the full scenario description.

Not the L3 Independent project (which the course's project ladder
still owes the repo, per PROJECT_STATE.md -- deferred past Chapter 8,
past Chapter 9, and still not built as of this chapter) -- a chapter
mini-project, matching Chapters 7-9's own pattern.

How to run:
    python3 solution.py
Prints the structural self-check: 9/9.
"""

import threading

CASES = [
    {"id": "C1", "claims": [("castingscout", "G-10"), ("bookingscout", "G-20")]},
    {"id": "C2", "claims": [("castingscout", "G-30"), ("bookingscout", "G-30")]},  # duplicate
    {"id": "C3", "claims": [("bookingscout", "G-40"), ("bookingscout", "G-40")]},  # same agent retries itself
    {"id": "C4", "deadlock": True, "elapsed_s": 6},
]

ALL_AGENTS = ["castingscout", "bookingscout"]


def parse_message_safely(raw_args, required_fields=("recipient", "type", "gig_id")):
    normalized = {k.strip(): v for k, v in raw_args.items()}
    missing = [f for f in required_fields if f not in normalized]
    if missing:
        return {"ok": False, "reason": f"missing required fields after normalization: {missing}"}
    return {"ok": True, "fields": normalized}


_shared_claims = set()
_shared_lock = threading.Lock()


def coordinated_claim(agent_name, gig_id):
    with _shared_lock:
        if gig_id in _shared_claims:
            return {"ok": False, "agent": agent_name, "gig_id": gig_id, "reason": "already claimed"}
        _shared_claims.add(gig_id)
        return {"ok": True, "agent": agent_name, "gig_id": gig_id}


def check_for_deadlock(timeout_s, elapsed_s):
    if elapsed_s >= timeout_s:
        return {"status": "deadlock_detected", "waited_s": elapsed_s}
    return {"status": "waiting", "waited_s": elapsed_s}


def break_deadlock_if_needed(timeout_s, elapsed_s, all_agent_names):
    status = check_for_deadlock(timeout_s, elapsed_s)
    if status["status"] != "deadlock_detected":
        return status
    first_mover = sorted(all_agent_names)[0]
    return {"status": "deadlock_broken", "first_mover": first_mover}


def which_agent_caused_duplicate(trace):
    for entry in trace:
        if entry["ok"] is False:
            return entry["agent"]
    return None


def run_ravenshollow_harness(cases=CASES, timeout_s=5):
    global _shared_claims
    _shared_claims = set()
    results = {}
    for case in cases:
        if case.get("deadlock"):
            results[case["id"]] = {
                "trace": [],
                "deadlock_status": break_deadlock_if_needed(timeout_s, case["elapsed_s"], ALL_AGENTS),
                "first_duplicate_agent": None,
            }
            continue
        trace = []
        for agent, gig_id in case["claims"]:
            outcome = coordinated_claim(agent, gig_id)
            trace.append(outcome)
        results[case["id"]] = {
            "trace": trace,
            "deadlock_status": None,
            "first_duplicate_agent": which_agent_caused_duplicate(trace),
        }
    return results


def self_check():
    results = []

    v1 = parse_message_safely({"recipient": "CastingScout", " type ": "claim", "gig_id": "G-1"})
    v2 = parse_message_safely({"recipient": "CastingScout", "kind": "claim", "gig_id": "G-1"})
    results.append(("parse_message_safely normalizes whitespace in keys", v1["ok"] is True))
    results.append(("parse_message_safely fails closed on a renamed/missing field", v2["ok"] is False))

    global _shared_claims
    _shared_claims = set()
    c1 = coordinated_claim("castingscout", "G-99")
    c2 = coordinated_claim("bookingscout", "G-99")
    results.append(("coordinated_claim: first claim succeeds", c1["ok"] is True))
    results.append(("coordinated_claim: duplicate claim is rejected, not re-granted", c2["ok"] is False))

    harness = run_ravenshollow_harness()
    results.append(("run_ravenshollow_harness returns results for all 4 cases", set(harness.keys()) == {"C1", "C2", "C3", "C4"}))
    results.append(("C1 (two distinct gigs) has 2 successful trace entries", sum(1 for t in harness["C1"]["trace"] if t["ok"]) == 2))
    results.append(("C2's duplicate claim is caught and attributed to bookingscout", harness["C2"]["first_duplicate_agent"] == "bookingscout"))
    results.append(("C3 (same agent retries itself) still catches the duplicate", harness["C3"]["first_duplicate_agent"] == "bookingscout"))
    results.append(("C4's deadlock is detected and broken by the alphabetically-first agent", harness["C4"]["deadlock_status"] == {"status": "deadlock_broken", "first_mover": "bookingscout"}))

    print("Chapter 10 Project -- Structural Self-Check")
    print("=" * 60)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 60)
    print(f"{passed}/{len(results)} checks passed")


if __name__ == "__main__":
    self_check()
