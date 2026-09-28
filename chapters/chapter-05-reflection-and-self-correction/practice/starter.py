"""
Chapter 5 Practice Bank: Reflection and Self-Correction
Eight short, independent scenarios -- each a different fictional system,
each testing whether you can correctly identify ONE reflection concept
or failure type from a short description. Faster and more varied than
the Exercises, on purpose: the goal is pattern recognition across many
systems, not depth on one.

How to run:
    python3 starter.py
Fill in each ANSWER_N, re-run, and watch your score climb toward 8/8.
"""


# Scenario 1: "PricingBot" at a car wash quotes a price, then a second,
# separate function call checks that quote against the wash's actual price
# table before the quote is sent to the customer. What's this second call
# called?
ANSWER_1 = None  # TODO: name the concept


# Scenario 2: "AdviceBot" at a fitness app recommends a workout plan, then
# checks that recommendation against the user's actual logged injuries
# (not the model's own opinion of whether it sounds safe) before returning
# it. What's the name for checking against actual logged facts, rather than
# the model's own re-read of its own answer?
ANSWER_2 = None  # TODO: name the concept


# Scenario 3: "SupportBot" got a wrong answer, so its "fix" was to re-ask
# the model the exact same question a second time and hope a different,
# better answer came back by chance -- no independent check was ever run
# against anything. What's wrong with calling this "reflection"?
ANSWER_3 = None  # TODO: name the concept


# Scenario 4: "QuoteBot" drafted an estimate that was wrong, and a
# reflection step replaced the wrong number with the correct one before
# sending the final response. What's this specific action called?
ANSWER_4 = None  # TODO: name the concept


# Scenario 5: "FormBot" runs a full reflection pass (a second model call)
# on every single request, including "what are your hours" -- a request
# with an obviously fixed, unambiguous answer -- doubling latency and cost
# for zero benefit. What's the lesson here?
ANSWER_5 = None  # TODO: describe the lesson


# Scenario 6: "AuditBot" drafted an email, reflection caught that it
# violated policy, and revised the TEXT before it was shown to a reviewer
# -- but an earlier version of AuditBot had already auto-sent a near-
# identical email moments before reflection was added to the pipeline.
# Reflection could not undo that already-sent email. What does this
# illustrate about reflection's limits?
ANSWER_6 = None  # TODO: describe the limit


# Scenario 7: "LoopBot" reflects, revises, reflects again, revises again,
# and keeps going indefinitely because its draft never quite satisfies its
# own reflection check. What's the fix?
ANSWER_7 = None  # TODO: name the concept


# Scenario 8: "CalcBot" asked a second model call to "double check" its own
# math, but never gave that second call the actual correct formula or
# values to check against -- just "does this look right to you?" The
# second call confidently said yes, and the original error shipped anyway.
# What does this scenario illustrate?
ANSWER_8 = None  # TODO: describe the lesson


def score():
    correct = {
        1: "reflection step (self-critique)",
        2: "grounded verification criteria",
        3: "retry is not reflection",
        4: "revise-the-answer correction",
        5: "reflection should not run here",
        6: "reflection cannot undo an already-executed action",
        7: "iteration bound (max reflections)",
        8: "reflection needs grounded criteria, not just a second look",
    }
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    keyword_scenarios = {
        1: ["reflection step", "self-critique", "self critique"],
        2: ["grounded", "verification criteria", "actual", "ground truth"],
        3: ["retry is not reflection", "not reflection", "just a retry"],
        4: ["revise-the-answer", "revise the answer", "revision", "correction"],
        5: ["should not run", "not worth", "waste", "skip reflection", "unnecessary"],
        6: ["cannot undo", "can't undo", "already-executed", "already executed", "already sent", "already happened"],
        7: ["iteration bound", "max reflections", "bound", "limit the loop", "stop after"],
        8: ["grounded criteria", "not just a second look", "no ground truth", "nothing to check against"],
    }
    for n, expected in correct.items():
        answer = (given[n] or "").strip().lower()
        if any(k in answer for k in keyword_scenarios[n]):
            earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 5 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
