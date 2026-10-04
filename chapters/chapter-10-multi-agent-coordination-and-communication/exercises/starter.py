"""
Chapter 10 Exercises: Multi-Agent Coordination and Communication
Scenario: Bellcrest Freelance Guild, a fictional freelance-coordination
cooperative. Its two PEER agents, DesignScout and DevScout, must claim
tasks from a shared project backlog by exchanging messages directly --
no supervisor routes work between them.

This is a fresh scenario, deliberately different from the lesson's
Harrowgate Logistics Exchange/DockScout-YardScout hook. The point is
applying this chapter's peer-to-peer coordination concepts (message
validation, shared claim-checking, deadlock, tie-breaking, cross-agent
attribution) to a system you haven't seen before.

How to run:
    python3 starter.py
Prints a score report. Fill in each # TODO, re-run, and watch your
score climb toward the total (19 points across 7 tasks).
"""

import threading
from collections import Counter


# ---------------------------------------------------------------------------
# Task 1: Map five Bellcrest facts to the single BEST-matching
# multi-agent communication concept from this list:
#   "miscommunication", "duplicated work", "deadlock",
#   "fail-closed validation", "consensus/tie-breaking"
#
# Fact A: DevScout receives a message with the key "tsk_id" instead of
#         "task_id" -- it has no way to know this means the same thing
#         without guessing, and guessing wrong would mean acting on the
#         wrong task entirely.
# Fact B: DesignScout and DevScout, with no shared check between them,
#         BOTH independently claim the same backlog task on the same
#         morning.
# Fact C: Both agents are configured to always wait for the other to
#         propose a task split first -- neither one ever sends the
#         first message, so neither ever makes progress.
# Fact D: A receiving agent checks that every required message field is
#         present (after normalizing safe whitespace) before acting on
#         it, and refuses to guess at a missing or renamed field.
# Fact E: DesignScout and DevScout disagree about who should take task
#         T-40; a pre-agreed rule (not a negotiation) decides who wins.
# ---------------------------------------------------------------------------

TASK_1_ANSWERS = {
    "fact_a": None,  # TODO 1
    "fact_b": None,  # TODO 2
    "fact_c": None,  # TODO 3
    "fact_d": None,  # TODO 4
    "fact_e": None,  # TODO 5
}


def score_exercise_1():
    correct = {
        "fact_a": "miscommunication",
        "fact_b": "duplicated work",
        "fact_c": "deadlock",
        "fact_d": "fail-closed validation",
        "fact_e": "consensus/tie-breaking",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Should a receiving agent guess that an unrecognized field name
# (e.g., "tsk_id") maps to a known required field (e.g., "task_id")
# rather than rejecting the message? Answer "YES" or "NO".
# ---------------------------------------------------------------------------
TASK_2_ANSWER = None  # TODO 6: "YES" or "NO"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# TODO 7 (production-gear): parse_message_safely -- normalize whitespace
# in keys (safe), then check every field in required_fields is present
# in the normalized dict. Return {"ok": False, "reason": ...} naming the
# missing fields if any are missing, else {"ok": True, "fields": ...}.
# ---------------------------------------------------------------------------
def parse_message_safely(raw_args, required_fields=("recipient", "type", "task_id")):
    # TODO 7: implement as described above.
    return {"ok": True, "fields": raw_args}


# ---------------------------------------------------------------------------
# TODO 8 (production-gear): coordinated_claim -- a shared, LOCKED
# claim-check. If task_id is already in _shared_claims, return
# "{agent_name} SKIPPED {task_id} -- already claimed". Otherwise add
# task_id to _shared_claims and return "{agent_name} claimed {task_id}".
# The check and the add must happen inside the SAME locked block.
# ---------------------------------------------------------------------------
_shared_claims = set()
_shared_lock = threading.Lock()


def coordinated_claim(agent_name, task_id):
    # TODO 8: implement as described above.
    return f"{agent_name} claimed {task_id}"


# ---------------------------------------------------------------------------
# TODO 9 (production-gear): which_agent_caused_miscommunication --
# message-level cross-agent attribution. exchange is a list of (sender,
# msg_type, interpreted_ok) tuples. Return the SENDER of the first
# tuple whose interpreted_ok is False, or None if every message was
# interpreted correctly.
# ---------------------------------------------------------------------------
def which_agent_caused_miscommunication(exchange):
    # TODO 9: implement as described above.
    return None


# ---------------------------------------------------------------------------
# TODO 10 (production-gear): classify_communication_gap. Check, in this
# exact order, and return the first matching string:
#   "validates_message_fields" is False -> "no message validation"
#   "checks_shared_state_before_claiming" is False -> "no shared claim-check"
#   "detects_deadlock_with_timeout" is False -> "no deadlock timeout"
#   "has_preagreed_tiebreaker" is False -> "no pre-agreed tie-breaker"
#   "attributes_to_specific_message" is False -> "no message-level attribution"
#   otherwise -> "no known gap"
# ---------------------------------------------------------------------------
def classify_communication_gap(setup):
    # TODO 10: implement as described above.
    return "no known gap"


# ---------------------------------------------------------------------------
# TODO 11 (production-gear): resolve_conflicting_claims -- consensus
# voting with fail-closed tie handling. votes is a dict agent -> who
# they think should get the task. Use collections.Counter to count the
# votes; if the top two counts are EQUAL, return None (escalate, don't
# guess). Otherwise return the most-voted-for value.
# ---------------------------------------------------------------------------
def resolve_conflicting_claims(votes):
    # TODO 11: implement as described above.
    return None


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

def self_check():
    results = []
    score = 0
    total = 0

    s1, t1 = score_exercise_1()
    score += s1; total += t1
    results.append((f"Task 1: fact-to-concept mapping ({s1}/{t1})", s1 == t1))

    s2, t2 = score_exercise_2()
    score += s2; total += t2
    results.append((f"Task 2: validation reasoning ({s2}/{t2})", s2 == t2))

    v1 = parse_message_safely({"recipient": "DevScout", " type ": "claim", "task_id": "T-12"})
    v2 = parse_message_safely({"recipient": "DevScout", "kind": "claim", "task_id": "T-12"})
    ok3 = v1["ok"] is True and v2["ok"] is False
    results.append((f"Task 3: parse_message_safely normalizes whitespace but fails closed on a renamed field", ok3))
    if ok3:
        score += 3
    total += 3

    global _shared_claims
    _shared_claims = set()
    c1 = coordinated_claim("designscout", "T-20")
    c2 = coordinated_claim("devscout", "T-20")
    ok4 = "claimed" in c1 and "SKIPPED" in c2
    results.append((f"Task 4: coordinated_claim prevents a duplicate claim (c1='{c1}', c2='{c2}')", ok4))
    if ok4:
        score += 3
    total += 3

    t_fail = [("designscout", "claim", True), ("devscout", "claim", False), ("designscout", "ack", True)]
    t_pass = [("designscout", "claim", True), ("devscout", "ack", True)]
    w1 = which_agent_caused_miscommunication(t_fail)
    w2 = which_agent_caused_miscommunication(t_pass)
    ok5 = w1 == "devscout" and w2 is None
    results.append((f"Task 5: which_agent_caused_miscommunication (fail='{w1}', pass='{w2}')", ok5))
    if ok5:
        score += 3
    total += 3

    d1 = classify_communication_gap({"validates_message_fields": False})
    d2 = classify_communication_gap({"validates_message_fields": True, "checks_shared_state_before_claiming": False})
    d3 = classify_communication_gap({"validates_message_fields": True, "checks_shared_state_before_claiming": True,
                                      "detects_deadlock_with_timeout": True, "has_preagreed_tiebreaker": True,
                                      "attributes_to_specific_message": True})
    ok6 = d1 == "no message validation" and d2 == "no shared claim-check" and d3 == "no known gap"
    results.append(("Task 6: classify_communication_gap classifies all three cases correctly", ok6))
    if ok6:
        score += 2
    total += 2

    maj = resolve_conflicting_claims({"designscout": "devscout", "devscout": "devscout", "observer": "designscout"})
    tie = resolve_conflicting_claims({"designscout": "designscout", "devscout": "devscout"})
    ok7 = maj == "devscout" and tie is None
    results.append((f"Task 7: resolve_conflicting_claims (majority='{maj}', tie='{tie}', expect 'devscout' and None)", ok7))
    if ok7:
        score += 2
    total += 2

    print("Chapter 10 Exercises -- Structural Self-Check")
    print("=" * 70)
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("=" * 70)
    print(f"Score: {score}/{total}")


if __name__ == "__main__":
    self_check()
