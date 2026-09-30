"""
Module 1 Combined Assessment: Agent-Loop Tracing + Planning Exercise

Per docs/curriculum/CURRICULUM_MAP.md, Module 1's stated assessment is
an "agent-loop-tracing + planning exercise," spanning Chapter 1 (the
agent loop) and Chapter 2 (planning and task decomposition). This
reuses the EXACT functions those two chapters' own projects already
built and tested (Chapter 1's run_agent/FakeModel, Chapter 2's
classify_task_planning_mode/decide_next_delay_check) applied to a new
combined scenario, rather than inventing new mechanics -- see
README.md for the full scenario and why this was built now.

How to run:
    python3 starter.py
It prints a structural self-check for the parts that are objectively
checkable; Part 3's justification is open-ended prose, self-graded
against RUBRIC.md.
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


# ---------------------------------------------------------------------------
# Part 1 (Chapter 1's own run_agent/FakeModel, applied to a new slip ID):
# Run the agent loop against slip "c19" (available, 45ft) using a
# FakeModel("normal") -- the same well-behaved model behavior Chapter
# 1's own self-check used, just a different slip.
# ---------------------------------------------------------------------------
PART_1_ANSWER = None  # TODO 1: call ch1.run_agent("c19", ch1.FakeModel("normal")) and store the (answer, trace) tuple


# ---------------------------------------------------------------------------
# Part 2 (Chapter 2's own classify_task_planning_mode + decide_next_delay_check,
# applied to a new order's delay-diagnosis history):
# A new order's delay-diagnosis has produced this history so far:
#   [("get_delay_status", {"notes": "delayed due to weather, icy roads reported"})]
# Use ch2.decide_next_delay_check on that history to decide the next
# diagnostic tool, AND use ch2.classify_task_planning_mode to classify
# this diagnosis task (later_steps_depend_on_earlier_results=True,
# steps_known_in_advance=False).
# ---------------------------------------------------------------------------
PART_2_NEXT_TOOL = None  # TODO 2
PART_2_PLANNING_MODE = None  # TODO 3


# ---------------------------------------------------------------------------
# Part 3 (cross-chapter synthesis -- the one genuinely new task this
# combined assessment adds beyond either chapter's own project):
# Chapter 1's SlipBot uses a FIXED single-tool loop (it only ever has
# one tool to call, so there's no real branching). Chapter 2's delay
# diagnosis is EMERGENT (each step's choice depends on the previous
# result). Write a short justification (2-4 sentences) explaining WHY
# SlipBot's loop structure doesn't actually need emergent planning,
# using Chapter 2's own classify_task_planning_mode logic (not just
# asserting "fixed is simpler") to make the case.
# ---------------------------------------------------------------------------
PART_3_JUSTIFICATION = None  # TODO 4: a real, descriptive string


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

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
