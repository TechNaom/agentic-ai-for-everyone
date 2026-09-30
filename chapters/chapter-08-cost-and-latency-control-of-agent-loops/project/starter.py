"""
Chapter 8 Project (Chapter Mini-Project): A Cost-Controlled Harness for
YieldScout. Scenario: Portage Grain Cooperative, a fictional grain-
storage cooperative, wants YieldScout built the same way the lesson's
FactScout was cost-controlled -- a fresh scenario you build yourself,
combining this chapter's three pillars (per-step accounting, a
fail-closed budget, and a cost-controlled harness reusing
cost_per_success) into one real, reusable cost-control layer.

YieldScout has five tools:
  - check_inventory_level(silo_id): cheap, decisive -- the first move
    in every correct trajectory, routed to the cheap model tier.
  - fetch_market_price(commodity): also cheap-eligible -- a simple
    lookup, not a judgment call.
  - compute_yield_estimate(record): the normal ending for a silo with
    no quality issue and complete data -- strong tier (needs real
    calculation care).
  - flag_quality_issue(reason): the ending for a silo that trips a
    quality flag -- strong tier.
  - escalate_to_manager(reason): the ending for a silo with incomplete
    data -- strong tier.

This is a chapter mini-project, NOT the course's L3 Independent
project (which ships after Chapter 8, per
docs/curriculum/CURRICULUM_MAP.md's project ladder). It is gradable
offline with a deterministic seeded simulation (no live model call
needed), matching this chapter's own lesson harness and this course's
project grading policy from Chapters 2-3, 7.

How to run:
    python3 starter.py
It prints a structural self-check: 9 checks across task success,
the fail-closed budget check, and the aggregate cost-controlled
harness.
"""

import random

SILOS = {
    "SILO-1": {"silo_id": "SILO-1", "quality_issue": False, "data_complete": True, "bushels": 4200},
    "SILO-2": {"silo_id": "SILO-2", "quality_issue": True, "data_complete": True, "bushels": 3100},
    "SILO-3": {"silo_id": "SILO-3", "quality_issue": False, "data_complete": False, "bushels": 5000},
}

TASKS = [
    {"id": "T1", "silo_id": "SILO-1",
     "expected_trajectory": ["check_inventory_level", "fetch_market_price", "compute_yield_estimate"],
     "success_tools": {"compute_yield_estimate"}},
    {"id": "T2", "silo_id": "SILO-2",
     "expected_trajectory": ["check_inventory_level", "fetch_market_price", "flag_quality_issue"],
     "success_tools": {"flag_quality_issue"}},
    {"id": "T3", "silo_id": "SILO-3",
     "expected_trajectory": ["check_inventory_level", "fetch_market_price", "escalate_to_manager"],
     "success_tools": {"escalate_to_manager"}},
]
TOOLS = ["check_inventory_level", "fetch_market_price", "compute_yield_estimate",
         "flag_quality_issue", "escalate_to_manager"]

STEP_ERROR_RATE = 0.15  # illustrative; disclosed, not measured against live traffic
MODEL_RATES = {"cheap": {"in": 0.05, "out": 0.15}, "strong": {"in": 1.00, "out": 3.00}}
CHEAP_ELIGIBLE = {"check_inventory_level", "fetch_market_price"}


# ---------------------------------------------------------------------------
# TODO 1: task_success -- a forgiving, order-independent check.
# ---------------------------------------------------------------------------
def task_success(trace, task):
    """
    trace is a list of tool-name strings. Return True if
    "check_inventory_level" appears in trace AND at least one of
    task["success_tools"] also appears anywhere in trace. Otherwise
    return False.
    """
    # TODO 1: implement as described above.
    return False


# ---------------------------------------------------------------------------
# Given -- per-step token/cost accounting. No need to edit.
# ---------------------------------------------------------------------------
def step_cost(tokens_in, tokens_out, model="cheap"):
    rates = MODEL_RATES[model]
    return round((tokens_in / 1000) * rates["in"] + (tokens_out / 1000) * rates["out"], 6)


# ---------------------------------------------------------------------------
# TODO 2: is_within_budget -- a fail-closed budget check.
# ---------------------------------------------------------------------------
def is_within_budget(steps_used, cost_used, max_steps, max_cost):
    """
    Return True only if steps_used <= max_steps AND cost_used <=
    max_cost. Return False if EITHER cap is exceeded (fail-closed: any
    single exceeded cap denies the step).
    """
    # TODO 2: implement as described above.
    return True


# ---------------------------------------------------------------------------
# Given -- model routing and a seeded simulated YieldScout run. No
# need to edit either of these.
# ---------------------------------------------------------------------------
def choose_model_for_step(step_name):
    return "cheap" if step_name in CHEAP_ELIGIBLE else "strong"


def simulate_agent_run(task, rng):
    trace = []
    for step in task["expected_trajectory"]:
        roll = rng.random()
        if roll < STEP_ERROR_RATE * 0.4:
            continue
        elif roll < STEP_ERROR_RATE * 0.7:
            distractor = rng.choice([t for t in TOOLS if t != step])
            trace.append(distractor)
            trace.append(step)
        else:
            trace.append(step)
    return trace


# ---------------------------------------------------------------------------
# TODO 3: run_cost_controlled_harness -- run each task N times, apply
# the fail-closed budget to each simulated run, and return a results
# dict keyed by task id.
# ---------------------------------------------------------------------------
def run_cost_controlled_harness(n_runs_per_task=20, seed=3, max_steps=6, max_cost=0.15):
    """
    For each task in TASKS, run simulate_agent_run n_runs_per_task
    times using a single shared random.Random(seed) instance. For
    EACH simulated run's trace, walk it step by step: for each step,
    compute its cost with step_cost(20, 20, choose_model_for_step(step))
    and check is_within_budget(steps_used + 1, run_cost + this_step_cost,
    max_steps, max_cost) BEFORE adding it -- if the check fails, stop
    walking this run's trace right there (the remaining steps are
    denied). Track the resulting allowed_trace and run_cost. After
    walking, compute task_success(allowed_trace, task) and add it to
    that task's successes list; add run_cost to that task's costs
    list. Return:
        {task_id: {"task_success_rate": float,
                    "total_cost": float,
                    "n_runs": int}}
    """
    # TODO 3: implement as described above.
    return {}


# ---------------------------------------------------------------------------
# Given -- cost_per_success, reused from Chapter 7's own pattern. No
# need to edit.
# ---------------------------------------------------------------------------
def cost_per_success(results):
    out = {}
    for tid, r in results.items():
        n = r["n_runs"]
        s = round(r["task_success_rate"] * n)
        out[tid] = round(r["total_cost"] / s, 6) if s else None
    return out


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

def self_check():
    results = []

    ok1a = task_success(["check_inventory_level", "fetch_market_price", "compute_yield_estimate"], TASKS[0]) is True
    ok1b = task_success(["fetch_market_price", "compute_yield_estimate"], TASKS[0]) is False
    results.append(("task_success is True with check_inventory_level + an ending tool present", ok1a))
    results.append(("task_success is False when check_inventory_level is missing", ok1b))

    ok2a = is_within_budget(2, 0.02, 3, 0.05) is True
    ok2b = is_within_budget(4, 0.02, 3, 0.05) is False
    ok2c = is_within_budget(2, 0.06, 3, 0.05) is False
    results.append(("is_within_budget True when both step and cost caps are respected", ok2a))
    results.append(("is_within_budget False when the step cap alone is exceeded", ok2b))
    results.append(("is_within_budget False when the cost cap alone is exceeded", ok2c))

    harness_results = run_cost_controlled_harness()
    ok3 = set(harness_results.keys()) == {"T1", "T2", "T3"}
    results.append(("run_cost_controlled_harness returns results for all 3 tasks", ok3))

    ok4 = ok3 and all(0.0 <= harness_results[t]["task_success_rate"] <= 1.0 for t in harness_results)
    results.append(("run_cost_controlled_harness task_success_rate values are valid rates in [0, 1]", ok4))

    ok5 = ok3 and all(harness_results[t]["total_cost"] >= 0.0 for t in harness_results)
    results.append(("run_cost_controlled_harness total_cost values are non-negative", ok5))

    cps = cost_per_success(harness_results) if ok3 else {}
    ok6 = ok3 and all(cps.get(t) is None or cps[t] >= 0.0 for t in harness_results)
    results.append(("cost_per_success computes a valid (non-negative or None) value per task", ok6))

    print("Chapter 8 Project -- Structural Self-Check")
    print("=" * 60)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 60)
    print(f"{passed}/{len(results)} checks passed")


if __name__ == "__main__":
    self_check()
