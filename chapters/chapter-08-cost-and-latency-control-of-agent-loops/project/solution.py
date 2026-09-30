"""
Chapter 8 Project (Chapter Mini-Project): A Cost-Controlled Harness for
YieldScout. Scenario: Portage Grain Cooperative, a fictional grain-
storage cooperative -- REFERENCE SOLUTION. See starter.py for the full
scenario description.

Not the L3 Independent project (which ships AFTER this chapter, per
docs/curriculum/CURRICULUM_MAP.md's project ladder) -- a chapter
mini-project, matching Chapter 7's own pattern.

How to run:
    python3 solution.py
Prints the structural self-check: 8/8.
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

STEP_ERROR_RATE = 0.15
MODEL_RATES = {"cheap": {"in": 0.05, "out": 0.15}, "strong": {"in": 1.00, "out": 3.00}}
CHEAP_ELIGIBLE = {"check_inventory_level", "fetch_market_price"}


def task_success(trace, task):
    return "check_inventory_level" in trace and bool(set(trace) & task["success_tools"])


def step_cost(tokens_in, tokens_out, model="cheap"):
    rates = MODEL_RATES[model]
    return round((tokens_in / 1000) * rates["in"] + (tokens_out / 1000) * rates["out"], 6)


def is_within_budget(steps_used, cost_used, max_steps, max_cost):
    return steps_used <= max_steps and cost_used <= max_cost


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


def run_cost_controlled_harness(n_runs_per_task=20, seed=3, max_steps=6, max_cost=0.15):
    rng = random.Random(seed)
    results = {}
    for task in TASKS:
        successes, costs = [], []
        for _ in range(n_runs_per_task):
            trace = simulate_agent_run(task, rng)
            run_cost, steps_used, allowed_trace = 0.0, 0, []
            for step in trace:
                model = choose_model_for_step(step)
                c = step_cost(20, 20, model)
                if not is_within_budget(steps_used + 1, run_cost + c, max_steps, max_cost):
                    break
                steps_used += 1
                run_cost += c
                allowed_trace.append(step)
            successes.append(task_success(allowed_trace, task))
            costs.append(run_cost)
        results[task["id"]] = {
            "task_success_rate": sum(successes) / len(successes),
            "total_cost": sum(costs),
            "n_runs": n_runs_per_task,
        }
    return results


def cost_per_success(results):
    out = {}
    for tid, r in results.items():
        n = r["n_runs"]
        s = round(r["task_success_rate"] * n)
        out[tid] = round(r["total_cost"] / s, 6) if s else None
    return out


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
