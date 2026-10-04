"""
Chapter 12 Practice Bank: Designing Agent Architectures
Eight short, independent scenarios -- each a different fictional
system being architected, each testing whether you can correctly name
ONE decision-framework concept from a short description --
REFERENCE SOLUTION.

How to run:
    python3 solution.py
Scores 8/8.
"""

# Scenario 1: "SingleDesk" handles three very differently-worded
# request types, but all three read and write the same customer
# record, with no concurrent independent actor required. What's the
# correct multi-agent verdict here?
ANSWER_1 = "single-agent is sufficient"

# Scenario 2: "TwinField" has two agents that must both act, at the
# same time, on the same shared plot of farmland inventory. What fact
# justifies multi-agent here?
ANSWER_2 = "concurrent independent actors on shared state"

# Scenario 3: "VaultGate" has one irreversible, high-value action (a
# large withdrawal) and currently has NO human-approval checkpoint
# before it fires. What does the architecture-smell check call this?
ANSWER_3 = "under-engineering / missing guardrail"

# Scenario 4: "ChatterMesh" was given a 3-agent supervisor/worker
# design for a single customer-support conversation with no distinct,
# independently-runnable subtasks at all. What does the
# architecture-smell check call this?
ANSWER_4 = "over-engineering / unjustified multi-agent"

# Scenario 5: "NightWatch" runs an unattended monitoring loop 24/7
# with no idempotency keys, no timeouts, and no structured logging.
# What single load-bearing mechanism is missing?
ANSWER_5 = "operating layer"

# Scenario 6: "DraftCritic" was given a grounded reflection step for
# an output that is always a single checkable number, never free text.
# What's this called, echoing Chapter 5's own lesson?
ANSWER_6 = "retry is not reflection / unneeded reflection"

# Scenario 7: "StakesLadder" assigns a HIGHER minimum task-success rate
# and a LOWER cost ceiling to its irreversible-action path than to its
# routine path. What is this an example of?
ANSWER_7 = "a reliability/cost budget scaled to stakes"

# Scenario 8: "ReviewPacket" lists the chosen design, two alternatives
# that were considered, and the specific reason each alternative was
# rejected. What artifact is this?
ANSWER_8 = "an architecture decision record (ADR)"


def score():
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    keyword_scenarios = {
        1: ["single-agent", "single agent", "one agent"],
        2: ["concurrent", "shared state", "shared resource"],
        3: ["guardrail", "under-engineer", "under engineer"],
        4: ["over-engineer", "over engineer", "unjustified multi-agent", "unjustified multi agent"],
        5: ["operating layer", "operating"],
        6: ["reflection", "retry is not reflection"],
        7: ["budget", "stakes"],
        8: ["decision record", "adr"],
    }
    for n in given:
        answer = (given[n] or "").strip().lower()
        if any(k in answer for k in keyword_scenarios[n]):
            earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 12 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
