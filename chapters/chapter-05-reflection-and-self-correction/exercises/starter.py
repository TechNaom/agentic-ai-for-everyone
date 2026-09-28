"""
Chapter 5 Exercises: Reflection and Self-Correction
Scenario: Fenwick Home Repair Co-op, a fictional handyman referral
service. Its estimate agent, RepairBot, drafts a price quote (hours
times an hourly rate, plus parts) for a repair job, and must also flag
jobs that legally require a licensed technician (gas lines, electrical
panels) rather than quoting them as ordinary handyman work.

This is a fresh scenario, deliberately different from the lesson's
Briarcliff Bike Rentals/BikeBot hook. The point is applying this
chapter's concepts (a draft pass, a grounded verification step, a
revise-the-answer correction, an iteration bound) to a system you
haven't seen before.

How to run:
    python3 starter.py
It prints a score report. Fill in each # TODO, re-run, and watch your
score climb toward the total (18 points across 8 tasks).
"""

import re

RATE_PER_HOUR = 65  # dollars, flat labor rate
LICENSED_ONLY_KEYWORDS = ["gas line", "electrical panel", "gas leak", "breaker panel"]


def compute_price(hours, parts_cost):
    return RATE_PER_HOUR * hours + parts_cost


def extract_dollar_amount(text):
    m = re.search(r"\$(\d+(?:\.\d{1,2})?)", text)
    return float(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Task 1: Map five RepairBot facts to the single BEST-matching reflection
# concept from this list:
#   "first-pass draft (no reflection)", "reflection step (self-critique)",
#   "grounded verification criteria", "revise-the-answer correction",
#   "iteration bound (max reflections)"
#
# Fact A: RepairBot's very first pass at a quote, produced before any check
#         runs against it at all.
# Fact B: A second, separate function call that evaluates the first draft
#         against a standard before it's returned to the customer.
# Fact C: compute_price(hours, parts_cost), re-derived independently of
#         whatever the draft happens to say, used to check the draft's
#         stated number.
# Fact D: When the check in Fact B finds the draft's price is wrong,
#         RepairBot replaces the wrong number with the correct one before
#         responding.
# Fact E: RepairBot stops retrying after 2 failed correction attempts and
#         escalates to a human instead of looping forever.
# ---------------------------------------------------------------------------

TASK_1_ANSWERS = {
    "fact_a": None,  # TODO 1
    "fact_b": None,  # TODO 2
    "fact_c": None,  # TODO 3
    "fact_d": None,  # TODO 4
    "fact_e": None,  # TODO 5
}


def score_exercise_1():
    correct = {
        "fact_a": "first-pass draft (no reflection)",
        "fact_b": "reflection step (self-critique)",
        "fact_c": "grounded verification criteria",
        "fact_d": "revise-the-answer correction",
        "fact_e": "iteration bound (max reflections)",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Dependency reasoning.
# ---------------------------------------------------------------------------
# If reflection is applied to EVERY single request regardless of stakes
# (a trivial, obviously-correct request gets the same extra model call as a
# high-stakes one), does the average cost-per-request become MORE likely,
# LESS likely, or have NO EFFECT on increasing unnecessarily?

TASK_2_ANSWER = None  # TODO 6: "MORE likely" | "LESS likely" | "NO EFFECT"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "MORE likely" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): grounded price verifier.
# ---------------------------------------------------------------------------
# Return True if the draft states a dollar amount AND it equals
# compute_price(hours, parts_cost), else False.

def verify_price(draft_text, hours, parts_cost):
    # TODO 7: implement the check described above.
    return False


def score_exercise_3():
    points = 0
    if verify_price("That job comes to $195 total.", 2, 65) is True:
        points += 1
    if verify_price("That job comes to $150 total.", 2, 65) is False:
        points += 1
    return points, 2


# ---------------------------------------------------------------------------
# Task 4 (production-gear): licensed-referral policy check.
# ---------------------------------------------------------------------------

def requires_licensed_referral(job_description):
    # TODO 8: return True if job_description (lowercased) contains any
    # phrase from LICENSED_ONLY_KEYWORDS, else False.
    return False


def draft_mentions_referral(draft_text):
    # TODO 9: return True if draft_text (lowercased) contains any of:
    # "licensed", "technician", "referral", "cannot quote", "unable to quote".
    return False


def score_exercise_4():
    points = 0
    if requires_licensed_referral("Fix a gas line leak in the kitchen") is True:
        points += 1
    if requires_licensed_referral("Patch drywall in the hallway") is False:
        points += 1
    if draft_mentions_referral("This requires a licensed technician -- I can't quote it directly.") is True:
        points += 1
    return points, 3


# ---------------------------------------------------------------------------
# Task 5 (production-gear): reflect_and_revise -- compose both checks.
# ---------------------------------------------------------------------------
def reflect_and_revise(draft_text, job_description, hours, parts_cost):
    """
    1. correct_price = compute_price(hours, parts_cost).
    2. needs_referral = requires_licensed_referral(job_description).
    3. referral_ok = (not needs_referral) or draft_mentions_referral(draft_text).
    4. stated_price = extract_dollar_amount(draft_text).
    5. If needs_referral AND referral_ok AND stated_price is None: price_ok
       = True (a response that appropriately declines to quote a
       licensed-only job doesn't need a price). Otherwise price_ok =
       verify_price(draft_text, hours, parts_cost).
    6. If price_ok and referral_ok: return (draft_text, False) -- unchanged.
    7. Otherwise, build `revised` starting from draft_text: if not price_ok,
       set revised = f"Corrected estimate: ${correct_price} for {hours}
       hour(s) of labor plus parts." If needs_referral and
       draft_mentions_referral(revised) is False, append " This job involves
       work that requires a licensed technician -- please treat this as a
       referral, not a DIY quote." to revised. Return (revised, True).
    """
    # TODO 10: implement the composed reflect-and-revise logic above.
    return draft_text, False


def score_exercise_5():
    points = 0
    revised, changed = reflect_and_revise("That'll be $100 total.", "Patch drywall", 2, 65)
    if changed and "195" in revised:
        points += 1
    revised2, changed2 = reflect_and_revise("That's $195 total.", "Fix a gas line leak", 2, 65)
    if changed2 and "licensed" in revised2.lower():
        points += 1
    good = "This requires a licensed technician, so I can't quote it directly."
    revised3, changed3 = reflect_and_revise(good, "Fix a gas line leak", 2, 65)
    if not changed3 and revised3 == good:
        points += 1
    return points, 3


# ---------------------------------------------------------------------------
# Task 6 (production-gear): Diagnose a failure type from a trace.
# ---------------------------------------------------------------------------
# RepairBot's first draft quoted $100 for a 2-hour drywall job. Instead of
# checking that number against compute_price(), the "reflection" step just
# re-asked the model the exact same question a second time and got $110 --
# still wrong (should be $130), and different only because of randomness.
# Name this failure using this chapter's exact vocabulary.

TASK_6_ANSWER = None  # TODO 11: fill in the exact concept string


def score_exercise_6():
    return (1 if TASK_6_ANSWER == "retry is not reflection" else 0), 1


# ---------------------------------------------------------------------------
# Task 7 (production-gear): a bounded reflect loop.
# ---------------------------------------------------------------------------
def bounded_reflect_loop(draft_text, job_description, hours, parts_cost, max_reflections=2):
    """
    Call reflect_and_revise() up to max_reflections times. If a call returns
    changed=False, return (attempt, i, False) immediately -- it converged.
    If the loop runs out of attempts, check once more whether the final
    attempt is actually correct (price_ok and referral_ok, same logic as
    inside reflect_and_revise); if so return (attempt, max_reflections,
    False), otherwise return ("This estimate needs a human to review before
    it's sent.", max_reflections, True) -- escalate rather than loop
    forever.
    """
    attempt = draft_text
    for i in range(max_reflections):
        # TODO 12: call reflect_and_revise and return early if converged.
        pass
    # TODO 12 (cont.): final check + escalate if still wrong.
    return "This estimate needs a human to review before it's sent.", max_reflections, True


def score_exercise_7():
    points = 0
    result, attempts, escalated = bounded_reflect_loop("That'll be $100 total.", "Patch drywall", 2, 65)
    if not escalated and attempts <= 2 and "195" in result:
        points += 1

    def stubborn_reflect(*args, **kwargs):
        return "That'll be $999 total.", True
    original = reflect_and_revise
    try:
        globals()["reflect_and_revise"] = stubborn_reflect
        result2, attempts2, escalated2 = bounded_reflect_loop("That'll be $999 total.", "Patch drywall", 2, 65, max_reflections=2)
        if escalated2 and attempts2 == 2:
            points += 1
    finally:
        globals()["reflect_and_revise"] = original
    return points, 2


# ---------------------------------------------------------------------------
# Task 8: Full-checklist completeness check.
# ---------------------------------------------------------------------------
def score_exercise_8():
    concepts_touched = set(v for v in TASK_1_ANSWERS.values() if v)
    all_five = {
        "first-pass draft (no reflection)", "reflection step (self-critique)",
        "grounded verification criteria", "revise-the-answer correction",
        "iteration bound (max reflections)",
    }
    points = 1 if concepts_touched == all_five else 0
    return points, 1


# ---------------------------------------------------------------------------
# Score report
# ---------------------------------------------------------------------------

def main():
    tasks = [
        ("Task 1: Map facts to reflection concepts", score_exercise_1),
        ("Task 2: Dependency reasoning", score_exercise_2),
        ("Task 3 (production-gear): Grounded price verifier", score_exercise_3),
        ("Task 4 (production-gear): Licensed-referral policy check", score_exercise_4),
        ("Task 5 (production-gear): reflect_and_revise composition", score_exercise_5),
        ("Task 6 (production-gear): Failure diagnosis", score_exercise_6),
        ("Task 7 (production-gear): Bounded reflect loop", score_exercise_7),
        ("Task 8: Completeness check", score_exercise_8),
    ]
    total_earned, total_possible = 0, 0
    print("Chapter 5 Exercises -- Score Report")
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
