"""
Chapter 7 Practice Bank: Evaluating Agent Reliability
Eight short, independent scenarios -- each a different fictional agent,
each testing whether you can correctly identify ONE eval concept or
failure type from a short description. Faster and more varied than the
Exercises, on purpose: the goal is pattern recognition across many systems,
not depth on one.

How to run:
    python3 starter.py
Fill in each ANSWER_N, re-run, and watch your score climb toward 8/8.
"""


# Scenario 1: "RouteBot" delivers packages. Across 20 identical repeated
# runs of the same delivery task, a team computes the probability that at
# least one of any 3 randomly chosen runs would have succeeded. What's this
# number called?
ANSWER_1 = None  # TODO: name the concept


# Scenario 2: "InvoiceBot" produces a correct final invoice, but it got
# there by calling apply_discount BEFORE verify_customer_tier, the reverse
# of the documented correct order -- even though the final number happened
# to come out right anyway. What's the metric that catches this, even
# though the outcome itself was correct?
ANSWER_2 = None  # TODO: name the concept


# Scenario 3: "TriageBot" handles support tickets. A team divides total
# spend across a batch of 50 runs by the 40 runs that actually resolved a
# ticket, not by all 50 attempts. What's this number called?
ANSWER_3 = None  # TODO: name the concept


# Scenario 4: "ResearchBot" runs long, multi-hour research sessions. Its
# trajectory correctness measurably drops in turns 20-30 compared to turns
# 1-10 of the same session. What's this phenomenon called?
ANSWER_4 = None  # TODO: name the concept


# Scenario 5: "QuoteBot"'s task-success check only verifies that a
# "quote_generated" tool call appears in the trace, regardless of order
# or what else happened. A run passes this check, but the quote's dollar
# figure is calculated from the wrong product's price. What KIND of
# failure is this (not the name of a specific metric)?
ANSWER_5 = None  # TODO: describe the kind of failure


# Scenario 6: "AuditBot" was evaluated with exactly one test run, which
# passed, and the team concluded "AuditBot is reliable." What's the
# specific problem with that conclusion?
ANSWER_6 = None  # TODO: describe the problem


# Scenario 7: "SchedulerBot"'s team reports "pass@5: 97% reliable" in a
# slide deck, with no pass@1 number shown anywhere. What's the risk of
# reporting only the higher-k number?
ANSWER_7 = None  # TODO: describe the risk


# Scenario 8: "SortBot" was evaluated using a seeded random simulation
# instead of live model calls, because running thousands of live calls
# would have blown the team's time budget. What must be true of that
# simulation's error-rate parameters for this to be a legitimate
# engineering trade-off rather than a fabricated result?
ANSWER_8 = None  # TODO: describe what must be true


def score():
    correct = {
        1: "pass@k",
        2: "trajectory correctness",
        3: "cost-per-success",
        4: "multi-turn drift",
        5: "content-correctness failure",
        6: "single run does not establish a reliability rate",
        7: "masks a low single-shot pass@1 behind a generous retry budget",
        8: "calibrated against real/live measured behavior, disclosed honestly",
    }
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    keyword_scenarios = {
        1: ["pass@k", "pass at k", "pass-at-k"],
        2: ["trajectory correctness", "trajectory"],
        3: ["cost-per-success", "cost per success"],
        4: ["multi-turn drift", "multi turn drift", "drift"],
        5: ["content", "content-correctness", "content correctness", "factual", "correctness of the content", "semantic"],
        6: ["single run", "one run", "single test", "no repeated", "not enough runs", "sample size", "doesn't establish", "does not establish"],
        7: ["mask", "hide", "retry", "single-shot", "single shot", "pass@1", "pass at 1"],
        8: ["calibrat", "real", "live", "disclos"],
    }
    for n, expected in correct.items():
        answer = (given[n] or "").strip().lower()
        if any(k in answer for k in keyword_scenarios[n]):
            earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 7 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
