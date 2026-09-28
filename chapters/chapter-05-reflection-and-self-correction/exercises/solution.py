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
haven't seen before -- REFERENCE SOLUTION.

How to run:
    python3 solution.py
It prints a score report. Scores 18/18.
"""

import re

RATE_PER_HOUR = 65  # dollars, flat labor rate
LICENSED_ONLY_KEYWORDS = ["gas line", "electrical panel", "gas leak", "breaker panel"]


def compute_price(hours, parts_cost):
    return RATE_PER_HOUR * hours + parts_cost


def requires_licensed_referral(job_description):
    text = job_description.lower()
    return any(k in text for k in LICENSED_ONLY_KEYWORDS)


def extract_dollar_amount(text):
    m = re.search(r"\$(\d+(?:\.\d{1,2})?)", text)
    return float(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Task 1: Map five RepairBot facts to the reflection concept each is about.
# ---------------------------------------------------------------------------
TASK_1_ANSWERS = {
    "fact_a": "first-pass draft (no reflection)",
    "fact_b": "reflection step (self-critique)",
    "fact_c": "grounded verification criteria",
    "fact_d": "revise-the-answer correction",
    "fact_e": "iteration bound (max reflections)",
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
TASK_2_ANSWER = "MORE likely"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "MORE likely" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): grounded price verifier.
# ---------------------------------------------------------------------------
def verify_price(draft_text, hours, parts_cost):
    correct_price = compute_price(hours, parts_cost)
    stated_price = extract_dollar_amount(draft_text)
    return stated_price is not None and stated_price == correct_price


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
def draft_mentions_referral(draft_text):
    text = draft_text.lower()
    return any(kw in text for kw in ["licensed", "technician", "referral", "cannot quote", "unable to quote"])


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
    correct_price = compute_price(hours, parts_cost)
    needs_referral = requires_licensed_referral(job_description)
    referral_ok = (not needs_referral) or draft_mentions_referral(draft_text)
    stated_price = extract_dollar_amount(draft_text)

    if needs_referral and referral_ok and stated_price is None:
        # Appropriately declines to quote a licensed-only job -- no price
        # is expected in that case, so don't flag a missing one.
        price_ok = True
    else:
        price_ok = verify_price(draft_text, hours, parts_cost)

    if price_ok and referral_ok:
        return draft_text, False

    revised = draft_text
    if not price_ok:
        revised = f"Corrected estimate: ${correct_price} for {hours} hour(s) of labor plus parts."
    if needs_referral and not draft_mentions_referral(revised):
        revised += " This job involves work that requires a licensed technician -- please treat this as a referral, not a DIY quote."
    return revised, True


def score_exercise_5():
    points = 0
    # Case A: wrong price, no referral needed -- should be corrected.
    revised, changed = reflect_and_revise("That'll be $100 total.", "Patch drywall", 2, 65)
    if changed and "195" in revised:
        points += 1
    # Case B: correct price, but missing referral flag on a gas job -- should be flagged.
    revised2, changed2 = reflect_and_revise("That's $195 total.", "Fix a gas line leak", 2, 65)
    if changed2 and "licensed" in revised2.lower():
        points += 1
    # Case C: already correct and already flags referral -- should pass through unchanged.
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
# Name this failure using the exact concept string.
TASK_6_ANSWER = "retry is not reflection"


def score_exercise_6():
    return (1 if TASK_6_ANSWER == "retry is not reflection" else 0), 1


# ---------------------------------------------------------------------------
# Task 7 (production-gear): a bounded reflect loop.
# ---------------------------------------------------------------------------
def bounded_reflect_loop(draft_text, job_description, hours, parts_cost, max_reflections=2):
    attempt = draft_text
    for i in range(max_reflections):
        attempt, changed = reflect_and_revise(attempt, job_description, hours, parts_cost)
        if not changed:
            return attempt, i, False  # converged before hitting the bound
    # Ran out of attempts -- check one more time; if still wrong, escalate.
    final_price_ok = verify_price(attempt, hours, parts_cost)
    final_referral_ok = (not requires_licensed_referral(job_description)) or draft_mentions_referral(attempt)
    if final_price_ok and final_referral_ok:
        return attempt, max_reflections, False
    return "This estimate needs a human to review before it's sent.", max_reflections, True


def score_exercise_7():
    points = 0
    # Converges in 1 reflection.
    result, attempts, escalated = bounded_reflect_loop("That'll be $100 total.", "Patch drywall", 2, 65)
    if not escalated and attempts <= 2 and "195" in result:
        points += 1
    # Never converges (adversarial: draft always restates the same wrong price) --
    # must escalate to a human rather than loop forever.
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
    concepts_touched = set(TASK_1_ANSWERS.values())
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
