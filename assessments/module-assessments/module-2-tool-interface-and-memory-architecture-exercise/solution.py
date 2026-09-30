"""
Module 2 Combined Assessment: Tool-Interface Design + Memory-Architecture
Exercise
REFERENCE SOLUTION. See starter.py and README.md for the full scenario.

How to run:
    python3 solution.py
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


if os.path.exists(MEMORY_PATH):
    os.remove(MEMORY_PATH)

PART_1_ANSWER = ch3.diagnose_appliance_issue("appl-301")

PART_2_STORE = ch4.MemoryStore(path=MEMORY_PATH)
PART_2_CONTEXT_BEFORE = ch4.build_working_context("pt-88", PART_2_STORE)
PART_2_VISIT_RESULT = ch4.run_visit_session(
    "pt-88", PART_2_STORE, ["I have a severe peanut allergy"],
    requested_date="2026-10-05", human_approved=True,
)
PART_2_CONTEXT_AFTER = ch4.build_working_context("pt-88", PART_2_STORE)

PART_3_JUSTIFICATION = (
    "RepairBot's tools are STATELESS -- check_warranty_status and "
    "run_diagnostic each only need the appliance_id passed in that single "
    "call, and nothing about diagnosing appl-301 today depends on any prior "
    "visit; without memory, RepairBot simply re-runs the same lookups on "
    "the next call, which is correct and cheap. CareBot's visit flow "
    "breaks without persisted memory in a much more consequential way: "
    "a condition (the peanut allergy) reported in visit 1 has to inform "
    "guardrail_check_booking() and clinical safety in visit 2, which "
    "happens in a LATER, separate session -- without a MemoryStore that "
    "survives between calls, that allergy would be invisible to visit 2 "
    "entirely, a correctness gap RepairBot's stateless tools never have."
)


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
