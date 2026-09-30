"""
Chapter 9 Practice Bank: Multi-Agent Orchestration Patterns
Eight short, independent scenarios -- each a different fictional
multi-agent system, each testing whether you can correctly name ONE
coordination pattern or failure mode from a short description. Faster
and more varied than the Exercises, on purpose: the goal is pattern
recognition across many systems, not depth on one.

How to run:
    python3 starter.py
Fill in each ANSWER_N, re-run, and watch your score climb toward 8/8.
"""


# Scenario 1: "HelpDesk Central" has one orchestrator agent that
# decomposes an incoming ticket into sub-tasks and dispatches each one
# to a specialist agent (billing, technical, or account-access), then
# combines their replies into one response. What's this coordination
# pattern called?
ANSWER_1 = None  # TODO: name the pattern


# Scenario 2: "DraftLine" runs three fixed stages in strict order on
# the same document: draft, fact-check, then format -- each stage
# always runs after the one before it, on that stage's own output,
# with no agent choosing which stage handles what. What's this
# coordination pattern called?
ANSWER_2 = None  # TODO: name the pattern


# Scenario 3: "QuoteDesk" fires three genuinely independent pricing
# lookups CONCURRENTLY instead of one after another, then waits for
# all three to finish before combining them into one quote. What's
# this pattern called?
ANSWER_3 = None  # TODO: name the pattern


# Scenario 4: "ProjectBoard" lets several agents read and write a
# single shared dict of task statuses, coordinating with each other
# through that shared state rather than through one agent explicitly
# routing every interaction. What's this coordination style called?
ANSWER_4 = None  # TODO: name the pattern


# Scenario 5: "FleetOps" wraps each of its three dispatched worker
# agents in its own try/except boundary, so one worker's exception
# never causes the other two workers' already-completed results to be
# lost. What's this called?
ANSWER_5 = None  # TODO: name the technique


# Scenario 6: "TicketRouter"'s keyword matcher returns None instead of
# guessing whenever an incoming ticket doesn't clearly match any of
# its three specialist agents' domains. What's this routing discipline
# called?
ANSWER_6 = None  # TODO: name the discipline


# Scenario 7: "OrderDesk" tracks which (order_id, worker) pairs have
# already been dispatched, so that a retry after a malformed response
# never re-dispatches the same order to the same worker twice. What's
# this called?
ANSWER_7 = None  # TODO: name the technique


# Scenario 8: "StatusBot"'s hotel-booking worker returns a
# well-formed, confident-looking result -- but the city field doesn't
# match the city that was actually requested. The only way to catch
# this is to check the result against what was requested, not just
# that a result came back at all. What's this called?
ANSWER_8 = None  # TODO: name the technique


def score():
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    keyword_scenarios = {
        1: ["supervisor", "worker"],
        2: ["sequential", "pipeline"],
        3: ["parallel", "fan-out", "fan out", "fan-in", "concurrent"],
        4: ["blackboard", "shared state", "shared-state"],
        5: ["failure isolation", "isolate", "isolation"],
        6: ["fail-closed", "fail closed", "routing"],
        7: ["idempotent", "idempotency", "duplicate"],
        8: ["content verification", "verify", "verification"],
    }
    for n in given:
        answer = (given[n] or "").strip().lower()
        if any(k in answer for k in keyword_scenarios[n]):
            earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 9 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
