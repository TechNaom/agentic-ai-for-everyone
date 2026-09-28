"""
Chapter 3 Practice Bank: Tool Use and Function Calling
Eight short, independent scenarios -- each a different fictional system,
each testing whether you can correctly identify ONE tool-use concept or
failure type from a short description. Faster and more varied than the
Exercises, on purpose: the goal is pattern recognition across many
systems, not depth on one.

How to run:
    python3 starter.py
Fill in each ANSWER_N, re-run, and watch your score climb toward 8/8.
"""


# Scenario 1: "QuoteBot" for a moving company has get_distance_estimate(from,
# to) and check_crew_availability(date) -- both plausible for "how much will
# my move cost," but QuoteBot calls check_crew_availability first because
# "move" reminded it of "crew," even though distance is the cheaper, more
# decisive signal for a rough quote. What's this called?
ANSWER_1 = None  # TODO: name the failure type


# Scenario 2: "InvoiceBot" at a bookkeeping firm receives client IDs as
# "CLIENT-88", "client88", "Client #88", and "88" across different intake
# channels, and needs one function to resolve all of them to the same
# lookup key. What's this called?
ANSWER_2 = None  # TODO: name the concept


# Scenario 3: "WeatherBot" calls a third-party radar API that occasionally
# never returns at all -- no error, no data, just silence past a few
# seconds. What kind of failure is this, distinct from a malformed response?
ANSWER_3 = None  # TODO: name the failure type


# Scenario 4: "ScoreBot" at a lending platform calls a legacy credit-check
# endpoint that, for certain applicant IDs, returns the plain string "NO
# RECORD" instead of the JSON object every other response uses. What kind
# of failure is this?
ANSWER_4 = None  # TODO: name the failure type


# Scenario 5: "CancelBot" for a gym membership always returns
# {"cancelled": True} from cancel_membership(), even for members with an
# active contract lock-in that makes cancellation impossible -- members
# only found out when they were billed again next month. What's this
# called?
ANSWER_5 = None  # TODO: name the failure type


# Scenario 6: "DispatchBot" hit a timeout on one call and, correctly,
# retried with a short backoff. On a DIFFERENT call, it got back a
# malformed (non-dict) response and also retried it three times before
# giving up -- getting the exact same malformed response every time. What
# should DispatchBot have done differently for the second case?
ANSWER_6 = None  # TODO: a few words describing the correct policy


# Scenario 7: "IntakeBot" at a legal clinic has three tools that could all
# plausibly explain "why hasn't my case moved forward" -- check_court_date,
# check_document_status, check_assigned_attorney. It now checks
# check_document_status FIRST, since missing documents are the cheapest,
# most common, and most decisive cause to rule out before anything else.
# What discipline does this reflect?
ANSWER_7 = None  # TODO: a few words naming the discipline


# Scenario 8: "TicketBot" received a seat ID as "A-12", "a12", "Seat A12",
# and "12A" (note: this last one means something different -- row 12, seat
# A) across different booking channels. A blind strip-and-lowercase
# normalize step would silently conflate "A-12" and "12A" into the same
# key even though they refer to different seats. What does this scenario
# illustrate about argument normalization?
ANSWER_8 = None  # TODO: a short sentence


def score():
    correct = {
        1: "wrong-tool-choice",
        2: "argument-formatting drift",
        3: "timeout failure",
        4: "malformed-output failure",
        5: "succeeds-but-wrong-answer failure",
        6: "not retried",
        7: "cheapest decisive signal first",
        8: "normalization can be wrong",
    }
    given = {
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    keyword_scenarios = {
        6: ["not retr", "no retry", "shouldn't retry", "should not retry", "stop retrying"],
        7: ["cheapest", "decisive"],
        8: ["wrong", "conflate", "ambiguous", "not just missing"],
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
    print("Chapter 3 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
