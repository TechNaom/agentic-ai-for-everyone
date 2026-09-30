"""
Module 1 Combined Assessment: Agent-Loop Tracing + Planning Exercise
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


ch1 = _load("ch1_solution", "chapters/chapter-01-the-agent-loop-building-your-first-autonomous-agent/project/solution.py")
ch2 = _load("ch2_solution", "chapters/chapter-02-planning-and-task-decomposition/project/solution.py")


PART_1_ANSWER = ch1.run_agent("c19", ch1.FakeModel("normal"))

PART_2_NEXT_TOOL = ch2.decide_next_delay_check(
    [("get_delay_status", {"notes": "delayed due to weather, icy roads reported"})]
)
PART_2_PLANNING_MODE = ch2.classify_task_planning_mode(
    later_steps_depend_on_earlier_results=True, steps_known_in_advance=False
)

PART_3_JUSTIFICATION = (
    "SlipBot's loop only ever has ONE tool available (check_slip_availability), "
    "so there is no branching decision to make after the first observation -- "
    "the very next action is always either 'answer' or 'call the same tool "
    "again,' never a choice among several candidate next tools. Applying "
    "classify_task_planning_mode's own logic, SlipBot's later steps do not "
    "meaningfully depend on earlier results in the way the delay-diagnosis "
    "task's do (where the SPECIFIC next tool changes based on what the "
    "previous tool returned); SlipBot's single-tool loop is closer to a "
    "fixed, pre-known step (there is exactly one possible tool call), even "
    "though it's technically implemented as a loop rather than a straight-line "
    "plan."
)


def self_check():
    results = []

    ok1 = (
        isinstance(PART_1_ANSWER, tuple)
        and len(PART_1_ANSWER) == 2
        and PART_1_ANSWER[0] == "Slip C19 is available."
    )
    results.append(("Part 1: run_agent correctly resolves slip c19 as available", ok1))

    ok2 = PART_2_NEXT_TOOL == "check_weather_conditions"
    results.append(("Part 2a: decide_next_delay_check correctly picks check_weather_conditions", ok2))

    ok3 = PART_2_PLANNING_MODE == "emergent"
    results.append(("Part 2b: classify_task_planning_mode correctly classifies the diagnosis as emergent", ok3))

    ok4 = isinstance(PART_3_JUSTIFICATION, str) and len(PART_3_JUSTIFICATION.strip()) >= 40 and "fixed" in PART_3_JUSTIFICATION.lower()
    results.append(("Part 3: justification is a real, substantive response referencing 'fixed'", ok4))

    print("Module 1 Combined Assessment -- Structural Self-Check")
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
