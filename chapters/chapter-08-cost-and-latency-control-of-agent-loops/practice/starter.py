"""
Chapter 8 Practice Bank: Cost and Latency Control of Agent Loops
Eight short, independent scenarios -- each a different fictional agent,
each testing whether you can correctly identify ONE cost/latency-
control technique or risk from a short description. Faster and more
varied than the Exercises, on purpose: the goal is pattern recognition
across many systems, not depth on one.

How to run:
    python3 starter.py
Fill in each ANSWER_N, re-run, and watch your score climb toward 8/8.
"""


# Scenario 1: "PingBot" monitors server health. It's configured with a
# hard dollar cost cap; once its running cost crosses that cap, EVERY
# subsequent step is denied outright, not just logged as a warning.
# What's this mechanism called?
ANSWER_1 = None  # TODO: name the technique


# Scenario 2: "SumBot" computes running totals across a multi-step
# loop. After every step, it checks whether the output already
# satisfies the task's success condition -- if so, it stops
# immediately, even though more steps remain available in its planned
# trajectory. What's this called?
ANSWER_2 = None  # TODO: name the technique


# Scenario 3: "LookupBot" sends simple, unambiguous field lookups to a
# small, cheap model, and reserves a larger, more careful model only
# for genuinely ambiguous cases. What's this called?
ANSWER_3 = None  # TODO: name the technique


# Scenario 4: "ArchiveBot" stores a prior tool result keyed by its
# exact arguments, and returns the stored result instantly on a
# repeat request instead of recomputing or re-calling. What's this
# called?
ANSWER_4 = None  # TODO: name the technique


# Scenario 5: "FetchBot" fires two genuinely independent API lookups
# CONCURRENTLY instead of one after another, cutting real wall-clock
# time for the combined request. What's this called?
ANSWER_5 = None  # TODO: name the technique


# Scenario 6: "MonitorBot"'s team finds that 1 in 20 requests takes
# more than 3x as long as a typical request -- a fact the average
# latency alone never revealed. What statistic exposes this directly?
ANSWER_6 = None  # TODO: name the statistic


# Scenario 7: "RetryBot" waits progressively longer before each
# successive retry attempt (e.g. 1s, then 2s, then 4s) instead of
# retrying immediately every single time. What's this called?
ANSWER_7 = None  # TODO: name the technique


# Scenario 8: "SavingsBot"'s team reports "we cut cost by 70%" after a
# redesign, but never rechecked whether the redesign's success rate
# also changed. What's the specific risk of trusting that reported
# number as-is?
ANSWER_8 = None  # TODO: describe the risk


def score():
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    keyword_scenarios = {
        1: ["fail-closed", "fail closed", "budget", "hard cap"],
        2: ["early termination", "early exit", "stop early", "stops early"],
        3: ["model routing", "model tiering", "routing", "tiering"],
        4: ["caching", "cache"],
        5: ["parallel", "concurrent", "concurrency"],
        6: ["p95", "percentile", "tail"],
        7: ["exponential backoff", "backoff"],
        8: ["cost-per-success", "cost per success", "success rate", "false win", "regression"],
    }
    for n in given:
        answer = (given[n] or "").strip().lower()
        if any(k in answer for k in keyword_scenarios[n]):
            earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 8 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
