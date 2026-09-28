"""
Chapter 4 Exercises: Memory and State -- REFERENCE SOLUTION
Scenario: Driftwood Legal Clinic, a fictional legal-aid clinic. Its
intake agent, IntakeBot, handles a separate phone/chat session for
each client visit, and needs to remember accessibility accommodations
and scheduling preferences a client states in ONE visit so a receptionist
booking a follow-up hearing weeks later automatically gets it right --
without a vector database or embedding framework, per this course's
memory-chapter scope. This is a fresh scenario, deliberately different
from the lesson's Larkspur Fitness Studio/CoachBot hook.

How to run:
    python3 solution.py
"""

import json
import os


MEMORY_PATH = "intakebot_memory_solution.json"

CASES = {
    "case-501": {"type": "eviction_defense", "status": "open"},
    "case-733": {"type": "benefits_appeal", "status": "open"},
}


def get_case_status(case_id):
    return CASES.get(case_id, {"error": f"no case on file for '{case_id}'"})


def load_all_memory(path=MEMORY_PATH):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def get_client_facts(client_id, path=MEMORY_PATH):
    return load_all_memory(path).get(client_id, {"accommodations": [], "preferences": []})


def save_client_facts(client_id, facts, path=MEMORY_PATH):
    all_memory = load_all_memory(path)
    all_memory[client_id] = facts
    with open(path, "w") as f:
        json.dump(all_memory, f, indent=2)
    return facts


# ---------------------------------------------------------------------------
# Task 1: Map five IntakeBot facts to the memory concept each is about.
# Concepts: "short-term working memory", "long-term persisted memory",
#           "token-budget pruning", "promote-worthy fact detection",
#           "read-modify-write merge bug"
# ---------------------------------------------------------------------------
TASK_1_ANSWERS = {
    "fact_a": "short-term working memory",
    "fact_b": "long-term persisted memory",
    "fact_c": "token-budget pruning",
    "fact_d": "promote-worthy fact detection",
    "fact_e": "read-modify-write merge bug",
}


def score_exercise_1():
    correct = {
        "fact_a": "short-term working memory",
        "fact_b": "long-term persisted memory",
        "fact_c": "token-budget pruning",
        "fact_d": "promote-worthy fact detection",
        "fact_e": "read-modify-write merge bug",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Dependency reasoning.
# ---------------------------------------------------------------------------
TASK_2_ANSWER = "MORE likely"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "MORE likely" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): promote-worthy classifier.
# ---------------------------------------------------------------------------
def is_promote_worthy(message_text):
    text = message_text.lower()
    accommodation_words = ["wheelchair", "interpreter", "hearing", "accessib", "disab"]
    preference_words = ["prefer", "morning", "afternoon", "call instead", "text instead"]
    if any(w in text for w in accommodation_words):
        return "accommodation"
    if any(w in text for w in preference_words):
        return "preference"
    return None


def score_exercise_3():
    points = 0
    if is_promote_worthy("I have hearing loss and need an ASL interpreter") == "accommodation":
        points += 1
    if is_promote_worthy("yeah that makes sense, thanks") is None:
        points += 1
    return points, 2


# ---------------------------------------------------------------------------
# Task 4 (production-gear): read-modify-write add function -- fixes the
# blind-overwrite bug described in fact_e.
# ---------------------------------------------------------------------------
def add_accommodation(client_id, note, path=MEMORY_PATH):
    facts = get_client_facts(client_id, path)
    facts["accommodations"].append(note)
    return save_client_facts(client_id, facts, path)


def score_exercise_4():
    test_path = "test_task4_solution.json"
    if os.path.exists(test_path):
        os.remove(test_path)
    save_client_facts("cl-9", {"accommodations": ["wheelchair-accessible room"], "preferences": []}, test_path)
    add_accommodation("cl-9", "ASL interpreter needed", test_path)
    result = get_client_facts("cl-9", test_path)
    points = 0
    if "wheelchair-accessible room" in result["accommodations"]:
        points += 1
    if "ASL interpreter needed" in result["accommodations"]:
        points += 1
    if os.path.exists(test_path):
        os.remove(test_path)
    return points, 2


# ---------------------------------------------------------------------------
# Task 5 (production-gear): merge persisted facts into a fresh working
# context.
# ---------------------------------------------------------------------------
def build_working_context(client_id, path=MEMORY_PATH):
    working_memory = []
    facts = get_client_facts(client_id, path)
    if facts["accommodations"]:
        working_memory.append({"role": "system", "content": f"Known accommodations (persisted): {'; '.join(facts['accommodations'])}"})
    if facts["preferences"]:
        working_memory.append({"role": "system", "content": f"Known preferences (persisted): {'; '.join(facts['preferences'])}"})
    return working_memory


def score_exercise_5():
    test_path = "test_task5_solution.json"
    if os.path.exists(test_path):
        os.remove(test_path)
    points = 0
    ctx_empty = build_working_context("cl-none", test_path)
    if ctx_empty == []:
        points += 1
    save_client_facts("cl-10", {"accommodations": ["wheelchair-accessible room"], "preferences": []}, test_path)
    ctx_full = build_working_context("cl-10", test_path)
    if len(ctx_full) == 1 and "wheelchair-accessible room" in ctx_full[0]["content"]:
        points += 1
    if os.path.exists(test_path):
        os.remove(test_path)
    return points, 2


# ---------------------------------------------------------------------------
# Task 6 (production-gear): Diagnose a failure type from a trace.
# ---------------------------------------------------------------------------
# IntakeBot's first save_client_facts() draft built {"accommodations": [],
# "preferences": [new_pref]} from scratch on every call instead of loading
# the client's existing facts first -- so recording a new scheduling
# preference silently deleted a wheelchair-accommodation note recorded the
# week before. Name the failure using the exact concept string from Task 1.
TASK_6_ANSWER = "read-modify-write merge bug"


def score_exercise_6():
    return (1 if TASK_6_ANSWER == "read-modify-write merge bug" else 0), 1


# ---------------------------------------------------------------------------
# Task 7 (production-gear): promote-before-prune -- any promote-worthy
# message must be written to the persisted store BEFORE it's allowed to be
# summarized/dropped from working memory, or it's lost for good.
# ---------------------------------------------------------------------------
def promote_before_prune(client_id, working_memory, path=MEMORY_PATH):
    for m in working_memory:
        if m["role"] != "user":
            continue
        category = is_promote_worthy(m["content"])
        if category == "accommodation":
            add_accommodation(client_id, m["content"], path)
    return get_client_facts(client_id, path)


def score_exercise_7():
    test_path = "test_task7_solution.json"
    if os.path.exists(test_path):
        os.remove(test_path)
    convo = [
        {"role": "user", "content": "When's my hearing?"},
        {"role": "user", "content": "I need a wheelchair-accessible room for it."},
        {"role": "assistant", "content": "Noted, I'll flag that."},
    ]
    facts = promote_before_prune("cl-11", convo, test_path)
    points = 1 if any("wheelchair" in a for a in facts["accommodations"]) else 0
    # Simulate pruning AFTER promotion -- the fact must survive on disk
    # even though `convo` itself is about to be discarded/summarized.
    del convo
    facts_after = get_client_facts("cl-11", test_path)
    if any("wheelchair" in a for a in facts_after["accommodations"]):
        points += 1
    if os.path.exists(test_path):
        os.remove(test_path)
    return points, 2


# ---------------------------------------------------------------------------
# Task 8: Full-checklist completeness check.
# ---------------------------------------------------------------------------
def score_exercise_8():
    concepts_touched = set(v for v in TASK_1_ANSWERS.values() if v)
    all_five = {
        "short-term working memory", "long-term persisted memory",
        "token-budget pruning", "promote-worthy fact detection",
        "read-modify-write merge bug",
    }
    points = 1 if concepts_touched == all_five else 0
    return points, 1


def main():
    tasks = [
        ("Task 1: Map facts to memory concepts", score_exercise_1),
        ("Task 2: Dependency reasoning", score_exercise_2),
        ("Task 3 (production-gear): Promote-worthy classifier", score_exercise_3),
        ("Task 4 (production-gear): Read-modify-write add function", score_exercise_4),
        ("Task 5 (production-gear): Merge into working context", score_exercise_5),
        ("Task 6 (production-gear): Failure diagnosis", score_exercise_6),
        ("Task 7 (production-gear): Promote-before-prune", score_exercise_7),
        ("Task 8: Completeness check", score_exercise_8),
    ]
    total_earned, total_possible = 0, 0
    print("Chapter 4 Exercises -- Score Report (SOLUTION)")
    print("=" * 50)
    for name, fn in tasks:
        earned, possible = fn()
        total_earned += earned
        total_possible += possible
        print(f"{name}: {earned}/{possible}")
    print("=" * 50)
    print(f"TOTAL: {total_earned}/{total_possible}")
    if os.path.exists(MEMORY_PATH):
        os.remove(MEMORY_PATH)


if __name__ == "__main__":
    main()
