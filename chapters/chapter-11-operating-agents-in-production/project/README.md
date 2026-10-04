# Chapter 11 Project: An Overnight Operating Harness for Wrenfield Dispatch Alliance

This is a **chapter mini-project**, not one of this course's numbered
L1-L4 projects. Per `docs/curriculum/CURRICULUM_MAP.md`'s project
ladder, the **L3 Independent project** ("design and implement a
reliability-instrumented, cost-bounded agent for a given problem, no
scaffold") was deferred past Chapter 8, past Chapter 9, and past
Chapter 10. This session's decision on whether it is built or deferred
a fifth time is recorded explicitly in
`quality-audits/chapter-11-audit.md` and in `PROJECT_STATE.md`'s
hand-off for Chapter 12 — see those files, not this one, for that
decision. This mini-project exists so this chapter's own three pillars
(idempotent commits, bounded retries, and a crash-survivable run
summary) get one combined, hands-on build of their own, the same
pattern Chapters 7-10's mini-projects used. Scenario: **Wrenfield
Dispatch Alliance**, a fictional regional freight alliance, runs two
PEER agents — **ClaimScout** and **ShipScout** — that confirm shipment
dispatches overnight, unattended, the same way the lesson's DockScout
and YardScout coordinated shipments during the day.

## The three pillars, combined

**Idempotent commits.** `idempotency_key()` + `commit_once()` key a
side effect on the fields that DEFINE it (agent, shipment, action),
not its raw call arguments — the same fix the lesson's Section 4-5
built after a real retried call drifted its own argument shape.

**Bounded retries.** `call_with_retries()` retries a flaky call up to
a fixed number of attempts, backing off between them, and logs every
attempt (including final exhaustion) rather than retrying silently
forever.

**Crash-survivable run summary.** `run_summary_from_log()` computes
dispatch counts, success rate, commits, and retry/exhaustion counts by
RE-PARSING the structured log, not from any in-memory counter — the
same guarantee the lesson's Section 11 built.

## The three TODOs

`starter.py` gives you the assembled overnight harness
(`run_wrenfield_night()`) already implemented — this project is about
the *idempotency, retry, and summary* layer underneath it, not
re-building the harness's own case-walking logic.

1. **TODO 1** — `idempotency_key()` + `commit_once()`: key on the
   fields that define the side effect; replay, never re-run, on a
   repeated key.
2. **TODO 2** — `call_with_retries()`: bounded attempts, exponential
   backoff, every attempt logged, `RetriesExhausted` raised on total
   failure.
3. **TODO 3** — `run_summary_from_log()`: a summary computed entirely
   by re-parsing the log.

## Why deterministic, constructed cases, not a live Ollama call

Same grading policy as this chapter's own lesson and every prior
chapter's `exercises/`/`practice/`/`project/`: `solution.py`'s
pass/fail checks never depend on a live model, so grading works the
same way everywhere, including CI with no Ollama server running.

## How to run it

```bash
python3 starter.py
```

This prints a structural self-check: 9 checks across idempotency,
retries, and the assembled overnight harness.

## How to check your work for real

1. Run the structural self-check above until all 9 checks pass.
2. Compare your implementation against `solution.py` — not to match
   its exact line-for-line shape, but to check whether your logic
   handles the same cases the same way.
3. Self-grade against `RUBRIC.md`.
4. Optional extension: add a per-case `max_agent_s`/`max_exchange_s`
   timeout check (the lesson's Section 8 pattern) to
   `run_wrenfield_night()`, and report which layer, if any, each case
   would have tripped.

## Files

- `starter.py` — the scaffold with 3 `# TODO`s and the self-check.
- `solution.py` — the fully filled-in reference; passes all 9 checks.
- `RUBRIC.md` — self-grading criteria.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a
  fourth scenario.
