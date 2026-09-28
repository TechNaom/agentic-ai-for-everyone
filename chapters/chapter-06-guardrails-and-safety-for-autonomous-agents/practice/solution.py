"""
Chapter 6 Practice Bank: Guardrails and Safety for Autonomous Agents
Eight short, independent scenarios -- each a different fictional system,
each testing whether you can correctly identify ONE guardrail concept or
failure type from a short description -- REFERENCE SOLUTION.

How to run:
    python3 solution.py
Scores 8/8.
"""


def score():
    correct = {
        1: "tool allowlist",
        2: "human-approval checkpoint",
        3: "sandboxed tool execution",
        4: "action budget",
        5: "rate limiting",
        6: "fail-safe default deny",
        7: "guardrail must be enforced in code, not a system prompt",
        8: "guardrail cannot undo an action already dispatched",
    }
    given = {
        1: "tool allowlist",
        2: "human-approval checkpoint",
        3: "sandboxed tool execution",
        4: "action budget",
        5: "rate limiting",
        6: "fail-safe default deny",
        7: "guardrail must be enforced in code, not a system prompt",
        8: "guardrail cannot undo an action already dispatched",
    }
    earned = sum(1 for n, expected in correct.items() if given[n] == expected)
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 6 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
