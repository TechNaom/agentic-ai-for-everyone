"""
Chapter 1 Exercises: The Agent Loop -- REFERENCE SOLUTION
Scenario: Summit Gear Co-op / GearBot. See starter.py's module docstring
for the full scenario description. This file is the fully filled-in
reference; running it directly scores a perfect total.
"""

import json
import time


GEAR_STOCK = {
    "4-person tent": {"in_stock": True, "quantity": 6},
    "sleeping bag": {"in_stock": True, "quantity": 14},
    "camp stove": {"in_stock": False, "quantity": 0},
}

GEAR_PRICES = {
    "4-person tent": 18.00,
    "sleeping bag": 7.50,
    "camp stove": 5.00,
}


def check_availability(item_name):
    key = item_name.strip().lower()
    return GEAR_STOCK.get(key, {"error": f"no item on file named '{item_name}'"})


def get_rental_price(item_name):
    key = item_name.strip().lower()
    if key not in GEAR_PRICES:
        return {"error": f"no item on file named '{item_name}'"}
    return {"daily_price": GEAR_PRICES[key]}


# Task 1
TASK_1_ANSWERS = {
    "fact_a": "action",
    "fact_b": "reasoning",
    "fact_c": "observation",
    "fact_d": "guard",
    "fact_e": "perception",
}


def score_exercise_1():
    correct = {
        "fact_a": "action",
        "fact_b": "reasoning",
        "fact_c": "observation",
        "fact_d": "guard",
        "fact_e": "perception",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# Task 2
TASK_2_ANSWER = "MORE likely"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "MORE likely" else 0), 1


# Task 3
GET_RETURN_DATE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_return_date",
        "description": "Look up the return due date for a rented item at Summit Gear Co-op.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {"type": "string"}
            },
            "required": ["item_name"],
        },
    },
}


def score_exercise_3():
    points = 0
    fn = GET_RETURN_DATE_SCHEMA.get("function", {})
    if fn.get("name") == "get_return_date":
        points += 1
    desc = (fn.get("description") or "").lower()
    if "return" in desc and ("due" in desc or "date" in desc):
        points += 1
    return points, 2


# Task 4
def normalize_item(name):
    key = name.strip().lower()
    if key.endswith(" rental"):
        key = key[: -len(" rental")]
    return key


def score_exercise_4():
    checks = [
        (normalize_item("camp stove rental") == "camp stove", 1),
        (normalize_item("Sleeping Bag") == "sleeping bag", 1),
        (normalize_item("  4-person tent  ") == "4-person tent", 1),
    ]
    return sum(p for ok, p in checks if ok), sum(p for _, p in checks)


# Task 5
def fake_model_step(iteration):
    return {"tool_calls": [{"name": "check_availability", "args": {"item_name": "camp stove"}}]}


def run_gearbot_loop(max_iterations=3):
    tool_impls = {"check_availability": check_availability, "get_rental_price": get_rental_price}
    trace = []
    for i in range(1, max_iterations + 1):
        step = fake_model_step(i)
        for call in step["tool_calls"]:
            fn = tool_impls[call["name"]]
            result = fn(**call["args"])
            trace.append((call["name"], call["args"], result))
    return None, trace


def score_exercise_5():
    answer, trace = run_gearbot_loop(max_iterations=3)
    points = 0
    if answer is None:
        points += 1
    if len(trace) == 3:
        points += 1
    return points, 2


# Task 6
TASK_6_ANSWER = "hallucinated result despite a real observation"


def score_exercise_6():
    return (1 if TASK_6_ANSWER == "hallucinated result despite a real observation" else 0), 1


# Task 7
def call_with_budget(slow_fn, seconds_budget, *args, **kwargs):
    start = time.monotonic()
    result = slow_fn(*args, **kwargs)
    elapsed = time.monotonic() - start
    if elapsed > seconds_budget:
        raise TimeoutError(f"exceeded {seconds_budget}s budget (took {elapsed:.2f}s)")
    return result


def score_exercise_7():
    def fast():
        return "ok"

    def slow():
        time.sleep(0.15)
        return "ok"

    points = 0
    try:
        assert call_with_budget(fast, 1.0) == "ok"
        points += 1
    except Exception:
        pass
    try:
        call_with_budget(slow, 0.05)
    except TimeoutError:
        points += 1
    except Exception:
        pass
    return points, 2


# Task 8
def score_exercise_8():
    concepts_touched = set(v for v in TASK_1_ANSWERS.values() if v)
    all_five = {"perception", "reasoning", "action", "observation", "guard"}
    points = 1 if concepts_touched == all_five else 0
    return points, 1


def main():
    tasks = [
        ("Task 1: Map failures to loop concepts", score_exercise_1),
        ("Task 2: Loop-dependency reasoning", score_exercise_2),
        ("Task 3 (production-gear): Tool schema", score_exercise_3),
        ("Task 4 (production-gear): Normalize fix", score_exercise_4),
        ("Task 5 (production-gear): Iteration guard", score_exercise_5),
        ("Task 6 (production-gear): Failure diagnosis", score_exercise_6),
        ("Task 7 (production-gear): Timeout budget", score_exercise_7),
        ("Task 8: Completeness check", score_exercise_8),
    ]
    total_earned, total_possible = 0, 0
    print("Chapter 1 Exercises -- Score Report (SOLUTION)")
    print("=" * 50)
    for name, fn in tasks:
        earned, possible = fn()
        total_earned += earned
        total_possible += possible
        print(f"{name}: {earned}/{possible}")
    print("=" * 50)
    print(f"TOTAL: {total_earned}/{total_possible}")


if __name__ == "__main__":
    main()
