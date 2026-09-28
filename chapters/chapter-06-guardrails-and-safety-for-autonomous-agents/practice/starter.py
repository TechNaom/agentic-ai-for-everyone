"""
Chapter 6 Practice Bank: Guardrails and Safety for Autonomous Agents
Eight short, independent scenarios -- each a different fictional system,
each testing whether you can correctly identify ONE guardrail concept or
failure type from a short description. Faster and more varied than the
Exercises, on purpose: the goal is pattern recognition across many systems,
not depth on one.

How to run:
    python3 starter.py
Fill in each ANSWER_N, re-run, and watch your score climb toward 8/8.
"""


# Scenario 1: "GateBot" at a parking garage can raise the gate arm, but a
# check runs first confirming the requested action name is one of the small,
# fixed set GateBot was actually given -- an attempt to call a made-up
# "disable_all_cameras" action is refused before anything runs. What's this
# check called?
ANSWER_1 = None  # TODO: name the concept


# Scenario 2: "PayBot" at a payroll service can issue an off-cycle payment,
# but any payment over $1,000 genuinely pauses and waits for a manager to
# confirm before PayBot's dispatch function proceeds -- execution does not
# continue until that confirmation arrives. What's this called?
ANSWER_2 = None  # TODO: name the concept


# Scenario 3: "OpsBot" at a data center can run a maintenance command, but
# only commands matching a fixed allowlist of shapes are permitted, and
# anything containing a shell metacharacter or a network call is refused
# before execution. What's this called?
ANSWER_3 = None  # TODO: name the concept


# Scenario 4: "TicketBot" at a support desk is capped at 10 total dispatched
# actions per session, regardless of how many reasoning steps it takes to
# get there -- once the cap is hit, no further action of ANY kind dispatches.
# What's this called?
ANSWER_4 = None  # TODO: name the concept


# Scenario 5: "BulkMailBot" can send a customer email, but is capped at 3
# sent emails per session specifically -- even though its overall action cap
# is much higher and it could still, say, look up ten more customer records
# after hitting that email cap. What's this specific, narrower bound called?
ANSWER_5 = None  # TODO: name the concept


# Scenario 6: "ApprovalBot"'s approval-checking service occasionally times
# out and raises an exception. The FIRST version of ApprovalBot's dispatcher
# treated any exception from the approval check as "approved" (since the
# code technically didn't say no) -- an unapproved high-risk transfer
# executed the one time the approval service happened to be down. What
# principle did this violate?
ANSWER_6 = None  # TODO: describe the principle


# Scenario 7: "MemoBot" was told, in its system prompt, "never delete a
# customer record without explicit confirmation." A crafted note embedded in
# a customer's own support ticket (read back to MemoBot as a tool result)
# claimed confirmation had "already been given by phone," and MemoBot
# deleted the record -- no code anywhere had actually verified that claim.
# What's the underlying architectural mistake here?
ANSWER_7 = None  # TODO: describe the mistake


# Scenario 8: "ShipBot" dispatched a real shipment to the wrong address. A
# later reflection step correctly caught the mistake and revised the
# CONFIRMATION MESSAGE shown to the customer -- but the package was already
# in transit to the wrong address, and nothing about revising the message
# changed that. What does this illustrate about what a guardrail is for that
# reflection alone cannot provide?
ANSWER_8 = None  # TODO: describe the limit


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
        1: ANSWER_1, 2: ANSWER_2, 3: ANSWER_3, 4: ANSWER_4,
        5: ANSWER_5, 6: ANSWER_6, 7: ANSWER_7, 8: ANSWER_8,
    }
    earned = 0
    keyword_scenarios = {
        1: ["allowlist", "allow list", "allow-list"],
        2: ["human-approval", "human approval", "approval checkpoint", "pause-and-wait", "pause and wait"],
        3: ["sandbox", "sandboxed"],
        4: ["action budget", "budget"],
        5: ["rate limit", "rate limiting"],
        6: ["fail-safe", "fail safe", "fail closed", "default deny"],
        7: ["not enforced", "system prompt", "code, not", "enforced in code"],
        8: ["cannot undo", "can't undo", "already dispatched", "already happened", "already executed", "already fired", "already in transit"],
    }
    for n, expected in correct.items():
        answer = (given[n] or "").strip().lower()
        if any(k in answer for k in keyword_scenarios[n]):
            earned += 1
    return earned, 8


if __name__ == "__main__":
    earned, total = score()
    print("Chapter 6 Practice Bank -- Score Report")
    print("=" * 40)
    print(f"TOTAL: {earned}/{total}")
