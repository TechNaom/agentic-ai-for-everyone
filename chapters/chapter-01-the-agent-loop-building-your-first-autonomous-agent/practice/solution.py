"""
Chapter 1 Practice Bank: The Agent Loop -- REFERENCE SOLUTION
Eight short, independent scenarios -- each a different fictional
system, each testing whether you can correctly identify ONE agent-loop
concept or failure type from a short description. This is the fully
filled-in reference; running it directly scores 8/8.
"""


# Scenario 1: Marisol runs "InboxTriage," which reads one email and
# replies with a one-line summary -- no tool calls, no loop, just one
# model call. Is InboxTriage an agent per this chapter's definition?
ANSWER_1 = "no"


# Scenario 2: "DeskBot" at a hotel front desk calls check_room_status,
# gets back {"clean": True}, and this result is appended to the message
# history before DeskBot answers the guest. Which loop step does
# appending the result to the history correspond to?
ANSWER_2 = "observation"


# Scenario 3: "QuoteBot" for an auto shop calls get_part_price("brake
# pads (front)") but the parts database is keyed exactly "brake pads".
# The lookup misses. What failure type is this?
ANSWER_3 = "wrong argument"


# Scenario 4: "RouteBot" for a delivery company has no cap on how many
# times it can call get_traffic_status in one task. During an outage
# where the traffic API always errors, RouteBot calls it over 200 times
# in one session before a human notices. What's missing?
ANSWER_4 = "iteration guard"


# Scenario 5: "MenuBot" at a restaurant answers "is the salmon
# gluten-free?" by generating a plausible-sounding answer from general
# food knowledge, even though a check_allergen_info tool exists and was
# never called. What's the most likely root cause?
ANSWER_5 = "vague tool description"


# Scenario 6: "PatchBot," a code-review agent, calls run_tests(), gets
# back {"passed": 41, "failed": 2}, and its next message says "All
# tests passed, ready to merge." What's this called?
ANSWER_6 = "hallucinated result despite a real observation"


# Scenario 7: A live call to PatchBot's model hangs with no response for
# over five minutes because of a flaky network. What should the calling
# code have set on every model call to prevent this from blocking
# indefinitely?
ANSWER_7 = "timeout"


# Scenario 8: "ReceptionBot" is built entirely with a heavy multi-agent
# framework, and its team can't explain what happens internally when a
# tool call fails, because the framework hides it. Per this chapter's
# own build philosophy, what's the recommended starting point instead?
ANSWER_8 = "plain python, from scratch"


def score():
    correct = {
        1: "no",
        2: "observation",
        3: "wrong argument",
        4: "iteration guard",
        5: "vague tool description",
        6: "hallucinated result despite a real observation",
        7: "timeout",
        8: "plain python",
    }
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    for n, expected in correct.items():
        answer = (given[n] or "").strip().lower()
        if n in (4, 7, 8):
            # Free-text scenarios: substance check, not exact match.
            keywords = {
                4: ["iteration", "guard", "cap", "max"],
                7: ["timeout", "time budget", "time limit"],
                8: ["plain python", "from scratch", "no framework", "minimal"],
            }[n]
            if any(k in answer for k in keywords):
                earned += 1
        else:
            if answer == expected:
                earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 1 Practice Bank -- Score Report (SOLUTION)")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
