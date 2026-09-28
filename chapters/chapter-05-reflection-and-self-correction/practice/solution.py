"""
Chapter 5 Practice Bank: Reflection and Self-Correction
Eight short, independent scenarios -- each a different fictional system,
each testing whether you can correctly identify ONE reflection concept
or failure type from a short description -- REFERENCE SOLUTION.

How to run:
    python3 solution.py
Scores 8/8.
"""


def score():
    correct = {
        1: "reflection step (self-critique)",
        2: "grounded verification criteria",
        3: "retry is not reflection",
        4: "revise-the-answer correction",
        5: "reflection should not run here",
        6: "reflection cannot undo an already-executed action",
        7: "iteration bound (max reflections)",
        8: "reflection needs grounded criteria, not just a second look",
    }
    given = {
        1: "reflection step (self-critique)",
        2: "grounded verification criteria",
        3: "retry is not reflection",
        4: "revise-the-answer correction",
        5: "reflection should not run here",
        6: "reflection cannot undo an already-executed action",
        7: "iteration bound (max reflections)",
        8: "reflection needs grounded criteria, not just a second look",
    }
    earned = sum(1 for n, expected in correct.items() if given[n] == expected)
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 5 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
