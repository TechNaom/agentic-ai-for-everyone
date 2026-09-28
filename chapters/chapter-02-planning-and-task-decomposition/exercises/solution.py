"""
Chapter 2 Exercises: Planning and Task Decomposition -- REFERENCE SOLUTION
Scenario: Pinehurst Realty Group, a fictional residential brokerage. Its
agent, ListBot, handles two kinds of task: listing a new property (a
fixed, up-front plan -- verify the address, pull comps, publish) and
diagnosing why a showing fell through (an emergent, one-step-at-a-time
investigation -- the right follow-up check depends on what the showing
log actually says). This is a fresh scenario, deliberately different
from the lesson's Alderleaf Research Group/ScoutBot hook. Running this
file directly scores a perfect total.

How to run:
    python3 solution.py
"""

import json


ADDRESS_DATA = {
    "142 birchwood ln": {"verified": True, "zip": "27510"},
    "88 harmon ct": {"verified": True, "zip": "27513"},
}
COMPS_DATA = {
    "142 birchwood ln": {"comp_avg_price": 412000},
    "88 harmon ct": {"comp_avg_price": 298000},
}
SHOWING_LOG = {
    "142 birchwood ln": {"outcome": "fell_through", "notes": "buyer's financing fell through last minute"},
    "88 harmon ct": {"outcome": "fell_through", "notes": "inspection revealed foundation cracks"},
}
BUYER_FINANCING = {"142 birchwood ln": {"preapproved": False}}
INSPECTION_REPORTS = {"88 harmon ct": {"issues_found": ["foundation cracks", "roof age"]}}


def verify_address(address):
    return ADDRESS_DATA.get(address.strip().lower(), {"error": f"no record for '{address}'"})


def get_comps(address):
    return COMPS_DATA.get(address.strip().lower(), {"error": f"no comps for '{address}'"})


def generate_listing_copy(address, comp_avg_price):
    return {"copy": f"Charming home at {address}, priced near ${comp_avg_price:,}."}


def publish_listing(address):
    return {"published": True, "address": address}


def get_showing_log(address):
    return SHOWING_LOG.get(address.strip().lower(), {"error": f"no showing log for '{address}'"})


def check_buyer_financing(address):
    return BUYER_FINANCING.get(address.strip().lower(), {"error": f"no financing record for '{address}'"})


def get_inspection_report(address):
    return INSPECTION_REPORTS.get(address.strip().lower(), {"error": f"no inspection report for '{address}'"})


TOOL_IMPLS = {
    "verify_address": verify_address,
    "get_comps": get_comps,
    "publish_listing": publish_listing,
    "get_showing_log": get_showing_log,
    "check_buyer_financing": check_buyer_financing,
    "get_inspection_report": get_inspection_report,
}


# ---------------------------------------------------------------------------
# Task 1: Map five ListBot facts to the planning concept each is about.
# Concepts: "fixed plan", "emergent plan", "re-planning",
#           "wrong-plan failure", "planning guard"
# ---------------------------------------------------------------------------
TASK_1_ANSWERS = {
    "fact_a": "fixed plan",
    "fact_b": "wrong-plan failure",
    "fact_c": "re-planning",
    "fact_d": "emergent plan",
    "fact_e": "planning guard",
}


def score_exercise_1():
    correct = {
        "fact_a": "fixed plan",
        "fact_b": "wrong-plan failure",
        "fact_c": "re-planning",
        "fact_d": "emergent plan",
        "fact_e": "planning guard",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Dependency reasoning.
# ---------------------------------------------------------------------------
TASK_2_ANSWER = "MORE likely"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "MORE likely" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): Write a fixed, up-front plan for listing a
# property: verify the address, pull comps, then publish -- in that order.
# ---------------------------------------------------------------------------
FIXED_LISTING_PLAN = [
    {"step": 1, "tool": "verify_address"},
    {"step": 2, "tool": "get_comps"},
    {"step": 3, "tool": "publish_listing"},
]


def score_exercise_3():
    names = [item.get("tool") for item in FIXED_LISTING_PLAN]
    points = 0
    if names and names[0] == "verify_address":
        points += 1
    if "get_comps" in names and "publish_listing" in names:
        points += 1
    return points, 2


# ---------------------------------------------------------------------------
# Task 4 (production-gear): Fix a wrong-argument bug with a normalize step.
# A model asked to verify "142 Birchwood Ln (Unit A)" -- ADDRESS_DATA's key
# is exactly "142 birchwood ln", no unit suffix.
# ---------------------------------------------------------------------------
def normalize_address(address):
    key = address.strip().lower()
    for suffix in (" (unit a)", " unit a"):
        if key.endswith(suffix):
            key = key[: -len(suffix)]
    return key


def score_exercise_4():
    checks = [
        (normalize_address("142 Birchwood Ln (Unit A)") == "142 birchwood ln", 1),
        (normalize_address("  88 Harmon Ct  ") == "88 harmon ct", 1),
    ]
    return sum(p for ok, p in checks if ok), sum(p for _, p in checks)


# ---------------------------------------------------------------------------
# Task 5 (production-gear): Implement the emergent decision function.
# The right follow-up check after get_showing_log depends entirely on what
# the log's notes actually say -- this cannot be a fixed plan.
# ---------------------------------------------------------------------------
def decide_next_showing_step(history):
    if not history:
        return "get_showing_log"
    last_tool, last_result = history[-1]
    if last_tool == "get_showing_log":
        notes = last_result.get("notes", "").lower()
        if "financing" in notes:
            return "check_buyer_financing"
        if "inspection" in notes:
            return "get_inspection_report"
        return None
    return None


def run_emergent_diagnosis(address, max_iterations=3):
    history = []
    for _ in range(max_iterations):
        next_tool = decide_next_showing_step(history)
        if next_tool is None:
            break
        result = TOOL_IMPLS[next_tool](address)
        history.append((next_tool, result))
    return history


def score_exercise_5():
    h1 = run_emergent_diagnosis("142 Birchwood Ln")
    h2 = run_emergent_diagnosis("88 Harmon Ct")
    points = 0
    if len(h1) == 2 and h1[1][0] == "check_buyer_financing":
        points += 1
    if len(h2) == 2 and h2[1][0] == "get_inspection_report":
        points += 1
    return points, 2


# ---------------------------------------------------------------------------
# Task 6 (production-gear): Diagnose a failure type from a trace.
# ---------------------------------------------------------------------------
# ListBot's log for 142 Birchwood Ln shows: verify_address succeeded,
# get_comps succeeded, but the plan's 3rd step (pre-committed before either
# result was known) was "schedule_open_house" -- even though the showing
# log (never checked by this fixed plan) already showed the buyer's
# financing fell through, meaning an open house wasn't the useful next
# action at all. Every tool call that DID run succeeded. Name the failure:
# "wrong tool choice", "wrong argument", or "wrong-plan failure".
TASK_6_ANSWER = "wrong-plan failure"


def score_exercise_6():
    return (1 if TASK_6_ANSWER == "wrong-plan failure" else 0), 1


# ---------------------------------------------------------------------------
# Task 7 (production-gear): Implement a re-plan guard bounded by max_replans.
# ---------------------------------------------------------------------------
def run_fixed_listing_with_guard(address, max_replans=2, correction=None):
    name = address
    for attempt in range(max_replans + 1):
        result = verify_address(name)
        if "error" not in result:
            return result, attempt
        if correction is None or attempt >= max_replans:
            return None, attempt
        name = correction
    return None, max_replans


def score_exercise_7():
    points = 0
    result, attempts = run_fixed_listing_with_guard("142 Birchwod Ln", correction="142 Birchwood Ln")
    if result is not None and attempts == 1:
        points += 1
    result2, attempts2 = run_fixed_listing_with_guard("Nowhere Ave", correction=None, max_replans=2)
    if result2 is None and attempts2 <= 2:
        points += 1
    return points, 2


# ---------------------------------------------------------------------------
# Task 8: Full-checklist completeness check.
# ---------------------------------------------------------------------------
def score_exercise_8():
    concepts_touched = set(v for v in TASK_1_ANSWERS.values() if v)
    all_five = {"fixed plan", "wrong-plan failure", "re-planning", "emergent plan", "planning guard"}
    points = 1 if concepts_touched == all_five else 0
    return points, 1


def main():
    tasks = [
        ("Task 1: Map facts to planning concepts", score_exercise_1),
        ("Task 2: Dependency reasoning", score_exercise_2),
        ("Task 3 (production-gear): Fixed plan", score_exercise_3),
        ("Task 4 (production-gear): Normalize fix", score_exercise_4),
        ("Task 5 (production-gear): Emergent decision fn", score_exercise_5),
        ("Task 6 (production-gear): Failure diagnosis", score_exercise_6),
        ("Task 7 (production-gear): Replan guard", score_exercise_7),
        ("Task 8: Completeness check", score_exercise_8),
    ]
    total_earned, total_possible = 0, 0
    print("Chapter 2 Exercises -- Score Report (SOLUTION)")
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
