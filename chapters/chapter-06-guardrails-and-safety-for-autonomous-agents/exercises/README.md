# Chapter 6 Exercises: Guardrails and Safety for Autonomous Agents

These exercises use a second scenario, deliberately different from the
lesson's Millbrook Credit Union/LedgerBot hook: **Amberlock
Self-Storage**, a fictional self-storage facility. Its operations
agent, **DispatchBot**, can check a unit's status, issue a refund,
remotely unlock a unit (a physical security override), and run a
facility "reconciliation script." Every one of those except the status
check is a real, consequential action a guardrail has to bound.
Applying this chapter's guardrail concepts to a fresh scenario is the
point — recalling the lesson's answers by heart won't get you through
these.

## How to run

You'll need Python 3 installed. Check with:

```bash
python3 --version
```

Then run the starter file:

```bash
python3 starter.py
```

It prints a score report. Fill in each `# TODO`, re-run, and watch
your score climb toward the total (19 points across 8 tasks).

## The eight tasks

1. **Map facts to guardrail concepts** — assign the correct concept
   (tool allowlist, human-approval checkpoint, sandboxed tool
   execution, action budget, fail-safe default deny) to five
   DispatchBot facts.
2. **Dependency reasoning** — decide whether an approval check that
   fails OPEN instead of fails SAFE makes an unapproved high-risk
   action more or less likely to execute.
3. **(Production-gear) Tool allowlist check** — refuse a tool name
   that was never actually given to the agent.
4. **(Production-gear) Approval-threshold check** — decide which
   actions require human approval before they can dispatch.
5. **(Production-gear) `dispatch_action` composition** — combine the
   allowlist, sandbox, and approval checks into one function that
   fails safe throughout.
6. **(Production-gear) Diagnose a failure type** — recognize a
   "system-prompt-only guardrail" from a real trace.
7. **(Production-gear) Fail-safe default deny** — treat an approval
   service's own error as "not approved," never as approved by
   default.
8. **Completeness check** — confirm all five guardrail concepts were
   actually used.

## Files

- `starter.py` — the scaffold with 11 `# TODO`s and the score report.
- `solution.py` — the fully filled-in reference; scores 19/19.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a third
  scenario.
