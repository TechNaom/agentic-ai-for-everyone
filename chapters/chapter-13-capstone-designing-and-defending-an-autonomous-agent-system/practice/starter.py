"""
Chapter 13 Practice Bank: Capstone -- Designing and Defending an
Autonomous Agent System
Eight short, independent scenarios -- each a different fictional
MULTI-COMPONENT system being architected at capstone scale, each
testing whether you can correctly name ONE decision-framework
concept from a short description.

Abstract system names (not full organizations), matching Chapter
12's own practice-bank convention for quick diagnostic scenarios.

How to run:
    python3 starter.py
Fill in each ANSWER_N below with your own short answer, then re-run.
Scores 8/8 when every answer contains the right keyword/phrase.
"""

# Scenario 1: "RouteDesk" has three components (intake, routing,
# billing) that each read/write the SAME shipment record, with no
# concurrent independent actor. All three claim to need their own
# agent. What's the correct multi-agent verdict?
ANSWER_1 = None  # TODO

# Scenario 2: "ClaimGate" has a claims-intake component and a
# fraud-review component that are genuinely different skills and can
# each proceed on their own queue -- but neither one touches a shared
# resource the other also writes to. What justifies multi-agent here?
ANSWER_2 = None  # TODO

# Scenario 3: "StockMesh" has a storefront-checkout component and a
# warehouse-replenishment component that both claim units from the
# SAME shared stock ledger at the same time. What SECOND justification
# for multi-agent applies here, beyond Scenario 2's?
ANSWER_3 = None  # TODO

# Scenario 4: "ReviewSpan" assembled a design with every one of
# Chapters 4-11's mechanisms turned on, for a system where only three
# of the eight are actually backed by a stated fact. What does the
# architecture-smell check call the other five?
ANSWER_4 = None  # TODO

# Scenario 5: "NightLedger" has an irreversible overnight commit step
# with no idempotency key, so a retried call can double-commit it.
# What single load-bearing mechanism is missing?
ANSWER_5 = None  # TODO

# Scenario 6: "FactField" claims a memory mechanism, but it's just an
# in-process dictionary that resets every time the script restarts --
# it never actually survives a separate, later session. What's wrong?
ANSWER_6 = None  # TODO

# Scenario 7: "GateCheck" has a refund guardrail that defaults to
# auto-approving unless a reviewer explicitly says no. What is this
# the opposite of?
ANSWER_7 = None  # TODO

# Scenario 8: "SpanCapstone" composed Chapters 1-11's full mechanism
# inventory for one new multi-component problem, then wrote up the
# characterization, the selection, the budget, the rejected
# alternatives, and the smell-check result as one reviewable document.
# What artifact is this?
ANSWER_8 = None  # TODO


def score():
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    keyword_scenarios = {
        1: ["single-agent", "single agent", "one agent"],
        2: ["independently", "specialized subtasks"],
        3: ["concurrent", "shared state", "shared resource"],
        4: ["over-engineer", "over engineer", "unjustified"],
        5: ["operating layer", "operating"],
        6: ["memory", "persist"],
        7: ["fail-closed", "fail closed", "fail-safe"],
        8: ["decision record", "adr"],
    }
    for n in given:
        answer = (given[n] or "").strip().lower()
        if any(k in answer for k in keyword_scenarios[n]):
            earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 13 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
