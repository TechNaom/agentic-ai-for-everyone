"""
Module 6 Combined Assessment: Architecture-Design Exercise
Reference solution.

Per docs/curriculum/CURRICULUM_MAP.md, Module 6's stated assessment is
an "architecture-design exercise," scoped to Chapter 12 alone (Chapter
13, the capstone, has its own separate "capstone rubric (architecture
challenge, Level 4)" -- the curriculum map's own line explicitly
splits the two, unlike every prior module's single combined
assessment spanning all of that module's chapters). This exercise
therefore reuses Chapter 12's own decision-framework functions,
loaded unchanged from its project file, applied to ONE brand-new
scenario not used anywhere else in this course.

How to run:
    python3 solution.py
Prints the assembled ADR, then a self-check. Scores 6/6.
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def _load(module_name, rel_path):
    path = os.path.join(REPO_ROOT, rel_path)
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ch12 = _load(
    "ch12_solution",
    "chapters/chapter-12-designing-agent-architectures/project/solution.py",
)


# ---------------------------------------------------------------------------
# The scenario: Alderwood Transit Cooperative -- a fifth fictional
# organization for Chapter 12's own content set (lesson used Copperfield
# Municipal Utilities, exercises used Lantern Hill Senior Living,
# exercises' ai-paired used Vantage Peak Ski Resorts, the project used
# Driftlight Energy Cooperative, the project's own ai-paired used
# Mirelake Water Authority -- this is a SIXTH, for the module assessment
# alone, never reused anywhere else).
#
# Alderwood runs paratransit ride booking (cancelling a scheduled ride
# late is costly to the rider and the co-op both) AND an unattended
# overnight wheelchair-lift maintenance-alert dispatch (a lift fault
# reported at 3 AM must page a technician with no staff watching).
# ---------------------------------------------------------------------------
ALDERWOOD_PROBLEM = {
    "_context": "Alderwood Transit Cooperative books paratransit rides and "
                "dispatches overnight, unattended wheelchair-lift "
                "maintenance alerts.",
    "distinct_specialized_subtasks": False,         # both read/write the
        # SAME ride/vehicle record
    "subtasks_can_run_independently": False,
    "requires_concurrent_independent_actors": False,
    "facts_must_persist_across_separate_sessions": False,  # no stated
        # cross-session fact to remember here, unlike Driftlight's pledge
    "has_a_hard_to_verify_free_text_output": False,
    "has_an_irreversible_or_costly_action": True,    # a late ride
        # cancellation has a real cost to the rider and the co-op
    "failures_are_costly_enough_to_measure": True,   # a missed lift-fault
        # page is a safety incident, not just an inconvenience
    "runs_at_volume_or_has_a_cost_ceiling": True,
    "runs_unattended": True,                          # the lift-fault
        # monitor runs 24/7 with no staff watching
}


# ---------------------------------------------------------------------------
# Part 1 -- characterization
# ---------------------------------------------------------------------------
def part1_characterize():
    return ch12.characterize_problem(ALDERWOOD_PROBLEM)


# ---------------------------------------------------------------------------
# Part 2 -- mechanism selection
# ---------------------------------------------------------------------------
def part2_select(verdict):
    problem = {**ALDERWOOD_PROBLEM, "multi_agent_justified": verdict["multi_agent_justified"]}
    return ch12.select_mechanisms(problem)


# ---------------------------------------------------------------------------
# Part 3 -- reliability/cost budget
# ---------------------------------------------------------------------------
def part3_budget():
    return ch12.reliability_cost_budget(ALDERWOOD_PROBLEM)


# ---------------------------------------------------------------------------
# Part 4 -- smell check (run against both the correct selection AND a
# deliberately wrong one, to prove the check actually discriminates)
# ---------------------------------------------------------------------------
def part4_smell_check(selection):
    good_flags = ch12.architecture_smell_check(ALDERWOOD_PROBLEM, selection)
    bad_selection = dict(selection)
    bad_selection["guardrails (Ch6)"] = False  # the mistake: dropped the
        # guardrail despite the irreversible cancellation action
    bad_flags = ch12.architecture_smell_check(ALDERWOOD_PROBLEM, bad_selection)
    return good_flags, bad_flags


# ---------------------------------------------------------------------------
# Part 5 -- the Architecture Decision Record
# ---------------------------------------------------------------------------
def part5_adr(verdict, selection, budget, flags):
    tradeoffs = [
        {"alternative": "multi-agent split, one agent for bookings and one "
             "for lift maintenance",
         "why_rejected": "both read/write the same ride/vehicle record "
             "with no independent-execution benefit -- Ch9's dispatch "
             "overhead buys nothing here"},
    ]
    return ch12.build_adr("Alderwood Transit Cooperative", ALDERWOOD_PROBLEM,
                           verdict, selection, budget, tradeoffs, flags)


# ---------------------------------------------------------------------------
# Part 6 -- cross-cutting synthesis (the one genuinely new question this
# assessment adds beyond just re-running Chapter 12's own functions):
# why does Alderwood need guardrails AND the operating layer TOGETHER,
# not just one or the other?
# ---------------------------------------------------------------------------
PART6_SYNTHESIS = (
    "Alderwood's lift-fault alert runs unattended (the operating layer is "
    "load-bearing: idempotent paging, timeouts, structured logging), but "
    "the SEPARATE ride-cancellation path is attended and irreversible "
    "(the guardrail is load-bearing: a human-approval checkpoint before a "
    "late cancellation fires). Dropping either mechanism leaves a real, "
    "distinct gap: no guardrail means an unattended system could also "
    "auto-cancel rides with no approval; no operating layer means a "
    "retried page could double-notify or silently drop a lift fault "
    "overnight. The two mechanisms are load-bearing for two DIFFERENT "
    "facts (an irreversible action vs. running unattended), not "
    "redundant with each other."
)


def self_check():
    results = []

    verdict = part1_characterize()
    ok1 = verdict["multi_agent_justified"] is False
    results.append(("1. Characterization reaches single-agent for Alderwood", ok1))

    selection = part2_select(verdict)
    ok2 = (selection["guardrails (Ch6)"] is True and
           selection["reliability measurement (Ch7)"] is True and
           selection["cost control (Ch8)"] is True and
           selection["operating layer (Ch11)"] is True and
           selection["memory (Ch4)"] is False and
           selection["multi-agent dispatch (Ch9)"] is False)
    results.append(("2. select_mechanisms selects guardrails/reliability/cost/operating, not memory/multi-agent", ok2))

    budget = part3_budget()
    ok3 = budget["min_task_success_rate"] == 0.95 and budget["max_cost_per_run"] == 0.08
    results.append(("3. reliability_cost_budget states the tight (irreversible-action) tier", ok3))

    good_flags, bad_flags = part4_smell_check(selection)
    ok4 = len(good_flags) == 0 and len(bad_flags) == 1
    results.append(("4. architecture_smell_check: zero flags on the correct design, one on the dropped guardrail", ok4))

    adr = part5_adr(verdict, selection, budget, good_flags)
    ok5 = ("guardrails (Ch6)" in adr and "operating layer (Ch11)" in adr and
           "flags: none" in adr)
    results.append(("5. build_adr assembles a consistent ADR naming both load-bearing mechanisms", ok5))

    ok6 = ("guardrail" in PART6_SYNTHESIS.lower() and
           "operating" in PART6_SYNTHESIS.lower() and
           "different" in PART6_SYNTHESIS.lower())
    results.append(("6. Cross-cutting synthesis names both mechanisms and why they're not redundant", ok6))

    print(adr)
    print()
    print("Module 6 Assessment -- Architecture-Design Exercise -- Self-Check")
    print("=" * 70)
    score = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        if ok:
            score += 1
    print("=" * 70)
    print(f"Score: {score}/{len(results)}")


if __name__ == "__main__":
    self_check()
