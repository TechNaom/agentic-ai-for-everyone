"""
Module 6 Combined Assessment: Architecture-Design Exercise

Per docs/curriculum/CURRICULUM_MAP.md, Module 6's stated assessment is
an "architecture-design exercise," scoped to Chapter 12 alone (Chapter
13's own "capstone rubric" is a separate deliverable -- see README.md
for why this module's assessment doesn't span both chapters the way
every prior module's did).

How to run:
    python3 starter.py
Fill in each # TODO, re-run, and watch the self-check climb toward
5/6 objectively-checkable parts (Part 6 is a free-text synthesis,
self-graded against RUBRIC.md).
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


# The scenario: Alderwood Transit Cooperative books paratransit rides
# (cancelling a scheduled ride late is costly to the rider and the
# co-op both) AND dispatches an unattended overnight wheelchair-lift
# maintenance alert (a lift fault reported at 3 AM must page a
# technician with no staff watching).
ALDERWOOD_PROBLEM = {
    "_context": "Alderwood Transit Cooperative books paratransit rides and "
                "dispatches overnight, unattended wheelchair-lift "
                "maintenance alerts.",
    "distinct_specialized_subtasks": False,
    "subtasks_can_run_independently": False,
    "requires_concurrent_independent_actors": False,
    "facts_must_persist_across_separate_sessions": False,
    "has_a_hard_to_verify_free_text_output": False,
    "has_an_irreversible_or_costly_action": True,
    "failures_are_costly_enough_to_measure": True,
    "runs_at_volume_or_has_a_cost_ceiling": True,
    "runs_unattended": True,
}


# ---------------------------------------------------------------------------
# Part 1: call ch12.characterize_problem on ALDERWOOD_PROBLEM.
# ---------------------------------------------------------------------------
def part1_characterize():
    return None  # TODO: return ch12.characterize_problem(ALDERWOOD_PROBLEM)


# ---------------------------------------------------------------------------
# Part 2: call ch12.select_mechanisms, remembering to merge in
# multi_agent_justified from Part 1's verdict first.
# ---------------------------------------------------------------------------
def part2_select(verdict):
    return None  # TODO: merge verdict into ALDERWOOD_PROBLEM, call select_mechanisms


# ---------------------------------------------------------------------------
# Part 3: call ch12.reliability_cost_budget on ALDERWOOD_PROBLEM.
# ---------------------------------------------------------------------------
def part3_budget():
    return None  # TODO: return ch12.reliability_cost_budget(ALDERWOOD_PROBLEM)


# ---------------------------------------------------------------------------
# Part 4: run ch12.architecture_smell_check against the CORRECT
# selection (should be empty) and against a copy with
# "guardrails (Ch6)" deliberately set to False (should raise exactly
# one flag).
# ---------------------------------------------------------------------------
def part4_smell_check(selection):
    return None, None  # TODO: return (good_flags, bad_flags)


# ---------------------------------------------------------------------------
# Part 5: assemble the ADR with ch12.build_adr. Name at least one
# rejected alternative.
# ---------------------------------------------------------------------------
def part5_adr(verdict, selection, budget, flags):
    return None  # TODO: return ch12.build_adr(...)


# ---------------------------------------------------------------------------
# Part 6 (free text, self-graded): why does Alderwood need BOTH
# guardrails (Ch6) AND the operating layer (Ch11) -- not just one or
# the other? Name the specific, DIFFERENT fact each one is load-
# bearing for.
# ---------------------------------------------------------------------------
PART6_SYNTHESIS = ""  # TODO: write 3-5 sentences


def self_check():
    results = []

    verdict = part1_characterize()
    ok1 = bool(verdict) and verdict.get("multi_agent_justified") is False
    results.append(("1. Characterization reaches single-agent for Alderwood", ok1))

    selection = part2_select(verdict) if verdict else None
    ok2 = bool(selection) and (
        selection.get("guardrails (Ch6)") is True and
        selection.get("reliability measurement (Ch7)") is True and
        selection.get("cost control (Ch8)") is True and
        selection.get("operating layer (Ch11)") is True and
        selection.get("memory (Ch4)") is False and
        selection.get("multi-agent dispatch (Ch9)") is False
    )
    results.append(("2. select_mechanisms selects guardrails/reliability/cost/operating, not memory/multi-agent", ok2))

    budget = part3_budget()
    ok3 = bool(budget) and budget.get("min_task_success_rate") == 0.95 and budget.get("max_cost_per_run") == 0.08
    results.append(("3. reliability_cost_budget states the tight (irreversible-action) tier", ok3))

    good_flags, bad_flags = part4_smell_check(selection) if selection else (None, None)
    ok4 = good_flags is not None and bad_flags is not None and len(good_flags) == 0 and len(bad_flags) == 1
    results.append(("4. architecture_smell_check: zero flags on the correct design, one on the dropped guardrail", ok4))

    adr = part5_adr(verdict, selection, budget, good_flags) if ok4 else None
    ok5 = bool(adr) and "guardrails (Ch6)" in adr and "operating layer (Ch11)" in adr and "flags: none" in adr
    results.append(("5. build_adr assembles a consistent ADR naming both load-bearing mechanisms", ok5))

    ok6 = ("guardrail" in PART6_SYNTHESIS.lower() and
           "operating" in PART6_SYNTHESIS.lower() and
           len(PART6_SYNTHESIS.strip()) > 40)
    results.append(("6. Cross-cutting synthesis names both mechanisms (self-graded fully against RUBRIC.md)", ok6))

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
