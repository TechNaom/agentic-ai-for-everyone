"""
Chapter 2 Practice Bank: Planning and Task Decomposition -- REFERENCE SOLUTION
Eight short, independent scenarios -- each a different fictional system,
each testing whether you can correctly identify ONE planning concept or
failure type from a short description. This is the fully filled-in
reference; running it directly scores 8/8.
"""


# Scenario 1: "WelcomeBot," a SaaS onboarding tool, runs the same four
# steps for every new customer regardless of what they signed up for --
# create account, send credentials, schedule kickoff call, add to mailing
# list. Should WelcomeBot use a fixed or emergent plan?
ANSWER_1 = "fixed"


# Scenario 2: "SupportBot" at a helpdesk reads a ticket, and only after
# reading it decides whether the next check is billing history or the
# outage status page -- the choice depends entirely on the ticket's
# content. Fixed or emergent?
ANSWER_2 = "emergent"


# Scenario 3: "PayoutBot" for a marketplace ran a fixed plan: verify
# seller account, calculate payout, issue payout. All three tool calls
# succeeded, but the plan never checked a fraud-hold flag that was
# sitting in the first step's own result, so the payout went out anyway.
# What's this called?
ANSWER_3 = "wrong-plan failure"


# Scenario 4: "RouteBot" kept failing on a typo'd pickup address and
# retried with a new guessed address... forever, with no cap. What's
# missing?
ANSWER_4 = "planning guard"


# Scenario 5: "RefundBot" hit a typo'd order ID, rebuilt its whole
# 3-step plan with a corrected ID, and re-ran all three steps once,
# succeeding. What's this called?
ANSWER_5 = "re-planning"


# Scenario 6: "AuditBot" runs the exact same 6-step document-collection
# checklist for every audit, but it's implemented as one reasoning call
# per step (6 calls every audit). What should the team switch to, to cut
# cost without changing behavior?
ANSWER_6 = "fixed plan"


# Scenario 7: "DiagnoseBot" at a car dealership chooses whether to check
# the battery or the alternator only after reading the mechanic's initial
# inspection notes. Fixed or emergent?
ANSWER_7 = "emergent"


# Scenario 8: "FormBot" was asked to output its whole multi-tool plan as
# free-text JSON without the real tool schema ever being passed to the
# model, and it invented tool names that don't exist in the system. What
# should FormBot use instead to keep every planned step grounded in a
# real tool?
ANSWER_8 = "tool-calling API"


def score():
    correct = {
        1: "fixed", 2: "emergent", 3: "wrong-plan failure",
        4: "planning guard", 5: "re-planning", 6: "fixed plan",
        7: "emergent", 8: "tool-calling",
    }
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    for n, expected in correct.items():
        answer = (given[n] or "").strip().lower()
        if n in (4, 6, 8):
            keywords = {
                4: ["guard", "cap", "max_replans", "replan"],
                6: ["fixed plan", "fixed"],
                8: ["tool-calling", "function calling", "tools=", "tool calling", "function-calling"],
            }[n]
            if any(k in answer for k in keywords):
                earned += 1
        else:
            if answer == expected:
                earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 2 Practice Bank -- Score Report (SOLUTION)")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
