"""
Module 5 Combined Assessment: Multi-Agent Coordination-Pattern Exercise

Per docs/curriculum/CURRICULUM_MAP.md, Module 5's stated assessment is
a "multi-agent coordination-pattern exercise," spanning Chapter 9
(orchestration/dispatch patterns), Chapter 10 (peer communication), and
Chapter 11 (operating a multi-agent system in production). Built during
Chapter 11's own session (its closing chapter), following the exact
precedent set at Chapter 8 for Module 4's own combined assessment.

How to run:
    python3 starter.py
Fill in each # TODO, re-run, and watch the self-check climb toward
4/4 objectively-checkable parts (Part 4 is self-graded against
RUBRIC.md).
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def _load(module_name, rel_path):
    path = os.path.join(REPO_ROOT, rel_path)
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ch9 = _load("ch9_solution", "chapters/chapter-09-multi-agent-orchestration-patterns/project/solution.py")
ch10 = _load("ch10_solution", "chapters/chapter-10-multi-agent-coordination-and-communication/project/solution.py")
ch11 = _load("ch11_solution", "chapters/chapter-11-operating-agents-in-production/project/solution.py")


# ---------------------------------------------------------------------------
# Part 1 (Chapter 9 dispatch): use ch9.route_subtask and
# ch9.which_agent_responsible (both loaded above, unchanged from
# Chapter 9's own project) to route a clear request, confirm an
# unroutable request returns None, and attribute a failed trace.
# ---------------------------------------------------------------------------
PART_1_ROUTE_CLEAR = None        # TODO 1: ch9.route_subtask("Inspect the site for structural issues.")
PART_1_ROUTE_UNROUTABLE = None   # TODO 2: ch9.route_subtask("I have a general question about my property.")
PART_1_RESPONSIBLE = None        # TODO 3: ch9.which_agent_responsible([("inspectionscout", "inspect", True), ("zonescout", "zone", False)])


# ---------------------------------------------------------------------------
# Part 2 (Chapter 10 communication): use ch10.parse_message_safely and
# ch10.coordinated_claim (both loaded above, unchanged from Chapter
# 10's own project) to validate a message and prevent a duplicate
# claim on the SAME gig_id.
# ---------------------------------------------------------------------------
PART_2_VALID = None       # TODO 4: ch10.parse_message_safely({"recipient": "CastingScout", " type ": "claim", "gig_id": "G-5"})
PART_2_INVALID = None     # TODO 5: ch10.parse_message_safely({"recipient": "CastingScout", "kind": "claim", "gig_id": "G-5"})
PART_2_CLAIM_1 = None     # TODO 6: reset ch10._shared_claims to a fresh set, then ch10.coordinated_claim("castingscout", "G-500")
PART_2_CLAIM_2 = None     # TODO 7: ch10.coordinated_claim("bookingscout", "G-500") -- same gig_id as TODO 6


# ---------------------------------------------------------------------------
# Part 3 (Chapter 11 operating): use ch11.idempotency_key,
# ch11.commit_once, and ch11.call_with_retries (all loaded above,
# unchanged from Chapter 11's own project) to commit a side effect
# exactly once and recover a flaky call within its retry bound.
# ---------------------------------------------------------------------------
PART_3_KEY = None         # TODO 8: ch11.idempotency_key("claimscout", "W-1", "confirm_dispatch")
PART_3_COMMIT_1 = None    # TODO 9: ch11.commit_once(PART_3_KEY, lambda: "first-commit") (reset ch11._committed_keys = {} first)
PART_3_COMMIT_2 = None    # TODO 10: ch11.commit_once(PART_3_KEY, lambda: "SHOULD NOT RUN AGAIN")

_attempts = {"n": 0}
def _flaky():
    _attempts["n"] += 1
    if _attempts["n"] < 2:
        raise RuntimeError("transient")
    return "recovered"

PART_3_RETRY_RESULT = None  # TODO 11: ch11.call_with_retries(_flaky, max_attempts=3, base_delay=0.0, log=[], correlation_id="module5-run", agent="claimscout")


# ---------------------------------------------------------------------------
# Part 4: cross-chapter synthesis. Write 3-5 sentences explaining how
# Chapter 9's which_agent_responsible, Chapter 10's coordinated_claim,
# and Chapter 11's idempotency_key together form ONE layered system,
# not three independent techniques -- reference all three function
# names by name and explain what happens if a retried call (Ch11)
# bypasses the claim-check (Ch10).
# ---------------------------------------------------------------------------
PART_4_JUSTIFICATION = None  # TODO 12: write your justification as a string


def self_check():
    results = []

    ok1 = (
        PART_1_ROUTE_CLEAR == "inspectionscout"
        and PART_1_ROUTE_UNROUTABLE is None
        and PART_1_RESPONSIBLE == "zonescout"
    )
    results.append(("Part 1: Chapter 9's route_subtask/which_agent_responsible route and attribute correctly", ok1))

    ok2 = (
        PART_2_VALID is not None and PART_2_VALID["ok"] is True
        and PART_2_INVALID is not None and PART_2_INVALID["ok"] is False
        and PART_2_CLAIM_1 is not None and PART_2_CLAIM_1["ok"] is True
        and PART_2_CLAIM_2 is not None and PART_2_CLAIM_2["ok"] is False
    )
    results.append(("Part 2: Chapter 10's parse_message_safely/coordinated_claim validate and prevent duplicates", ok2))

    ok3 = (
        PART_3_COMMIT_1 is not None and PART_3_COMMIT_1["replayed"] is False
        and PART_3_COMMIT_2 is not None and PART_3_COMMIT_2["replayed"] is True
        and PART_3_COMMIT_2 is not None and PART_3_COMMIT_1 is not None
        and PART_3_COMMIT_2["result"] == PART_3_COMMIT_1["result"]
        and PART_3_RETRY_RESULT == "recovered"
    )
    results.append(("Part 3: Chapter 11's commit_once/call_with_retries commit once and recover within bound", ok3))

    ok4 = (
        isinstance(PART_4_JUSTIFICATION, str)
        and len(PART_4_JUSTIFICATION.strip()) >= 40
        and "which_agent_responsible" in PART_4_JUSTIFICATION
        and "coordinated_claim" in PART_4_JUSTIFICATION
        and "idempotency_key" in PART_4_JUSTIFICATION
    )
    results.append(("Part 4: justification connects dispatch, communication, and operating layers together", ok4))

    print("Module 5 Combined Assessment -- Structural Self-Check")
    print("=" * 70)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 70)
    print(f"{passed}/{len(results)} objectively-checkable parts passed")
    print("Part 4's prose quality is self-graded against RUBRIC.md.")


if __name__ == "__main__":
    self_check()
