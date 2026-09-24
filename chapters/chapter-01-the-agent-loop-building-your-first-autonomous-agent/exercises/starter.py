"""
Chapter 1 Exercises: The Agent Loop
Scenario: Summit Gear Co-op, a fictional camping-gear rental shop.
Their agent, GearBot, answers questions using two tools:
  - check_availability(item_name) -> is a piece of gear in stock today
  - get_rental_price(item_name)   -> the daily rental price of an item

This is a fresh scenario, deliberately different from the lesson's
TrailBot/Northbeam Outdoors hook. The point is applying this chapter's
concepts (the loop, tool schemas, wrong-argument diagnosis, guards,
timeouts) to a system you haven't seen before -- recalling the lesson's
answers by heart will not get you through these.

How to run:
    python3 starter.py
It prints a score report. Fill in each # TODO, re-run, and watch your
score climb toward the total (17 points across 8 tasks).
"""

import json


# ---------------------------------------------------------------------------
# Shared fixtures used by several tasks below -- do not need to be edited.
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Task 1: Map five GearBot failures to the agent-loop concept each is about.
# ---------------------------------------------------------------------------
# For each fact below, GearBot's team observed a real problem. Assign the
# single BEST-matching concept from this list to each fact:
#   "perception", "reasoning", "action", "observation", "guard"
#
# Fact A: GearBot called check_availability but the code never actually
#         invoked the Python function -- it just echoed the model's
#         intended arguments back as if they were the result.
# Fact B: A customer asked about a "camp stove," but GearBot's tool
#         description for check_availability never mentioned it checks
#         stock -- it just said "gear info" -- so GearBot picked the
#         wrong tool (get_rental_price) for an availability question.
# Fact C: GearBot's tool-result message was never appended back into the
#         message history, so on the next turn the model had no idea the
#         tool had already been called.
# Fact D: GearBot kept calling check_availability on the exact same item
#         over and over, forever, because nothing capped the loop.
# Fact E: A tool result correctly came back as {"in_stock": True}, but it
#         was never added to `messages` at all before the next model call.

TASK_1_ANSWERS = {
    "fact_a": None,  # TODO 1: "perception" | "reasoning" | "action" | "observation" | "guard"
    "fact_b": None,  # TODO 2
    "fact_c": None,  # TODO 3
    "fact_d": None,  # TODO 4
    "fact_e": None,  # TODO 5
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


# ---------------------------------------------------------------------------
# Task 2: Loop-dependency reasoning.
# ---------------------------------------------------------------------------
# If Fact C above (observation never appended to messages) is true, does it
# make Fact D (runaway loop) MORE likely, LESS likely, or have NO EFFECT on
# it? Set TASK_2_ANSWER to one of those three exact strings.

TASK_2_ANSWER = None  # TODO 6: "MORE likely" | "LESS likely" | "NO EFFECT"


def score_exercise_2():
    # If the model never sees the tool result, it has no evidence the task
    # is progressing -- it is more likely to keep re-requesting the same
    # tool, since nothing in its context shows the call already happened.
    return (1 if TASK_2_ANSWER == "MORE likely" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): Write a JSON schema for a third tool.
# ---------------------------------------------------------------------------
# Complete GET_RETURN_DATE_SCHEMA so it describes a tool named
# "get_return_date" that takes one required string argument "item_name"
# and whose description mentions it looks up when a rented item is due
# back.

GET_RETURN_DATE_SCHEMA = {
    "type": "function",
    "function": {
        "name": None,        # TODO 7: fill in the tool's name
        "description": None,  # TODO 8: fill in a real description
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


# ---------------------------------------------------------------------------
# Task 4 (production-gear): Fix a wrong-argument bug with a normalize step.
# ---------------------------------------------------------------------------
# A customer asks "is the camp stove available?" and the model calls
# check_availability("camp stove rental") -- adding the word "rental,"
# the same class of bug the lesson's Cedar Hollow example had. Write
# normalize_item() so GEAR_STOCK lookups succeed even with this kind of
# extra wording.

def normalize_item(name):
    # TODO 9: strip a trailing " rental" (and only that suffix) from name,
    # after trimming whitespace and lowercasing, the same pattern the
    # lesson's _normalize() used for " trail"/" loop"/" trailhead".
    return name.strip().lower()


def score_exercise_4():
    checks = [
        (normalize_item("camp stove rental") == "camp stove", 1),
        (normalize_item("Sleeping Bag") == "sleeping bag", 1),
        (normalize_item("  4-person tent  ") == "4-person tent", 1),
    ]
    return sum(p for ok, p in checks if ok), sum(p for _, p in checks)


# ---------------------------------------------------------------------------
# Task 5 (production-gear): Implement the iteration guard.
# ---------------------------------------------------------------------------
# run_gearbot_loop below is missing its guard. Complete it so that if the
# fake model (fake_model_step) never stops requesting tool calls, the loop
# still halts after `max_iterations` iterations and returns None, exactly
# like the lesson's run_agent().

def fake_model_step(iteration):
    """Stands in for a model that never stops asking for a tool call."""
    return {"tool_calls": [{"name": "check_availability", "args": {"item_name": "camp stove"}}]}


def run_gearbot_loop(max_iterations=3):
    tool_impls = {"check_availability": check_availability, "get_rental_price": get_rental_price}
    trace = []
    # TODO 10: write a for-loop over range(1, max_iterations + 1) that
    # calls fake_model_step(i), executes each requested tool call, appends
    # a (tool_name, args, result) tuple to `trace`, and -- because
    # fake_model_step never returns a final answer -- falls through to
    # return (None, trace) once the loop's iterations are exhausted.
    return None, trace


def score_exercise_5():
    answer, trace = run_gearbot_loop(max_iterations=3)
    points = 0
    if answer is None:
        points += 1
    if len(trace) == 3:
        points += 1
    return points, 2


# ---------------------------------------------------------------------------
# Task 6 (production-gear): Diagnose a failure type from a trace.
# ---------------------------------------------------------------------------
# GearBot's log shows this single exchange:
#   User: "How much does the sleeping bag cost per day?"
#   Model calls: check_availability({"item_name": "sleeping bag"})
#   Tool result: {"in_stock": True, "quantity": 14}
#   Model's final answer: "The sleeping bag is $7.50 per day."
# The price shown was never actually looked up -- get_rental_price was
# never called. Name the failure type: "wrong tool choice",
# "wrong argument", or "hallucinated result despite a real observation".

TASK_6_ANSWER = None  # TODO 11: fill in the failure type, exact string from above


def score_exercise_6():
    return (1 if TASK_6_ANSWER == "hallucinated result despite a real observation" else 0), 1


# ---------------------------------------------------------------------------
# Task 7 (production-gear): Add a timeout budget to a model call wrapper.
# ---------------------------------------------------------------------------
# Complete call_with_budget so that it raises TimeoutError if `slow_fn`
# takes longer than `seconds_budget`, mirroring the lesson's
# call_with_budget() pattern (there, wrapping the openai client; here,
# wrapping any function for testability without a live model).

import time


def call_with_budget(slow_fn, seconds_budget, *args, **kwargs):
    start = time.monotonic()
    result = slow_fn(*args, **kwargs)
    elapsed = time.monotonic() - start
    # TODO 12: if elapsed > seconds_budget, raise TimeoutError with a
    # message naming the budget and the elapsed time; otherwise return
    # result.
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


# ---------------------------------------------------------------------------
# Task 8: Full-checklist completeness check.
# ---------------------------------------------------------------------------
# No code to write here -- this just confirms every concept from Tasks 1-7
# was actually touched (all five loop concepts from Task 1, plus the
# schema, normalize, guard, diagnosis, and timeout tasks).

def score_exercise_8():
    concepts_touched = set(v for v in TASK_1_ANSWERS.values() if v)
    all_five = {"perception", "reasoning", "action", "observation", "guard"}
    points = 1 if concepts_touched == all_five else 0
    return points, 1


# ---------------------------------------------------------------------------
# Score report
# ---------------------------------------------------------------------------

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
    print("Chapter 1 Exercises -- Score Report")
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
