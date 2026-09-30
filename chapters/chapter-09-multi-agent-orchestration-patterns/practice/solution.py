"""
Chapter 9 Practice Bank: Multi-Agent Orchestration Patterns
Eight short, independent scenarios -- REFERENCE SOLUTION.

How to run:
    python3 solution.py
Scores 8/8.
"""

ANSWER_1 = "supervisor/worker pattern"
ANSWER_2 = "sequential pipeline"
ANSWER_3 = "parallel fan-out/fan-in"
ANSWER_4 = "blackboard/shared-state coordination"
ANSWER_5 = "failure isolation"
ANSWER_6 = "fail-closed routing"
ANSWER_7 = "idempotent dispatch"
ANSWER_8 = "content verification"


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
