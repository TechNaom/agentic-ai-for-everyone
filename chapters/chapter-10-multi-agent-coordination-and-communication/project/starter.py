"""
Chapter 10 Project (Chapter Mini-Project): A Peer Coordination Harness
for Ravenshollow Talent Agency, a fictional talent-booking agency.
It runs two PEER agents -- CastingScout and BookingScout -- that must
claim audition/booking gigs from a shared pool by exchanging messages
directly, the same way the lesson's DockScout and YardScout coordinated
shipments. No supervisor routes work between them.

This is a chapter mini-project, NOT the course's L3 Independent
project (which the project ladder still owes the repo -- deferred past
Chapter 8, past Chapter 9, and NOT built this chapter either; see
PROJECT_STATE.md). It is gradable offline with deterministic,
constructed scenarios (no live model call needed), matching this
chapter's own lesson harness and this course's project grading policy
from Chapters 7-9.

How to run:
    python3 starter.py
It prints a structural self-check: 9 checks across message validation,
the shared claim-check, and the assembled peer-coordination harness.
"""

import threading

CASES = [
    {"id": "C1", "claims": [("castingscout", "G-10"), ("bookingscout", "G-20")]},
    {"id": "C2", "claims": [("castingscout", "G-30"), ("bookingscout", "G-30")]},  # duplicate
    {"id": "C3", "claims": [("bookingscout", "G-40"), ("bookingscout", "G-40")]},  # same agent retries itself
    {"id": "C4", "deadlock": True, "elapsed_s": 6},
]

ALL_AGENTS = ["castingscout", "bookingscout"]


# ---------------------------------------------------------------------------
# TODO 1: parse_message_safely -- normalize safe whitespace in keys, fail
# closed on a missing (or renamed) required field.
# ---------------------------------------------------------------------------
def parse_message_safely(raw_args, required_fields=("recipient", "type", "gig_id")):
    """
    Build `normalized` by stripping leading/trailing whitespace from
    every key in raw_args (values unchanged). Then check that every
    field in required_fields is present in `normalized`. If any are
    missing, return {"ok": False, "reason": "missing required fields
    after normalization: <list of missing fields>"}. Otherwise return
    {"ok": True, "fields": normalized}.
    """
    # TODO 1: implement as described above.
    return {"ok": True, "fields": raw_args}


# ---------------------------------------------------------------------------
# TODO 2: coordinated_claim -- an atomic, LOCKED check-and-claim against
# shared state, preventing duplicated work between the two peers.
# ---------------------------------------------------------------------------
_shared_claims = set()
_shared_lock = threading.Lock()


def coordinated_claim(agent_name, gig_id):
    """
    Inside a single `with _shared_lock:` block: if gig_id is already in
    _shared_claims, return {"ok": False, "agent": agent_name, "gig_id":
    gig_id, "reason": "already claimed"}. Otherwise, add gig_id to
    _shared_claims and return {"ok": True, "agent": agent_name,
    "gig_id": gig_id}. The check and the add MUST happen inside the
    SAME locked block, or the race this chapter's own Section 8 found
    live can still occur.
    """
    # TODO 2: implement as described above.
    return {"ok": True, "agent": agent_name, "gig_id": gig_id}


# ---------------------------------------------------------------------------
# Given -- deadlock detection/breaking and duplicate attribution, reused
# from the lesson's own pattern. No need to edit.
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# TODO 3: run_ravenshollow_harness -- the assembled peer-coordination
# harness.
# ---------------------------------------------------------------------------
def run_ravenshollow_harness(cases=CASES, timeout_s=5):
    """
    Reset the shared claim set to empty first (so re-running the
    harness doesn't carry state from a previous run). For each case in
    `cases`:
      1. If case.get("deadlock") is truthy: store
         {"trace": [], "deadlock_status":
         break_deadlock_if_needed(timeout_s, case["elapsed_s"],
         ALL_AGENTS), "first_duplicate_agent": None} under
         results[case["id"]], and move on to the next case.
      2. Otherwise: build an empty `trace` list. For each (agent,
         gig_id) pair in case["claims"], call
         coordinated_claim(agent, gig_id) and append its return value
         to `trace`. Store {"trace": trace, "deadlock_status": None,
         "first_duplicate_agent": which_agent_caused_duplicate(trace)}
         under results[case["id"]].
    Return the `results` dict.
    """
    # TODO 3: implement as described above.
    return {}


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

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
    results.append(("C1 (two distinct gigs) has 2 successful trace entries", sum(1 for t in harness.get("C1", {}).get("trace", []) if t["ok"]) == 2))
    results.append(("C2's duplicate claim is caught and attributed to bookingscout", harness.get("C2", {}).get("first_duplicate_agent") == "bookingscout"))
    results.append(("C3 (same agent retries itself) still catches the duplicate", harness.get("C3", {}).get("first_duplicate_agent") == "bookingscout"))
    results.append(("C4's deadlock is detected and broken by the alphabetically-first agent", harness.get("C4", {}).get("deadlock_status") == {"status": "deadlock_broken", "first_mover": "bookingscout"}))

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
