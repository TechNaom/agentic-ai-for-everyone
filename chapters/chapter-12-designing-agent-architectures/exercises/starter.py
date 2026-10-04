"""
Chapter 12 Exercises: Designing Agent Architectures
Scenario: Lantern Hill Senior Living, a fictional senior-living
community. Its proposed agent handles two very different request
types -- routine medication check-ins and 24/7 unattended fall-sensor
alert dispatch -- against the SAME decision framework the lesson
built, applied here cold to a fresh scenario.

This is a fresh scenario, deliberately different from the lesson's
Copperfield Municipal Utilities hook. The point is applying this
chapter's decision framework to a system you haven't seen before --
recalling the lesson's answers by heart won't get you through these.

How to run:
    python3 starter.py
It prints a score report. Fill in each # TODO, re-run, and watch your
score climb toward the total (17 points across 7 tasks).
"""

import json


# ---------------------------------------------------------------------------
# Task 1 (5 pts): Map five Lantern Hill facts to the single BEST-
# matching decision-framework concept. Choose from:
#   "single-agent characterization", "multi-agent characterization",
#   "guardrails load-bearing", "operating layer load-bearing",
#   "reliability measurement load-bearing",
#   "architecture smell: over-engineering",
#   "architecture smell: under-engineering"
#
# fact_a: "Medication check-ins and fall-alert dispatch both read/write
#          the SAME resident record."
# fact_b: "The fall-sensor monitor runs 24/7 with no staff watching it."
# fact_c: "A missed fall alert or a wrongly dispatched nurse both have
#          real safety/cost consequences."
# fact_d: "A proposed design adds a second peer agent for fall alerts
#          with no concurrent-actor need."
# fact_e: "A proposed design has nurse-dispatch (irreversible, costly)
#          with no approval guardrail."
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
        "fact_a": "single-agent characterization",
        "fact_b": "operating layer load-bearing",
        "fact_c": "reliability measurement load-bearing",
        "fact_d": "architecture smell: over-engineering",
        "fact_e": "architecture smell: under-engineering",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2 (1 pt): Should Lantern Hill's design be characterized as
# multi-agent just because medication check-ins and emergency fall
# alerts are VERY different in tone and urgency? Answer "YES" or "NO".
# ---------------------------------------------------------------------------
TASK_2_ANSWER = None  # TODO 6


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# Tasks 3-7 (decision-gear): the lesson's own framework functions,
# GIVEN below unchanged -- your job is TODOs 7-11 only, filling in
# LANTERN_HILL_PROBLEM's facts and reading the framework's own verdict.
# ---------------------------------------------------------------------------
def characterize_problem(problem):
    if problem.get("distinct_specialized_subtasks") and problem.get("subtasks_can_run_independently"):
        return {"multi_agent_justified": True,
                "reason": "distinct, specialized subtasks that can proceed independently"}
    if problem.get("requires_concurrent_independent_actors"):
        return {"multi_agent_justified": True,
                "reason": "multiple independent actors must act at the same time on a shared resource"}
    return {"multi_agent_justified": False,
            "reason": "one agent, multiple tools, is sufficient"}


MECHANISM_TESTS = {
    "memory (Ch4)": lambda p: p.get("facts_must_persist_across_separate_sessions", False),
    "reflection (Ch5)": lambda p: p.get("has_a_hard_to_verify_free_text_output", False),
    "guardrails (Ch6)": lambda p: p.get("has_an_irreversible_or_costly_action", False),
    "reliability measurement (Ch7)": lambda p: p.get("failures_are_costly_enough_to_measure", False),
    "cost control (Ch8)": lambda p: p.get("runs_at_volume_or_has_a_cost_ceiling", False),
    "multi-agent dispatch (Ch9)": lambda p: p.get("multi_agent_justified", False),
    "peer communication (Ch10)": lambda p: p.get("multi_agent_justified", False) and p.get("requires_concurrent_independent_actors", False),
    "operating layer (Ch11)": lambda p: p.get("runs_unattended", False),
}


def select_mechanisms(problem):
    return {name: test(problem) for name, test in MECHANISM_TESTS.items()}


def reliability_cost_budget(problem):
    if problem.get("has_an_irreversible_or_costly_action"):
        return {"min_task_success_rate": 0.95, "max_cost_per_run": 0.08}
    return {"min_task_success_rate": 0.85, "max_cost_per_run": 0.15}


def architecture_smell_check(problem, selected):
    flags = []
    if selected.get("multi-agent dispatch (Ch9)") and not problem.get("distinct_specialized_subtasks"):
        flags.append("OVER-ENGINEERED: multi-agent chosen with no distinct specialized subtasks")
    if problem.get("has_an_irreversible_or_costly_action") and not selected.get("guardrails (Ch6)"):
        flags.append("UNDER-ENGINEERED: an irreversible/costly action exists with NO guardrail")
    if problem.get("runs_unattended") and not selected.get("operating layer (Ch11)"):
        flags.append("UNDER-ENGINEERED: runs unattended with no operating layer")
    if selected.get("reflection (Ch5)") and not problem.get("has_a_hard_to_verify_free_text_output"):
        flags.append("OVER-ENGINEERED: reflection chosen with no hard-to-verify output")
    return flags


def build_adr(name, problem, verdict, selected, budget, flags):
    lines = [f"ARCHITECTURE DECISION RECORD -- {name}",
             f"multi-agent: {verdict['multi_agent_justified']}"]
    for mech, needed in selected.items():
        if needed:
            lines.append(f"load-bearing: {mech}")
    lines.append(f"min_task_success_rate: {budget['min_task_success_rate']}")
    lines.append(f"max_cost_per_run: {budget['max_cost_per_run']}")
    lines.append(f"flags: {flags if flags else 'none'}")
    return "\n".join(lines)


# TODO 7: fill in LANTERN_HILL_PROBLEM's facts (read the scenario above
# and this chapter's own lesson Section 7 for the shape expected).
LANTERN_HILL_PROBLEM = {
    "distinct_specialized_subtasks": None,
    "subtasks_can_run_independently": None,
    "requires_concurrent_independent_actors": None,
    "facts_must_persist_across_separate_sessions": None,
    "has_a_hard_to_verify_free_text_output": None,
    "has_an_irreversible_or_costly_action": None,
    "failures_are_costly_enough_to_measure": None,
    "runs_at_volume_or_has_a_cost_ceiling": None,
    "runs_unattended": None,
}


def score_exercise_3():
    v = characterize_problem(LANTERN_HILL_PROBLEM)
    return (1 if v["multi_agent_justified"] is False else 0), 1


def score_exercise_4():
    sel = select_mechanisms(LANTERN_HILL_PROBLEM)
    ok = (sel["guardrails (Ch6)"] is True and sel["operating layer (Ch11)"] is True
          and sel["reliability measurement (Ch7)"] is True
          and sel["multi-agent dispatch (Ch9)"] is False)
    return (3 if ok else 0), 3


def score_exercise_5():
    b = reliability_cost_budget(LANTERN_HILL_PROBLEM)
    ok = b["min_task_success_rate"] == 0.95 and b["max_cost_per_run"] == 0.08
    return (2 if ok else 0), 2


# TODO 8: build a "good" mechanism selection for LANTERN_HILL_PROBLEM
# (hint: select_mechanisms(LANTERN_HILL_PROBLEM) IS the good selection,
# once TODO 7 above is filled in correctly).
def score_exercise_6():
    good_selection = select_mechanisms(LANTERN_HILL_PROBLEM)
    flags_good = architecture_smell_check(LANTERN_HILL_PROBLEM, good_selection)
    bad_selection = dict(good_selection)
    bad_selection["operating layer (Ch11)"] = False
    flags_bad = architecture_smell_check(LANTERN_HILL_PROBLEM, bad_selection)
    ok = len(flags_good) == 0 and len(flags_bad) == 1
    return (3 if ok else 0), 3


def score_exercise_7():
    v = characterize_problem(LANTERN_HILL_PROBLEM)
    sel = select_mechanisms(LANTERN_HILL_PROBLEM)
    b = reliability_cost_budget(LANTERN_HILL_PROBLEM)
    flags = architecture_smell_check(LANTERN_HILL_PROBLEM, sel)
    adr = build_adr("Lantern Hill Senior Living", LANTERN_HILL_PROBLEM, v, sel, b, flags)
    ok = ("operating layer (Ch11)" in adr and "guardrails (Ch6)" in adr
          and "flags: none" in adr)
    return (2 if ok else 0), 2


def self_check():
    results = []
    score = 0
    total = 0

    s1, t1 = score_exercise_1()
    score += s1; total += t1
    results.append((f"Task 1: fact-to-concept mapping ({s1}/{t1})", s1 == t1))

    s2, t2 = score_exercise_2()
    score += s2; total += t2
    results.append((f"Task 2: reasoning question ({s2}/{t2})", s2 == t2))

    s3, t3 = score_exercise_3()
    score += s3; total += t3
    results.append((f"Task 3: characterize_problem on Lantern Hill ({s3}/{t3})", s3 == t3))

    s4, t4 = score_exercise_4()
    score += s4; total += t4
    results.append((f"Task 4: select_mechanisms on Lantern Hill ({s4}/{t4})", s4 == t4))

    s5, t5 = score_exercise_5()
    score += s5; total += t5
    results.append((f"Task 5: reliability_cost_budget on Lantern Hill ({s5}/{t5})", s5 == t5))

    s6, t6 = score_exercise_6()
    score += s6; total += t6
    results.append((f"Task 6: architecture_smell_check catches the forgotten operating layer ({s6}/{t6})", s6 == t6))

    s7, t7 = score_exercise_7()
    score += s7; total += t7
    results.append((f"Task 7: build_adr assembles a consistent ADR ({s7}/{t7})", s7 == t7))

    print("Chapter 12 Exercises -- Structural Self-Check")
    print("=" * 70)
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("=" * 70)
    print(f"Score: {score}/{total}")


if __name__ == "__main__":
    self_check()
