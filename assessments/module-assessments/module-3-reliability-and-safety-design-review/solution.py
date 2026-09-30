"""
Module 3 Combined Assessment: Reliability-and-Safety Design Review
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


ch4 = _load("ch4_solution", "chapters/chapter-04-memory-and-state/project/solution.py")

FACTS = {"conditions": ["unevaluated chest pain"], "preferences": []}

PART_1_DENIED = ch4.guardrail_check_booking(FACTS, human_approved=False)
PART_1_APPROVED = ch4.guardrail_check_booking(FACTS, human_approved=True)

PART_2_CONTEXT = {
    "facts": {"conditions": ["unevaluated chest pain"]},
    "tool_trace": [("schedule_followup", {"scheduled": True})],
}
PART_2_REFLECTED_DRAFT = ch4.reflect_on_response("Your visit is confirmed.", PART_2_CONTEXT)

PART_3_JUSTIFICATION = (
    "The guardrail and reflection are kept as two independent, defense-in-"
    "depth layers rather than one being retired now that the other exists: "
    "the guardrail (Chapter 6) stops most unsafe bookings BEFORE dispatch, "
    "which is why Part 1's denied case never lets schedule_followup run at "
    "all -- but reflection (Chapter 5) stays as a second, independent check "
    "against a future code path, a guardrail bug, or a refactor that "
    "accidentally bypasses the one call site the guardrail currently "
    "guards. In the common case shown here, the guardrail does make "
    "reflection's blocking-condition branch unreachable, but that's exactly "
    "what defense-in-depth is supposed to look like most of the time: the "
    "outer layer doing its job so the inner layer rarely has to."
)


def self_check():
    results = []

    ok1 = (
        isinstance(PART_1_DENIED, dict) and PART_1_DENIED.get("allowed") is False
        and isinstance(PART_1_APPROVED, dict) and PART_1_APPROVED.get("allowed") is True
    )
    results.append(("Part 1: guardrail_check_booking denies unapproved, allows approved, for the same blocking condition", ok1))

    ok2 = (
        isinstance(PART_2_REFLECTED_DRAFT, str)
        and "clinical review" in PART_2_REFLECTED_DRAFT
        and "unevaluated chest pain" in PART_2_REFLECTED_DRAFT
    )
    results.append(("Part 2: reflect_on_response correctly revises the draft for the blocking condition", ok2))

    ok3 = (
        isinstance(PART_3_JUSTIFICATION, str)
        and len(PART_3_JUSTIFICATION.strip()) >= 40
        and "defense" in PART_3_JUSTIFICATION.lower()
    )
    results.append(("Part 3: justification is a real, substantive response referencing 'defense-in-depth'", ok3))

    print("Module 3 Combined Assessment -- Structural Self-Check")
    print("=" * 70)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 70)
    print(f"{passed}/{len(results)} objectively-checkable parts passed")
    print("Part 3's prose quality is self-graded against RUBRIC.md.")


if __name__ == "__main__":
    self_check()
