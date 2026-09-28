"""
Chapter 3 Exercises: Tool Use and Function Calling -- REFERENCE SOLUTION
Scenario: Thornbury Insurance Group, a fictional auto insurer. Its
agent, ClaimBot, has four tools that plausibly overlap in what they can
explain about a slow claim -- a lapsed policy, a repair-shop delay, or
missing adjuster notes -- and one tool (send_status_update) that always
"succeeds" without meaning the claim is actually resolved. This is a
fresh scenario, deliberately different from the lesson's Palisade
Broadband/NetBot hook. Running this file directly scores a perfect
total.

How to run:
    python3 solution.py
"""

import re
import concurrent.futures


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
# Concepts: "wrong-tool-choice", "argument-formatting drift",
#           "timeout failure", "malformed-output failure",
#           "succeeds-but-wrong-answer failure"
# ---------------------------------------------------------------------------
TASK_1_ANSWERS = {
    "fact_a": "wrong-tool-choice",
    "fact_b": "argument-formatting drift",
    "fact_c": "timeout failure",
    "fact_d": "malformed-output failure",
    "fact_e": "succeeds-but-wrong-answer failure",
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
TASK_2_ANSWER = "MORE likely"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "MORE likely" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): Normalize a policy ID across real format drift.
# ---------------------------------------------------------------------------
def normalize_policy_id(raw):
    digits = re.sub(r"\D", "", raw)
    return f"pol-{digits}" if digits else raw.strip().lower()


def score_exercise_3():
    checks = [
        (normalize_policy_id("POL-4471") == "pol-4471", 1),
        (normalize_policy_id("Policy #4471") == "pol-4471", 1),
    ]
    return sum(p for ok, p in checks if ok), sum(p for _, p in checks)


# ---------------------------------------------------------------------------
# Task 4 (production-gear): Tool-selection function -- check the cheapest,
# most decisive signal (policy status) before the topically-tempting one
# (repair shop status).
# ---------------------------------------------------------------------------
def diagnose_claim_delay(policy_id, claim_id):
    policy = get_policy_details(policy_id)
    if policy.get("status") == "lapsed":
        return "get_policy_details", policy
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
# is often transient.
# ---------------------------------------------------------------------------
def call_repair_status_with_retry(claim_id, simulate_hang=False, max_retries=2, budget_seconds=1):
    for attempt in range(max_retries + 1):
        outcome = call_with_timeout(
            check_repair_shop_status,
            {"claim_id": claim_id, "_simulate_hang": simulate_hang and attempt == 0},
            budget_seconds,
        )
        if outcome["ok"]:
            return outcome["result"], attempt
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
TASK_6_ANSWER = "malformed-output failure"


def score_exercise_6():
    return (1 if TASK_6_ANSWER == "malformed-output failure" else 0), 1


# ---------------------------------------------------------------------------
# Task 7 (production-gear): Outcome-check function for a tool that always
# "succeeds" -- send_status_update never fails, but that doesn't mean the
# claim is actually resolved.
# ---------------------------------------------------------------------------
def verify_resolution(claim_id):
    update = send_status_update(claim_id)
    status = check_repair_shop_status(claim_id)
    resolved = status.get("shop_status") == "completed"
    return {"update": update, "resolved": resolved}


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
def score_exercise_8():
    concepts_touched = set(v for v in TASK_1_ANSWERS.values() if v)
    all_five = {
        "wrong-tool-choice", "argument-formatting drift", "timeout failure",
        "malformed-output failure", "succeeds-but-wrong-answer failure",
    }
    points = 1 if concepts_touched == all_five else 0
    return points, 1


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
    print("Chapter 3 Exercises -- Score Report (SOLUTION)")
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
