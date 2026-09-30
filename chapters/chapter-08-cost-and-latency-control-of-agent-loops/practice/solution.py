"""
Chapter 8 Practice Bank: Cost and Latency Control of Agent Loops
Eight short, independent scenarios -- REFERENCE SOLUTION.

How to run:
    python3 solution.py
Scores 8/8.
"""

ANSWER_1 = "fail-closed budget"
ANSWER_2 = "early termination"
ANSWER_3 = "model routing"
ANSWER_4 = "caching"
ANSWER_5 = "parallel tool calls"
ANSWER_6 = "p95 latency percentile"
ANSWER_7 = "exponential backoff"
ANSWER_8 = "the cost cut could be a false win if cost-per-success actually got worse"


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
