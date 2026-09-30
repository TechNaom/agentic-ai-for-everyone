"""
Module 3 Combined Assessment: Reliability-and-Safety Design Review

Per docs/curriculum/CURRICULUM_MAP.md, Module 3's stated assessment is
a "reliability-and-safety design review," spanning Chapter 5
(reflection and self-correction) and Chapter 6 (guardrails and safety).
Chapters 5 and 6 don't have their own standalone project files -- both
extended Chapter 4's CareBot project directly (reflect_on_response()
added by Chapter 5, guardrail_check_booking() added by Chapter 6, both
living in chapters/chapter-04-memory-and-state/project/solution.py).
This assessment reuses those EXACT functions, applied to a combined
review scenario -- see README.md for the full scenario and why this
was built now.

How to run:
    python3 starter.py
It prints a structural self-check for the objectively-checkable parts;
Part 3's justification is open-ended prose, self-graded against
RUBRIC.md.
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


# ---------------------------------------------------------------------------
# Part 1 (Chapter 6's own guardrail_check_booking, applied to a fresh
# patient's persisted facts):
# A new patient's persisted facts show one blocking condition,
# "unevaluated chest pain". Call ch4.guardrail_check_booking
# TWICE: once with human_approved=False, once with human_approved=True.
# ---------------------------------------------------------------------------
PART_1_DENIED = None  # TODO 1: guardrail_check_booking(..., human_approved=False)
PART_1_APPROVED = None  # TODO 2: guardrail_check_booking(..., human_approved=True)


# ---------------------------------------------------------------------------
# Part 2 (Chapter 5's own reflect_on_response, applied to a draft
# confirmation message for the SAME blocking condition):
# A draft says "Your visit is confirmed." The session's context shows
# facts={"conditions": ["unevaluated chest pain"]} and a
# tool_trace showing schedule_followup was actually dispatched
# (scheduled=True). Call reflect_on_response with this draft and
# context.
# ---------------------------------------------------------------------------
PART_2_REFLECTED_DRAFT = None  # TODO 3


# ---------------------------------------------------------------------------
# Part 3 (cross-chapter synthesis -- the one genuinely new task this
# combined assessment adds beyond either chapter's own material):
# Part 1 shows the guardrail DENYING the booking outright when not
# approved. Part 2 shows reflection REVISING a draft that describes a
# booking that (per Chapter 6's own extension) would only have
# happened at all if it were approved. Write a short justification
# (2-4 sentences) explaining why CareBot keeps BOTH mechanisms even
# though, in the common case, the guardrail makes reflection's
# blocking-condition branch unreachable -- reference Chapter 6's own
# "defense-in-depth" framing, not just "more checks are better."
# ---------------------------------------------------------------------------
PART_3_JUSTIFICATION = None  # TODO 4: a real, descriptive string


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

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
