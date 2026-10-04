"""
Chapter 13 Exercises: Capstone -- Designing and Defending an
Autonomous Agent System
Scenario: a SUBSET of the lesson's own Thornwick Marketplace
Collective -- just Buyer Concierge and Fraud & Dispute Review,
with NO Maker Fulfillment component -- against the SAME decision
framework (characterize_problem/select_mechanisms/
reliability_cost_budget/architecture_smell_check/build_adr), applied
here cold to a fresh variant -- REFERENCE SOLUTION.

The point: removing ONE component (Maker Fulfillment) removes BOTH
the overnight-unattended fact AND the shared-inventory race -- which
should flip the operating layer AND peer communication from
load-bearing to NOT load-bearing, while leaving memory, reflection,
guardrails, reliability measurement, cost control, and multi-agent
dispatch untouched. Recalling the lesson's full-system verdicts by
heart will get half of this wrong.

How to run:
    python3 solution.py
Prints a score report. Scores 17/17.
"""


# ---------------------------------------------------------------------------
# Task 1: Map five facts about the two-component subset to the single
# BEST-matching decision-framework concept.
# ---------------------------------------------------------------------------
TASK_1_ANSWERS = {
    "fact_a": "multi-agent characterization",
    "fact_b": "operating layer NOT load-bearing",
    "fact_c": "peer communication NOT load-bearing",
    "fact_d": "reflection load-bearing",
    "fact_e": "guardrails load-bearing",
}


def score_exercise_1():
    correct = {
        "fact_a": "multi-agent characterization",
        "fact_b": "operating layer NOT load-bearing",
        "fact_c": "peer communication NOT load-bearing",
        "fact_d": "reflection load-bearing",
        "fact_e": "guardrails load-bearing",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Reasoning question. Removing Maker Fulfillment removes both
# the overnight-unattended fact and the shared-inventory race. Does
# multi-agent dispatch (Ch9) stop being justified too?
# ---------------------------------------------------------------------------
TASK_2_ANSWER = "NO"
    # Buyer Concierge and Fraud & Dispute Review are STILL two
    # distinct, specialized subtasks that can proceed independently --
    # that fact never depended on Maker Fulfillment existing at all.


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "NO" else 0), 1


# ---------------------------------------------------------------------------
# Tasks 3-7 (decision-gear): the lesson's own framework functions,
# reused unchanged (same logic as chapters/chapter-12-designing-agent-
# architectures/project/solution.py), applied to the subset.
# ---------------------------------------------------------------------------
def characterize_problem(problem):
    if problem.get("distinct_specialized_subtasks") and problem.get("subtasks_can_run_independently"):
        return {"multi_agent_justified": True,
                "reason": "distinct, specialized subtasks that can proceed "
                           "independently"}
    if problem.get("requires_concurrent_independent_actors"):
        return {"multi_agent_justified": True,
                "reason": "multiple independent actors must act at the "
                           "same time on a shared resource"}
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
    if problem.get("facts_must_persist_across_separate_sessions") and not selected.get("memory (Ch4)"):
        flags.append("UNDER-ENGINEERED: facts must persist across sessions with NO memory mechanism")
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


# Thornwick WITHOUT Maker Fulfillment: no overnight batch, no shared
# inventory race -- just Buyer Concierge (conversational ordering,
# allergy memory, hard-to-verify dispute-explanation text written back
# to buyers) and Fraud & Dispute Review (refund guardrail).
THORNWICK_SUBSET_PROBLEM = {
    "distinct_specialized_subtasks": True,      # conversational ordering
        # vs. fraud/dispute judgment are still two different skills
    "subtasks_can_run_independently": True,
    "requires_concurrent_independent_actors": False,  # no Maker
        # Fulfillment means no second actor racing on shared inventory
    "facts_must_persist_across_separate_sessions": True,   # the buyer's
        # allergy preference still has to survive to a LATER order
    "has_a_hard_to_verify_free_text_output": True,          # the written
        # dispute-resolution explanation is still free text
    "has_an_irreversible_or_costly_action": True,           # the refund
    "failures_are_costly_enough_to_measure": True,
    "runs_at_volume_or_has_a_cost_ceiling": True,
    "runs_unattended": False,                                 # NOTHING
        # here runs overnight once Maker Fulfillment is removed -- a
        # human buyer is present on one side of every conversation, and
        # dispute review happens during a reviewer's own shift
}


def score_exercise_3():
    v = characterize_problem(THORNWICK_SUBSET_PROBLEM)
    return (1 if v["multi_agent_justified"] is True else 0), 1


def _subset_with_verdict():
    v = characterize_problem(THORNWICK_SUBSET_PROBLEM)
    return {**THORNWICK_SUBSET_PROBLEM, "multi_agent_justified": v["multi_agent_justified"]}


def score_exercise_4():
    sel = select_mechanisms(_subset_with_verdict())
    ok = (sel["memory (Ch4)"] is True and sel["reflection (Ch5)"] is True and
          sel["guardrails (Ch6)"] is True and
          sel["multi-agent dispatch (Ch9)"] is True and
          sel["peer communication (Ch10)"] is False and
          sel["operating layer (Ch11)"] is False)
    return (3 if ok else 0), 3


def score_exercise_5():
    b = reliability_cost_budget(THORNWICK_SUBSET_PROBLEM)
    ok = b["min_task_success_rate"] == 0.95 and b["max_cost_per_run"] == 0.08
    return (2 if ok else 0), 2


def score_exercise_6():
    good_selection = select_mechanisms(_subset_with_verdict())
    flags_good = architecture_smell_check(THORNWICK_SUBSET_PROBLEM, good_selection)
    bad_selection = dict(good_selection)
    bad_selection["memory (Ch4)"] = False   # forgot it, despite the
        # allergy preference needing to persist
    flags_bad = architecture_smell_check(THORNWICK_SUBSET_PROBLEM, bad_selection)
    ok = len(flags_good) == 0 and len(flags_bad) == 1
    return (3 if ok else 0), 3


def score_exercise_7():
    v = characterize_problem(THORNWICK_SUBSET_PROBLEM)
    sel = select_mechanisms(_subset_with_verdict())
    b = reliability_cost_budget(THORNWICK_SUBSET_PROBLEM)
    flags = architecture_smell_check(THORNWICK_SUBSET_PROBLEM, sel)
    adr = build_adr("Thornwick (Buyer Concierge + Fraud Review subset)",
                     THORNWICK_SUBSET_PROBLEM, v, sel, b, flags)
    ok = ("memory (Ch4)" in adr and "operating layer (Ch11)" not in adr
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
    results.append((f"Task 3: characterize_problem on the subset ({s3}/{t3})", s3 == t3))

    s4, t4 = score_exercise_4()
    score += s4; total += t4
    results.append((f"Task 4: select_mechanisms on the subset ({s4}/{t4})", s4 == t4))

    s5, t5 = score_exercise_5()
    score += s5; total += t5
    results.append((f"Task 5: reliability_cost_budget on the subset ({s5}/{t5})", s5 == t5))

    s6, t6 = score_exercise_6()
    score += s6; total += t6
    results.append((f"Task 6: architecture_smell_check catches the forgotten memory mechanism ({s6}/{t6})", s6 == t6))

    s7, t7 = score_exercise_7()
    score += s7; total += t7
    results.append((f"Task 7: build_adr assembles a consistent ADR ({s7}/{t7})", s7 == t7))

    print("Chapter 13 Exercises -- Structural Self-Check")
    print("=" * 70)
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("=" * 70)
    print(f"Score: {score}/{total}")


if __name__ == "__main__":
    self_check()
