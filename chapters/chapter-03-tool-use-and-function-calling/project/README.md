# Chapter 3 Project: Robust Tool Use for RepairBot

This is a **chapter mini-project**, not one of this course's numbered
L1-L4 projects (per `docs/curriculum/CURRICULUM_MAP.md`'s project
ladder, this chapter's material is folded into the L2 Assisted project
that ships after Chapter 4, the same way Chapter 2's material was).
It exists so this chapter's three pillars get one combined, hands-on
build of their own before that larger project arrives. Scenario:
**Kestrel Appliance Service**, a fictional home-appliance repair
dispatcher, wants **RepairBot** built the same way the lesson's NetBot
was — a fresh scenario you build yourself.

## The three pillars, combined

**Tool selection.** `check_warranty_status(appliance_id)` is cheap and
decisive: an expired warranty alone explains the need for a repair
visit. `run_diagnostic(appliance_id)` is more expensive and should
only run if the warranty check doesn't already answer the question —
the same cheapest-decisive-signal-first discipline the lesson's
`diagnose_connectivity_issue()` used.

**Timeout-aware failure handling.** `run_diagnostic` can hang past a
configured budget (a realistic stand-in for a slow upstream call).
The right policy is a bounded retry, since a hang is often transient —
distinct from a malformed-output failure, which the lesson's Section
11 showed should never be retried.

**Outcome verification.** `schedule_repair_visit(ticket_id)` always
"succeeds," the same shape as the lesson's `restart_modem` — a clean
success dict that doesn't guarantee the appliance is actually fixed.
The only real check is independent evidence: `get_repair_ticket_status`.

## The three TODOs

`starter.py` gives you all the tool functions, fixtures, and the
`call_with_timeout` wrapper already implemented — this project is
about the *tool-use discipline* layer, not re-building Chapter 1's
tool-calling mechanics.

1. **TODO 1** — `diagnose_appliance_issue()`: the tool-selection
   function (warranty check before diagnostic).
2. **TODO 2** — `run_diagnostic_with_retry()`: the timeout-retry
   policy, mirroring the lesson's Section 12.
3. **TODO 3** — `verify_repair_outcome()`: the outcome-verification
   function, mirroring the lesson's Section 13.

## Why deterministic fixtures, not a live Ollama call

Same grading policy as this chapter's `exercises/` and `practice/`,
and Chapter 2's own project: `solution.py`'s pass/fail checks never
depend on a live model, so grading works the same way everywhere,
including CI with no Ollama server running. If you want the full live
experience once your self-check passes, swap the tool-selection
decision for a real `openai`-against-Ollama call using the exact
pattern from `lesson.html` Section 5 — `base_url=
"http://localhost:11434/v1"`, `model="llama3.2:latest"`.

## How to run it

```bash
python3 starter.py
```

This prints a structural self-check: 7 checks across tool selection
(warranty-first and diagnostic-fallthrough), timeout-retry recovery
(with and without a simulated hang), outcome verification (resolved
and unresolved cases), and one end-to-end composition check.

## How to check your work for real

1. Run the self-check above until all 7 checks pass.
2. Compare your implementation against `solution.py` — not to match
   its exact line-for-line shape, but to check whether your logic
   handles the same cases the same way.
3. Self-grade against `RUBRIC.md`.
4. Optional: try the live-Ollama swap described above.

## Files

- `starter.py` — the scaffold with 3 `# TODO`s and the self-check.
- `solution.py` — the fully filled-in reference; passes all 7 checks.
- `RUBRIC.md` — self-grading criteria.
- `ai-paired.html` — a solo-build-then-critique exercise using this
  same RepairBot scenario.
