"""
Module 4 Combined Assessment: Reliability-Plan and Cost-Control Exercise

Per docs/curriculum/CURRICULUM_MAP.md, Module 4's stated assessment is
a "reliability-plan + cost-control exercise," spanning Chapter 7
(evaluating agent reliability) and Chapter 8 (cost and latency
control). Built during Chapter 8's own session, following the exact
precedent set at Chapter 7 for Modules 1-3's own combined assessments.

How to run:
    python3 starter.py
Fill in each # TODO, re-run, and watch the self-check climb toward
3/3 objectively-checkable parts (Part 3 is self-graded against
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


ch7 = _load("ch7_solution", "chapters/chapter-07-evaluating-agent-reliability/project/solution.py")
ch8 = _load("ch8_solution", "chapters/chapter-08-cost-and-latency-control-of-agent-loops/project/solution.py")

CH7_TASK = ch7.TASKS[0]  # T1: CLM-1, expects pull_claim_record -> check_fraud_flags -> calculate_payout_estimate


# ---------------------------------------------------------------------------
# Part 1 (Chapter 7 reliability): use ch7.trajectory_correctness and
# ch7.task_success (both loaded above, unchanged from Chapter 7's own
# project) to check a correct-order trace and a wrong-order trace
# against CH7_TASK.
# ---------------------------------------------------------------------------
PART_1_CORRECT_ORDER = None  # TODO 1: ch7.trajectory_correctness(correct-order trace, CH7_TASK["expected_trajectory"])
PART_1_WRONG_ORDER = None    # TODO 2: ch7.trajectory_correctness(wrong-order trace, CH7_TASK["expected_trajectory"])
PART_1_TASK_SUCCESS = None   # TODO 3: ch7.task_success(correct-order trace, CH7_TASK)


# ---------------------------------------------------------------------------
# Part 2 (Chapter 8 cost control): use ch8.is_within_budget and
# ch8.step_cost (both loaded above, unchanged from Chapter 8's own
# project) to check a within-budget case, a step-cap violation, a
# cost-cap violation, and two model-tier costs.
# ---------------------------------------------------------------------------
PART_2_WITHIN_BUDGET = None      # TODO 4: ch8.is_within_budget(2, 0.02, max_steps=3, max_cost=0.05)
PART_2_OVER_STEP_BUDGET = None   # TODO 5: ch8.is_within_budget(4, 0.02, max_steps=3, max_cost=0.05)
PART_2_OVER_COST_BUDGET = None   # TODO 6: ch8.is_within_budget(2, 0.08, max_steps=3, max_cost=0.05)
PART_2_STEP_COST_CHEAP = None    # TODO 7: ch8.step_cost(20, 20, "cheap")
PART_2_STEP_COST_STRONG = None   # TODO 8: ch8.step_cost(20, 20, "strong")


# ---------------------------------------------------------------------------
# Part 3: cross-chapter synthesis. Write 2-4 sentences explaining why
# Chapter 7's reliability instrumentation and Chapter 8's cost control
# cannot be optimized independently -- reference cost_per_success (or
# the general idea it represents) and explain what a fail-closed
# budget set too aggressively could do to a task's own success rate.
# ---------------------------------------------------------------------------
PART_3_JUSTIFICATION = None  # TODO 9: write your justification as a string


def self_check():
    results = []

    ok1 = PART_1_CORRECT_ORDER is True and PART_1_WRONG_ORDER is False and PART_1_TASK_SUCCESS is True
    results.append(("Part 1: Chapter 7's trajectory_correctness/task_success correctly distinguish correct vs. wrong order", ok1))

    ok2 = (
        PART_2_WITHIN_BUDGET is True
        and PART_2_OVER_STEP_BUDGET is False
        and PART_2_OVER_COST_BUDGET is False
        and PART_2_STEP_COST_CHEAP is not None and abs(PART_2_STEP_COST_CHEAP - 0.004) < 0.0001
        and PART_2_STEP_COST_STRONG is not None and abs(PART_2_STEP_COST_STRONG - 0.08) < 0.0001
    )
    results.append(("Part 2: Chapter 8's is_within_budget/step_cost correctly enforce a fail-closed budget", ok2))

    ok3 = (
        isinstance(PART_3_JUSTIFICATION, str)
        and len(PART_3_JUSTIFICATION.strip()) >= 40
        and "cost_per_success" in PART_3_JUSTIFICATION
        and "task_success" in PART_3_JUSTIFICATION
    )
    results.append(("Part 3: justification is a real, substantive response connecting cost control back to reliability", ok3))

    print("Module 4 Combined Assessment -- Structural Self-Check")
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
