"""
Chapter 10 Practice Bank: Multi-Agent Coordination and Communication
Eight short, independent scenarios -- each a different fictional
peer-to-peer agent system, each testing whether you can correctly name
ONE communication pattern or failure mode from a short description --
REFERENCE SOLUTION.

How to run:
    python3 solution.py
Scores 8/8.
"""

# Scenario 1: "RelayDesk" has two EQUAL agents that exchange messages
# directly, with no third agent routing every interaction between
# them. What's this coordination style called (as opposed to
# supervisor/worker)?
ANSWER_1 = "peer-to-peer communication"

# Scenario 2: "InboxGuard" checks every incoming message's required
# fields are present (after normalizing safe whitespace) before acting
# on it, refusing to guess at a renamed field. What's this called?
ANSWER_2 = "message validation"

# Scenario 3: "ShiftPlanner" has two agents independently decide, with
# no shared check, to cover the exact same shift -- neither one did
# anything wrong individually. What's this failure mode called?
ANSWER_3 = "duplicated work"

# Scenario 4: "LotTracker" fixes the problem above with one function,
# guarded by a single lock, that checks whether a lot is already
# claimed and adds the new claim in the SAME atomic operation. What's
# this fix called?
ANSWER_4 = "shared claim-check / lock"

# Scenario 5: "WaitLoop" has two agents each configured to wait for the
# other to send the first message -- neither one ever does, so neither
# makes progress. What's this failure mode called?
ANSWER_5 = "deadlock"

# Scenario 6: "ClockGuard" tracks elapsed waiting time between two
# agents and flags a specific status once that elapsed time crosses a
# fixed bound. What's this detection mechanism called?
ANSWER_6 = "deadlock timeout"

# Scenario 7: "RosterRule" has two deadlocked agents each independently
# sort a fixed, shared roster and let the alphabetically-first name
# send the first message -- no negotiation needed. What's this called?
ANSWER_7 = "consensus / tie-breaking"

# Scenario 8: "ExchangeLog" walks a recorded (sender, type,
# interpreted_ok) sequence and reports the FIRST sender whose message
# was misread, so a bad exchange can be debugged without guessing which
# side caused it. What's this called?
ANSWER_8 = "cross-agent message attribution"


def score():
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    keyword_scenarios = {
        1: ["peer-to-peer", "peer to peer", "peer"],
        2: ["message validation", "validate", "validation"],
        3: ["duplicated work", "duplicate work", "duplication"],
        4: ["shared claim", "lock", "claim-check", "claim check"],
        5: ["deadlock"],
        6: ["timeout", "deadlock timeout"],
        7: ["consensus", "tie-break", "tie breaking", "voting"],
        8: ["attribution", "which agent", "cross-agent"],
    }
    for n in given:
        answer = (given[n] or "").strip().lower()
        if any(k in answer for k in keyword_scenarios[n]):
            earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 10 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
