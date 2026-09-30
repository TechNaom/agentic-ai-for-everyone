"""
Module 4 Combined Assessment: Reliability-Plan and Cost-Control Exercise
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


ch7 = _load("ch7_solution", "chapters/chapter-07-evaluating-agent-reliability/project/solution.py")
ch8 = _load("ch8_solution", "chapters/chapter-08-cost-and-latency-control-of-agent-loops/project/solution.py")

# ---------------------------------------------------------------------------
# Part 1 (Chapter 7): reliability -- trajectory correctness and task
# success on TriageScout's own T1 claim.
# ---------------------------------------------------------------------------
CH7_TASK = ch7.TASKS[0]  # T1: CLM-1, expects pull_claim_record -> check_fraud_flags -> calculate_payout_estimate

PART_1_CORRECT_ORDER = ch7.trajectory_correctness(
    ["pull_claim_record", "check_fraud_flags", "calculate_payout_estimate"],
    CH7_TASK["expected_trajectory"],
)
PART_1_WRONG_ORDER = ch7.trajectory_correctness(
    ["check_fraud_flags", "pull_claim_record", "calculate_payout_estimate"],
    CH7_TASK["expected_trajectory"],
)
PART_1_TASK_SUCCESS = ch7.task_success(
    ["pull_claim_record", "check_fraud_flags", "calculate_payout_estimate"], CH7_TASK
)

# ---------------------------------------------------------------------------
# Part 2 (Chapter 8): cost control -- the fail-closed budget on
# YieldScout's own accounting.
# ---------------------------------------------------------------------------
PART_2_WITHIN_BUDGET = ch8.is_within_budget(2, 0.02, max_steps=3, max_cost=0.05)
PART_2_OVER_STEP_BUDGET = ch8.is_within_budget(4, 0.02, max_steps=3, max_cost=0.05)
PART_2_OVER_COST_BUDGET = ch8.is_within_budget(2, 0.08, max_steps=3, max_cost=0.05)
PART_2_STEP_COST_CHEAP = ch8.step_cost(20, 20, "cheap")
PART_2_STEP_COST_STRONG = ch8.step_cost(20, 20, "strong")

# ---------------------------------------------------------------------------
# Part 3: cross-chapter synthesis -- the one genuinely new task this
# assessment adds.
# ---------------------------------------------------------------------------
PART_3_JUSTIFICATION = (
    "Chapter 7's reliability instrumentation and Chapter 8's cost control "
    "are not independent concerns that can be optimized separately -- "
    "Chapter 8's own cost_per_success function (reused conceptually here) "
    "exists specifically because a cost-reduction change can silently make "
    "the system worse if it is not re-measured against Chapter 7's own "
    "task_success and trajectory_correctness checks. A fail-closed budget "
    "(Part 2) that denies a step once a cap is exceeded can truncate a "
    "run's trace before it reaches its outcome-producing tool call, which "
    "directly lowers Part 1's own task_success rate if the caps are set "
    "too aggressively. The correct engineering practice is: never ship a "
    "cost or latency change without re-running the reliability harness "
    "afterward, and never report a cost-per-run number without also "
    "reporting the success rate it was measured against."
)


def self_check():
    results = []

    ok1 = PART_1_CORRECT_ORDER is True and PART_1_WRONG_ORDER is False and PART_1_TASK_SUCCESS is True
    results.append(("Part 1: Chapter 7's trajectory_correctness/task_success correctly distinguish correct vs. wrong order", ok1))

    ok2 = (
        PART_2_WITHIN_BUDGET is True
        and PART_2_OVER_STEP_BUDGET is False
        and PART_2_OVER_COST_BUDGET is False
        and abs(PART_2_STEP_COST_CHEAP - 0.004) < 0.0001
        and abs(PART_2_STEP_COST_STRONG - 0.08) < 0.0001
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
