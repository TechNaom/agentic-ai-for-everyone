"""
Module 2 Combined Assessment: Tool-Interface Design + Memory-Architecture
Exercise

Per docs/curriculum/CURRICULUM_MAP.md, Module 2's stated assessment is
a "tool-interface design + memory-architecture exercise," spanning
Chapter 3 (tool use and function calling) and Chapter 4 (memory and
state). This reuses the EXACT functions those two chapters' own
projects already built and tested (Chapter 3's
diagnose_appliance_issue, Chapter 4's build_working_context /
run_visit_session / MemoryStore) applied to a combined scenario -- see
README.md for the full scenario and why this was built now.

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
MEMORY_PATH = os.path.join(HERE, "_module2_memory_scratch.json")


def _load(module_name, rel_path):
    path = os.path.join(REPO_ROOT, rel_path)
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ch3 = _load("ch3_solution", "chapters/chapter-03-tool-use-and-function-calling/project/solution.py")
ch4 = _load("ch4_solution", "chapters/chapter-04-memory-and-state/project/solution.py")


# ---------------------------------------------------------------------------
# Part 1 (Chapter 3's own diagnose_appliance_issue, applied to a new
# appliance whose warranty is EXPIRED):
# Call ch3.diagnose_appliance_issue("appl-301") -- Chapter 3's own
# fixture data already has this appliance's warranty as expired.
# ---------------------------------------------------------------------------
PART_1_ANSWER = None  # TODO 1: (tool_name, result) tuple


# ---------------------------------------------------------------------------
# Part 2 (Chapter 4's own MemoryStore + build_working_context +
# run_visit_session, applied to a fresh patient "pt-88"):
# Using a MemoryStore pointed at MEMORY_PATH (so this doesn't collide
# with any other chapter's memory file):
#   (a) confirm the working context is empty before any visit
#   (b) run a visit session where the patient reports "I have a severe
#       peanut allergy", requesting date "2026-10-05", human_approved=True
#   (c) confirm the SAME fact now appears in a fresh call to
#       build_working_context for the same patient (proving persistence
#       survived beyond the single session call)
# ---------------------------------------------------------------------------
PART_2_STORE = None  # TODO 2: ch4.MemoryStore(path=MEMORY_PATH)
PART_2_CONTEXT_BEFORE = None  # TODO 3
PART_2_VISIT_RESULT = None  # TODO 4
PART_2_CONTEXT_AFTER = None  # TODO 5


# ---------------------------------------------------------------------------
# Part 3 (cross-chapter synthesis -- the one genuinely new task this
# combined assessment adds beyond either chapter's own project):
# Chapter 3's RepairBot tools (check_warranty_status,
# run_diagnostic, schedule_repair_visit) are all STATELESS -- each call
# only depends on its own arguments. Chapter 4's CareBot tools compose
# with a MemoryStore that persists ACROSS calls. Write a short
# justification (2-4 sentences) for why RepairBot's diagnostic flow
# does NOT need a persisted memory store the way CareBot's visit flow
# does, referencing what specifically would break if RepairBot's
# tools had no memory of a PRIOR diagnostic call versus what actually
# breaks for CareBot if IT has no memory of a prior visit.
# ---------------------------------------------------------------------------
PART_3_JUSTIFICATION = None  # TODO 6: a real, descriptive string


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

def self_check():
    results = []

    ok1 = PART_1_ANSWER == ("check_warranty_status", {"status": "expired"})
    results.append(("Part 1: diagnose_appliance_issue correctly picks check_warranty_status for an expired warranty", ok1))

    ok2a = PART_2_CONTEXT_BEFORE == ([], {"conditions": [], "preferences": []})
    results.append(("Part 2a: working context is empty before any visit", ok2a))

    ok2b = (
        isinstance(PART_2_VISIT_RESULT, dict)
        and PART_2_VISIT_RESULT.get("persisted_facts", {}).get("conditions") == ["I have a severe peanut allergy"]
    )
    results.append(("Part 2b: run_visit_session persists the reported allergy as a condition", ok2b))

    ok2c = (
        isinstance(PART_2_CONTEXT_AFTER, tuple)
        and PART_2_CONTEXT_AFTER[1].get("conditions") == ["I have a severe peanut allergy"]
    )
    results.append(("Part 2c: a fresh build_working_context call still sees the persisted fact", ok2c))

    ok3 = isinstance(PART_3_JUSTIFICATION, str) and len(PART_3_JUSTIFICATION.strip()) >= 40 and "stateless" in PART_3_JUSTIFICATION.lower()
    results.append(("Part 3: justification is a real, substantive response referencing 'stateless'", ok3))

    print("Module 2 Combined Assessment -- Structural Self-Check")
    print("=" * 70)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 70)
    print(f"{passed}/{len(results)} objectively-checkable parts passed")
    print("Part 3's prose quality is self-graded against RUBRIC.md.")

    if os.path.exists(MEMORY_PATH):
        os.remove(MEMORY_PATH)


if __name__ == "__main__":
    self_check()
