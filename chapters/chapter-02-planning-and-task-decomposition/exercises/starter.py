"""
Chapter 2 Exercises: Planning and Task Decomposition
Scenario: Pinehurst Realty Group, a fictional residential brokerage. Its
agent, ListBot, handles two kinds of task: listing a new property (a
fixed, up-front plan -- verify the address, pull comps, publish) and
diagnosing why a showing fell through (an emergent, one-step-at-a-time
investigation -- the right follow-up check depends on what the showing
log actually says).

This is a fresh scenario, deliberately different from the lesson's
Alderleaf Research Group/ScoutBot hook. The point is applying this
chapter's planning concepts (fixed vs. emergent, re-planning, wrong-plan
failures, planning guards) to a system you haven't seen before.

How to run:
    python3 starter.py
It prints a score report. Fill in each # TODO, re-run, and watch your
score climb toward the total (16 points across 8 tasks).
"""

import json


# ---------------------------------------------------------------------------
# Shared fixtures used by several tasks below -- do not need to be edited.
# ---------------------------------------------------------------------------

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
# ---------------------------------------------------------------------------
# For each fact below, ListBot's team observed a real situation. Assign the
# single BEST-matching concept from this list to each fact:
#   "fixed plan", "emergent plan", "re-planning", "wrong-plan failure",
#   "planning guard"
#
# Fact A: Before touching any tool, ListBot decided the complete ordered
#         sequence -- verify_address, then get_comps, then publish_listing
#         -- in one reasoning step, and never revisited that order.
# Fact B: Every tool call in a listing plan succeeded, but the plan itself
#         scheduled an open house before checking the showing log, which
#         already showed the buyer's financing had fallen through --
#         the open house wasn't useful, even though nothing errored.
# Fact C: After verify_address failed on a typo'd address, ListBot threw
#         out the whole plan and rebuilt it from scratch with a corrected
#         address, then re-ran all three steps.
# Fact D: Diagnosing a fallen-through showing, ListBot checked the showing
#         log first, then decided its NEXT check (financing vs. inspection)
#         only after reading what the log's notes actually said.
# Fact E: ListBot capped how many times it would rebuild and re-run a
#         failing plan at 2 attempts, after which it stopped and flagged
#         a human instead of retrying forever.

TASK_1_ANSWERS = {
    "fact_a": None,  # TODO 1
    "fact_b": None,  # TODO 2
    "fact_c": None,  # TODO 3
    "fact_d": None,  # TODO 4
    "fact_e": None,  # TODO 5
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
# If a fixed plan for the showing-diagnosis task pre-committed to checking
# buyer financing as step 2, BEFORE reading the showing log's notes in step
# 1, does that make a wrong-plan failure MORE likely, LESS likely, or have
# NO EFFECT? Set TASK_2_ANSWER to one of those three exact strings.

TASK_2_ANSWER = None  # TODO 6: "MORE likely" | "LESS likely" | "NO EFFECT"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "MORE likely" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): Write a fixed, up-front plan.
# ---------------------------------------------------------------------------
# Complete FIXED_LISTING_PLAN as a list of {"step": n, "tool": name} dicts
# for listing a new property: verify the address FIRST, then pull comps,
# then publish -- in that exact order. (generate_listing_copy is
# intentionally left out of this plan -- Task 3 only grades the 3-step
# skeleton.)

FIXED_LISTING_PLAN = [
    # TODO 7: fill in three dicts, in order:
    #   {"step": 1, "tool": "verify_address"},
    #   {"step": 2, "tool": "get_comps"},
    #   {"step": 3, "tool": "publish_listing"},
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
# ---------------------------------------------------------------------------
# A model asked to verify "142 Birchwood Ln (Unit A)" -- ADDRESS_DATA's key
# is exactly "142 birchwood ln", no unit suffix. Write normalize_address()
# so the lookup succeeds despite this kind of extra wording, the same
# pattern the lesson's re-planning section used for a typo'd company name.

def normalize_address(address):
    # TODO 8: strip a trailing " (unit a)" or " unit a" (case-insensitive
    # after lowercasing) from address, after trimming whitespace and
    # lowercasing.
    return address.strip().lower()


def score_exercise_4():
    checks = [
        (normalize_address("142 Birchwood Ln (Unit A)") == "142 birchwood ln", 1),
        (normalize_address("  88 Harmon Ct  ") == "88 harmon ct", 1),
    ]
    return sum(p for ok, p in checks if ok), sum(p for _, p in checks)


# ---------------------------------------------------------------------------
# Task 5 (production-gear): Implement the emergent decision function.
# ---------------------------------------------------------------------------
# The right follow-up check after get_showing_log depends entirely on what
# the log's notes actually say -- this cannot be a fixed plan, the same
# reason the lesson's stock-drop investigation needed emergent planning.
# Complete decide_next_showing_step() so that:
#   - with no history yet, it returns "get_showing_log"
#   - after get_showing_log, if notes mention "financing", it returns
#     "check_buyer_financing"
#   - after get_showing_log, if notes mention "inspection", it returns
#     "get_inspection_report"
#   - otherwise (or after any other step), it returns None (stop)

def decide_next_showing_step(history):
    if not history:
        return "get_showing_log"
    last_tool, last_result = history[-1]
    if last_tool == "get_showing_log":
        notes = last_result.get("notes", "").lower()
        # TODO 9: return "check_buyer_financing" if "financing" in notes,
        # "get_inspection_report" if "inspection" in notes, else None.
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
# financing had fallen through, meaning an open house wasn't the useful
# next action at all. Every tool call that DID run succeeded. Name the
# failure: "wrong tool choice", "wrong argument", or "wrong-plan failure".

TASK_6_ANSWER = None  # TODO 10: fill in the failure type, exact string from above


def score_exercise_6():
    return (1 if TASK_6_ANSWER == "wrong-plan failure" else 0), 1


# ---------------------------------------------------------------------------
# Task 7 (production-gear): Implement a re-plan guard bounded by max_replans.
# ---------------------------------------------------------------------------
# Complete run_fixed_listing_with_guard so that if verify_address keeps
# failing, it retries with `correction` up to max_replans times and then
# gives up cleanly -- mirroring the lesson's run_fixed_plan_with_replan_guard.

def run_fixed_listing_with_guard(address, max_replans=2, correction=None):
    name = address
    for attempt in range(max_replans + 1):
        result = verify_address(name)
        if "error" not in result:
            return result, attempt
        # TODO 11: if correction is None or attempt >= max_replans, return
        # (None, attempt). Otherwise, set name = correction and continue
        # the loop for another attempt.
        return None, attempt
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
# No code to write here -- this just confirms every concept from Task 1
# was actually touched (all five planning concepts).

def score_exercise_8():
    concepts_touched = set(v for v in TASK_1_ANSWERS.values() if v)
    all_five = {"fixed plan", "wrong-plan failure", "re-planning", "emergent plan", "planning guard"}
    points = 1 if concepts_touched == all_five else 0
    return points, 1


# ---------------------------------------------------------------------------
# Score report
# ---------------------------------------------------------------------------

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
    print("Chapter 2 Exercises -- Score Report")
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
