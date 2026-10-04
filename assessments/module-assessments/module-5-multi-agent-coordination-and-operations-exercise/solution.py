"""
Module 5 Combined Assessment: Multi-Agent Coordination-Pattern Exercise
REFERENCE SOLUTION. See starter.py and README.md for the full scenario.

How to run:
    python3 solution.py
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
# Part 1 (Chapter 9): dispatch -- route_subtask and which_agent_responsible
# on CityScout's own case roster.
# ---------------------------------------------------------------------------
PART_1_ROUTE_CLEAR = ch9.route_subtask("Inspect the site for structural issues.")
PART_1_ROUTE_UNROUTABLE = ch9.route_subtask("I have a general question about my property.")
PART_1_RESPONSIBLE = ch9.which_agent_responsible(
    [("inspectionscout", "inspect", True), ("zonescout", "zone", False)]
)

# ---------------------------------------------------------------------------
# Part 2 (Chapter 10): communication -- parse_message_safely and
# coordinated_claim on Ravenshollow's own claim-check.
# ---------------------------------------------------------------------------
PART_2_VALID = ch10.parse_message_safely({"recipient": "CastingScout", " type ": "claim", "gig_id": "G-5"})
PART_2_INVALID = ch10.parse_message_safely({"recipient": "CastingScout", "kind": "claim", "gig_id": "G-5"})

_fresh_claims = set()
ch10._shared_claims = _fresh_claims
PART_2_CLAIM_1 = ch10.coordinated_claim("castingscout", "G-500")
PART_2_CLAIM_2 = ch10.coordinated_claim("bookingscout", "G-500")

# ---------------------------------------------------------------------------
# Part 3 (Chapter 11): operating -- idempotency_key/commit_once and
# call_with_retries on Wrenfield's own overnight harness.
# ---------------------------------------------------------------------------
ch11._committed_keys = {}
PART_3_KEY = ch11.idempotency_key("claimscout", "W-1", "confirm_dispatch")
PART_3_COMMIT_1 = ch11.commit_once(PART_3_KEY, lambda: "first-commit")
PART_3_COMMIT_2 = ch11.commit_once(PART_3_KEY, lambda: "SHOULD NOT RUN AGAIN")

_attempts = {"n": 0}
def _flaky():
    _attempts["n"] += 1
    if _attempts["n"] < 2:
        raise RuntimeError("transient")
    return "recovered"

PART_3_RETRY_RESULT = ch11.call_with_retries(
    _flaky, max_attempts=3, base_delay=0.0, log=[], correlation_id="module5-run", agent="claimscout"
)

# ---------------------------------------------------------------------------
# Part 4: cross-chapter synthesis -- the one genuinely new task this
# assessment adds.
# ---------------------------------------------------------------------------
PART_4_JUSTIFICATION = (
    "Chapters 9, 10, and 11 are three layers of the SAME multi-agent system, "
    "not three independent techniques. Chapter 9's which_agent_responsible "
    "only tells you a dispatch step failed if the dispatch trace was recorded "
    "in the first place; Chapter 10's coordinated_claim only prevents a "
    "duplicate commit if every caller actually routes through it, including "
    "a RETRIED caller; and Chapter 11's idempotency_key plus commit_once is "
    "what makes a retry of a Chapter 9 dispatch or a Chapter 10 claim safe to "
    "attempt at all, because without it a retried call that happens to drift "
    "in its own arguments (this course's own live result) could slip past "
    "coordinated_claim's dedupe and double-commit. Operating a multi-agent "
    "system in production means all three layers run together on every "
    "call: route and attribute (Ch9), validate and claim exactly once among "
    "peers (Ch10), and retry that claim safely without ever re-committing "
    "its side effect (Ch11)."
)


def self_check():
    results = []

    ok1 = (
        PART_1_ROUTE_CLEAR == "inspectionscout"
        and PART_1_ROUTE_UNROUTABLE is None
        and PART_1_RESPONSIBLE == "zonescout"
    )
    results.append(("Part 1: Chapter 9's route_subtask/which_agent_responsible route and attribute correctly", ok1))

    ok2 = (
        PART_2_VALID["ok"] is True
        and PART_2_INVALID["ok"] is False
        and PART_2_CLAIM_1["ok"] is True
        and PART_2_CLAIM_2["ok"] is False
    )
    results.append(("Part 2: Chapter 10's parse_message_safely/coordinated_claim validate and prevent duplicates", ok2))

    ok3 = (
        PART_3_COMMIT_1["replayed"] is False
        and PART_3_COMMIT_2["replayed"] is True
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
