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
attribution) to a system you haven't seen before -- REFERENCE SOLUTION.

How to run:
    python3 solution.py
Prints a score report. Scores 19/19.
"""

import threading
from collections import Counter


# ---------------------------------------------------------------------------
# Task 1: Map five Bellcrest facts to the single BEST-matching
# multi-agent communication concept.
# ---------------------------------------------------------------------------
TASK_1_ANSWERS = {
    "fact_a": "miscommunication",
    "fact_b": "duplicated work",
    "fact_c": "deadlock",
    "fact_d": "fail-closed validation",
    "fact_e": "consensus/tie-breaking",
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
# Task 2: Reasoning question.
# ---------------------------------------------------------------------------
TASK_2_ANSWER = "NO"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): parse_message_safely -- normalize safe
# whitespace issues, fail closed on missing/renamed fields.
# ---------------------------------------------------------------------------
def parse_message_safely(raw_args, required_fields=("recipient", "type", "task_id")):
    normalized = {k.strip(): v for k, v in raw_args.items()}
    missing = [f for f in required_fields if f not in normalized]
    if missing:
        return {"ok": False, "reason": f"missing required fields after normalization: {missing}"}
    return {"ok": True, "fields": normalized}


# ---------------------------------------------------------------------------
# Task 4 (production-gear): coordinated_claim -- a shared, locked
# claim-check preventing duplicated work between two peers.
# ---------------------------------------------------------------------------
_shared_claims = set()
_shared_lock = threading.Lock()


def coordinated_claim(agent_name, task_id):
    with _shared_lock:
        if task_id in _shared_claims:
            return f"{agent_name} SKIPPED {task_id} -- already claimed"
        _shared_claims.add(task_id)
        return f"{agent_name} claimed {task_id}"


# ---------------------------------------------------------------------------
# Task 5 (production-gear): which_agent_caused_miscommunication --
# message-level cross-agent attribution.
# ---------------------------------------------------------------------------
def which_agent_caused_miscommunication(exchange):
    for sender, msg_type, interpreted_ok in exchange:
        if not interpreted_ok:
            return sender
    return None


# ---------------------------------------------------------------------------
# Task 6 (production-gear): classify_communication_gap.
# ---------------------------------------------------------------------------
def classify_communication_gap(setup):
    if setup.get("validates_message_fields") is False:
        return "no message validation"
    if setup.get("checks_shared_state_before_claiming") is False:
        return "no shared claim-check"
    if setup.get("detects_deadlock_with_timeout") is False:
        return "no deadlock timeout"
    if setup.get("has_preagreed_tiebreaker") is False:
        return "no pre-agreed tie-breaker"
    if setup.get("attributes_to_specific_message") is False:
        return "no message-level attribution"
    return "no known gap"


# ---------------------------------------------------------------------------
# Task 7 (production-gear): resolve_conflicting_claims -- consensus
# with fail-closed tie handling.
# ---------------------------------------------------------------------------
def resolve_conflicting_claims(votes):
    counts = Counter(votes.values())
    top = counts.most_common()
    if len(top) > 1 and top[0][1] == top[1][1]:
        return None
    return top[0][0]


# ---------------------------------------------------------------------------
# Structural self-check (identical to starter.py)
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
