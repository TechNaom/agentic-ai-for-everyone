"""
Chapter 3 Exercises: Tool Use and Function Calling
Scenario: Thornbury Insurance Group, a fictional auto insurer. Its
agent, ClaimBot, has four tools that plausibly overlap in what they can
explain about a slow claim -- a lapsed policy, a repair-shop delay, or
missing adjuster notes -- and one tool (send_status_update) that always
"succeeds" without meaning the claim is actually resolved.

This is a fresh scenario, deliberately different from the lesson's
Palisade Broadband/NetBot hook. The point is applying this chapter's
concepts (tool selection among overlapping candidates, argument-
formatting drift, and differentiated failure/retry handling) to a
system you haven't seen before.

How to run:
    python3 starter.py
It prints a score report. Fill in each # TODO, re-run, and watch your
score climb toward the total (16 points across 8 tasks).
"""

import re
import concurrent.futures


# ---------------------------------------------------------------------------
# Shared fixtures used by several tasks below -- do not need to be edited.
# ---------------------------------------------------------------------------

POLICIES = {
    "pol-4471": {"status": "lapsed", "coverage": "full"},
    "pol-8823": {"status": "active", "coverage": "full"},
}
REPAIR_SHOP_STATUS = {
    "cl-501": {"shop_status": "in_progress", "eta_days": 5},
    "cl-902": {"shop_status": "completed", "eta_days": 0},
}
ADJUSTER_NOTES = {
    "cl-501": {"notes": "waiting on parts"},
}


def get_policy_details(policy_id):
    return POLICIES.get(policy_id.strip().lower(), {"error": f"no policy on file for '{policy_id}'"})


def check_repair_shop_status(claim_id, _simulate_hang=False):
    import time
    if _simulate_hang:
        time.sleep(3)
    return REPAIR_SHOP_STATUS.get(claim_id.strip().lower(), {"error": f"no repair shop status for '{claim_id}'"})


def get_adjuster_notes(claim_id):
    key = claim_id.strip().lower()
    if key == "cl-999":
        return "ERR: claim not found in legacy adjuster system"  # malformed -- not a dict
    return ADJUSTER_NOTES.get(key, {"error": f"no adjuster notes for '{claim_id}'"})


def send_status_update(claim_id):
    return {"sent": True, "claim_id": claim_id}


TOOL_IMPLS = {
    "get_policy_details": get_policy_details,
    "check_repair_shop_status": check_repair_shop_status,
    "get_adjuster_notes": get_adjuster_notes,
    "send_status_update": send_status_update,
}


def call_with_timeout(fn, kwargs, budget_seconds):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(fn, **kwargs)
        try:
            return {"ok": True, "result": future.result(timeout=budget_seconds)}
        except concurrent.futures.TimeoutError:
            return {"ok": False, "failure_type": "timeout"}


# ---------------------------------------------------------------------------
# Task 1: Map five ClaimBot facts to the concept each is about.
# ---------------------------------------------------------------------------
# For each fact below, ClaimBot's team observed a real situation. Assign the
# single BEST-matching concept from this list to each fact:
#   "wrong-tool-choice", "argument-formatting drift", "timeout failure",
#   "malformed-output failure", "succeeds-but-wrong-answer failure"
#
# Fact A: ClaimBot called check_repair_shop_status first because "claim" and
#         "shop" seemed topically related to the customer's wording, without
#         first checking get_policy_details -- even though a lapsed policy
#         would have explained the delay immediately and more cheaply.
# Fact B: ClaimBot received policy IDs in four different formats
#         ("POL-4471", "pol4471", "Policy #4471", "4471") and needed one
#         normalize step to resolve all of them to the same lookup key.
# Fact C: check_repair_shop_status hung past the configured budget on one
#         call, and ClaimBot's wrapper had to give up and report a timeout
#         rather than waiting indefinitely.
# Fact D: A legacy adjuster-notes endpoint returned a raw string instead of
#         the expected dict shape when a claim id wasn't found, and code
#         downstream that assumed a dict crashed until a defensive check
#         was added.
# Fact E: send_status_update(claim_id) returned {"sent": True} every time,
#         even for a claim whose underlying repair delay was never actually
#         resolved -- a clean success that didn't mean the customer's
#         problem was solved.

TASK_1_ANSWERS = {
    "fact_a": None,  # TODO 1
    "fact_b": None,  # TODO 2
    "fact_c": None,  # TODO 3
    "fact_d": None,  # TODO 4
    "fact_e": None,  # TODO 5
}


def score_exercise_1():
    correct = {
        "fact_a": "wrong-tool-choice",
        "fact_b": "argument-formatting drift",
        "fact_c": "timeout failure",
        "fact_d": "malformed-output failure",
        "fact_e": "succeeds-but-wrong-answer failure",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Dependency reasoning.
# ---------------------------------------------------------------------------
# If ClaimBot always calls the tool whose name sounds most topically related
# to the customer's wording, instead of checking the cheapest, most decisive
# signal first, does that make a wrong-tool-choice failure MORE likely, LESS
# likely, or have NO EFFECT? Set TASK_2_ANSWER to one of those three exact
# strings.

TASK_2_ANSWER = None  # TODO 6: "MORE likely" | "LESS likely" | "NO EFFECT"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "MORE likely" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): Normalize a policy ID across real format drift.
# ---------------------------------------------------------------------------
# Write normalize_policy_id() so that "POL-4471", "Policy #4471", "pol4471",
# and "4471" all resolve to the canonical key "pol-4471" -- the same
# beyond-strip-and-lower pattern the lesson's normalize_account_id() used.

def normalize_policy_id(raw):
    # TODO 7: extract only the digits from `raw` (re.sub(r"\D", "", raw))
    # and return f"pol-{digits}" if any digits were found, else
    # raw.strip().lower().
    return raw.strip().lower()


def score_exercise_3():
    checks = [
        (normalize_policy_id("POL-4471") == "pol-4471", 1),
        (normalize_policy_id("Policy #4471") == "pol-4471", 1),
    ]
    return sum(p for ok, p in checks if ok), sum(p for _, p in checks)


# ---------------------------------------------------------------------------
# Task 4 (production-gear): Tool-selection function.
# ---------------------------------------------------------------------------
# Complete diagnose_claim_delay() so it checks the cheapest, most decisive
# signal FIRST: if the policy is lapsed, that alone explains the delay --
# return ("get_policy_details", policy) without ever touching the repair
# shop. Only if the policy is NOT lapsed should it fall through to
# check_repair_shop_status.

def diagnose_claim_delay(policy_id, claim_id):
    policy = get_policy_details(policy_id)
    # TODO 8: if policy.get("status") == "lapsed", return
    # ("get_policy_details", policy). Otherwise, return
    # ("check_repair_shop_status", check_repair_shop_status(claim_id)).
    return "check_repair_shop_status", check_repair_shop_status(claim_id)


def score_exercise_4():
    points = 0
    tool1, _ = diagnose_claim_delay("pol-4471", "cl-501")
    if tool1 == "get_policy_details":
        points += 1
    tool2, _ = diagnose_claim_delay("pol-8823", "cl-501")
    if tool2 == "check_repair_shop_status":
        points += 1
    return points, 2


# ---------------------------------------------------------------------------
# Task 5 (production-gear): Timeout failure policy -- retry, since a hang
# is often transient (unlike a malformed-output failure, which never gets
# fixed by retrying the same call).
# ---------------------------------------------------------------------------
def call_repair_status_with_retry(claim_id, simulate_hang=False, max_retries=2, budget_seconds=1):
    # TODO 9: for attempt in range(max_retries + 1): call call_with_timeout()
    # against check_repair_shop_status with kwargs {"claim_id": claim_id,
    # "_simulate_hang": simulate_hang and attempt == 0} and budget_seconds.
    # If outcome["ok"], return (outcome["result"], attempt). If every
    # attempt times out, return (None, max_retries).
    return None, max_retries


def score_exercise_5():
    points = 0
    result1, attempts1 = call_repair_status_with_retry("cl-501", simulate_hang=True)
    if result1 is not None and attempts1 == 1:
        points += 1
    result2, attempts2 = call_repair_status_with_retry("cl-902", simulate_hang=False)
    if result2 is not None and attempts2 == 0:
        points += 1
    return points, 2


# ---------------------------------------------------------------------------
# Task 6 (production-gear): Diagnose a failure type from a trace.
# ---------------------------------------------------------------------------
# ClaimBot called get_adjuster_notes("cl-999") and got back the raw string
# "ERR: claim not found in legacy adjuster system" instead of the dict
# shape every other tool returns -- code downstream that assumed a dict
# crashed with an AttributeError until a defensive isinstance() check was
# added. Name the failure: "timeout failure", "malformed-output failure",
# or "succeeds-but-wrong-answer failure".

TASK_6_ANSWER = None  # TODO 10: fill in the failure type, exact string from above


def score_exercise_6():
    return (1 if TASK_6_ANSWER == "malformed-output failure" else 0), 1


# ---------------------------------------------------------------------------
# Task 7 (production-gear): Outcome-check function.
# ---------------------------------------------------------------------------
# send_status_update() always "succeeds" -- it never returns an error. The
# only way to know whether a claim is ACTUALLY resolved is to check
# independent evidence (the repair shop's real status), the same discipline
# the lesson's restart_modem_with_outcome_check() used.

def verify_resolution(claim_id):
    update = send_status_update(claim_id)
    status = check_repair_shop_status(claim_id)
    # TODO 11: set resolved = True only if status.get("shop_status") ==
    # "completed". Return {"update": update, "resolved": resolved}.
    return {"update": update, "resolved": False}


def score_exercise_7():
    points = 0
    r1 = verify_resolution("cl-902")
    if r1["resolved"] is True:
        points += 1
    r2 = verify_resolution("cl-501")
    if r2["resolved"] is False:
        points += 1
    return points, 2


# ---------------------------------------------------------------------------
# Task 8: Full-checklist completeness check.
# ---------------------------------------------------------------------------
# No code to write here -- this just confirms every concept from Task 1
# was actually touched (all five tool-failure concepts).

def score_exercise_8():
    concepts_touched = set(v for v in TASK_1_ANSWERS.values() if v)
    all_five = {
        "wrong-tool-choice", "argument-formatting drift", "timeout failure",
        "malformed-output failure", "succeeds-but-wrong-answer failure",
    }
    points = 1 if concepts_touched == all_five else 0
    return points, 1


# ---------------------------------------------------------------------------
# Score report
# ---------------------------------------------------------------------------

def main():
    tasks = [
        ("Task 1: Map facts to tool-failure concepts", score_exercise_1),
        ("Task 2: Dependency reasoning", score_exercise_2),
        ("Task 3 (production-gear): Normalize policy ID", score_exercise_3),
        ("Task 4 (production-gear): Tool-selection function", score_exercise_4),
        ("Task 5 (production-gear): Timeout retry policy", score_exercise_5),
        ("Task 6 (production-gear): Failure diagnosis", score_exercise_6),
        ("Task 7 (production-gear): Outcome-check function", score_exercise_7),
        ("Task 8: Completeness check", score_exercise_8),
    ]
    total_earned, total_possible = 0, 0
    print("Chapter 3 Exercises -- Score Report")
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
