"""
Chapter 7 Practice Bank: Evaluating Agent Reliability
Eight short, independent scenarios -- REFERENCE SOLUTION.

How to run:
    python3 solution.py
Scores 8/8.
"""

ANSWER_1 = "pass@k"
ANSWER_2 = "trajectory correctness"
ANSWER_3 = "cost-per-success"
ANSWER_4 = "multi-turn drift"
ANSWER_5 = "a content-correctness failure, not a process failure"
ANSWER_6 = "a single run does not establish a reliability rate -- it needs repeated runs"
ANSWER_7 = "reporting only pass@5 can mask a low single-shot pass@1 behind a generous retry budget"
ANSWER_8 = "its error-rate parameters must be calibrated against real, live measured behavior, and disclosed honestly as a simulation"


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
