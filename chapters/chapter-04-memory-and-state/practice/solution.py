"""
Chapter 4 Practice Bank: Memory and State -- REFERENCE SOLUTION
Eight short, independent scenarios -- each a different fictional system,
each testing whether you can correctly identify ONE memory concept or
failure type from a short description. This is the fully filled-in
reference; running it directly scores 8/8.
"""


# Scenario 1: "ConciergeBot" at a hotel front desk keeps a list of every
# message exchanged during one guest's check-in call, so it can refer back
# to something the guest said two turns earlier in the SAME call -- but
# that list is thrown away the moment the call ends. What's this called?
ANSWER_1 = "short-term working memory"


# Scenario 2: "AdvisorBot" at a financial planning firm writes a client's
# stated risk tolerance to a database, so six months later, in a completely
# separate session, it can pull that same fact back up without the client
# repeating it. What's this called?
ANSWER_2 = "long-term persisted memory"


# Scenario 3: "TutorBot" ran a 90-minute one-on-one session, and by the end,
# the growing message list was replaced with a short rolling summary of
# everything before the last few turns, to stay under the model's practical
# context limit. What's this called?
ANSWER_3 = "token-budget pruning"


# Scenario 4: "OnboardBot" at a new-hire portal has to decide whether "I go
# by Alex, not my legal first name" is worth writing to a persisted profile,
# versus "got it, thanks" which isn't. What's this decision called?
ANSWER_4 = "promote-worthy fact detection"


# Scenario 5: "ProfileBot" for a meal-kit service had a save function that
# built a brand-new preferences dict from scratch on every call instead of
# loading the customer's existing preferences first -- so recording a new
# delivery-day preference silently erased a previously recorded allergy
# note. What's this called?
ANSWER_5 = "read-modify-write merge bug"


# Scenario 6: "CoachBot" (a different one) loaded a member's persisted
# facts once at the very start of a session, stored them in a local
# variable, and then used that SAME stale variable to decide its reply --
# even after the member stated a brand-new injury two messages later in
# that same session. What's the bug here?
ANSWER_6 = "stale snapshot"


# Scenario 7: "NotesBot" for a therapy practice persisted literally every
# single message a client sent, including "can you turn the AC down" and
# "one sec, my dog is barking" -- filling the long-term store with routine
# noise no future session would ever need. What should NotesBot have done
# differently?
ANSWER_7 = "only persist promote-worthy facts"


# Scenario 8: "SummaryBot" relied ENTIRELY on its rolling conversation
# summary to preserve a client's stated peanut allergy, rather than writing
# that fact to the persisted store directly -- and the next summarization
# pass dropped it, since the summarizer had no way to know that detail was
# more important than the small talk around it. What does this scenario
# illustrate?
ANSWER_8 = "summarization is not a substitute for persisting durable facts"


def score():
    correct = {
        1: "short-term working memory",
        2: "long-term persisted memory",
        3: "token-budget pruning",
        4: "promote-worthy fact detection",
        5: "read-modify-write merge bug",
        6: "stale snapshot",
        7: "only persist promote-worthy facts",
        8: "summarization is not a substitute for persisting durable facts",
    }
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    keyword_scenarios = {
        6: ["stale", "snapshot", "not re-check", "didn't re-check", "outdated"],
        7: ["only persist", "promote-worthy", "not persist everything", "filter"],
        8: ["not a substitute", "summariz", "can drop", "shouldn't rely"],
    }
    for n, expected in correct.items():
        answer = (given[n] or "").strip().lower()
        if n in keyword_scenarios:
            if any(k in answer for k in keyword_scenarios[n]):
                earned += 1
        else:
            if answer == expected:
                earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 4 Practice Bank -- Score Report (SOLUTION)")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
