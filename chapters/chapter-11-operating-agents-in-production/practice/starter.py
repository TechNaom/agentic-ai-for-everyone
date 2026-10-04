"""
Chapter 11 Practice Bank: Operating Agents in Production
Eight short, independent scenarios -- each a different fictional
production-operating system, each testing whether you can correctly
name ONE operating mechanism or failure mode from a short description.
Faster and more varied than the Exercises, on purpose: the goal is
pattern recognition across many systems, not depth on one.

How to run:
    python3 starter.py
Fill in each ANSWER_N, re-run, and watch your score climb toward 8/8.
"""


# Scenario 1: "RetryDock" keys a confirmation call on (agent, order_id,
# action) rather than its raw arguments, so a retried call with
# slightly different argument shape still lands on the SAME key. What's
# this mechanism called?
ANSWER_1 = None  # TODO: name the mechanism


# Scenario 2: "BackoffQueue" waits longer after each failed attempt
# than the last, up to a fixed maximum number of attempts, logging
# every try. What's this retry pattern called?
ANSWER_2 = None  # TODO: name the pattern


# Scenario 3: "WireWatch" wraps a single network call so it cannot hang
# past a configured budget, independent of how long the overall agent
# loop or exchange is allowed to run. What timeout layer is this?
ANSWER_3 = None  # TODO: name the layer


# Scenario 4: "LoopGuard" bounds how long ONE agent's entire internal
# loop (its own retries, its own reflection passes) may run, even if
# every individual call inside it was within its own budget. What
# timeout layer is this?
ANSWER_4 = None  # TODO: name the layer


# Scenario 5: "StalledExchange" bounds how long a whole multi-message
# exchange between two or more agents may run before being flagged,
# even if every call and every agent were individually healthy. What
# timeout layer is this (same mechanism as Chapter 10's deadlock
# detection)?
ANSWER_5 = None  # TODO: name the layer


# Scenario 6: "EventTrail" writes one JSON object per line for every
# dispatch, retry, timeout, and commit, all tagged with the same id for
# one run. What's this practice called?
ANSWER_6 = None  # TODO: name the practice


# Scenario 7: "MorningReport" computes a run's success rate, retries
# used, and timeouts hit by RE-PARSING the written log the next
# morning, not from counters that only ever lived in the crashed
# process's memory. What property does this give the summary?
ANSWER_7 = None  # TODO: name the property


# Scenario 8: "AttributeAfter" reconstructs a (agent, tool, ok) trace
# purely from structured log lines, days after the run finished, and
# feeds it into an unchanged Chapter 9 function. What's this called?
ANSWER_8 = None  # TODO: name the technique


def score():
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    keyword_scenarios = {
        1: ["idempotency", "idempotent"],
        2: ["retry", "retries", "backoff"],
        3: ["per-call", "per call", "call timeout"],
        4: ["per-agent", "per agent", "agent timeout"],
        5: ["per-exchange", "per exchange", "exchange timeout", "deadlock"],
        6: ["structured logging", "structured log", "logging"],
        7: ["crash-survivable", "crash survivable", "durable", "survives a crash"],
        8: ["attribution", "from logs", "log alone"],
    }
    for n in given:
        answer = (given[n] or "").strip().lower()
        if any(k in answer for k in keyword_scenarios[n]):
            earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 11 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
