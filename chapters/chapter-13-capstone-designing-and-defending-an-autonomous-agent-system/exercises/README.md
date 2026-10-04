# Chapter 13 Exercises: Capstone — Designing and Defending an Autonomous Agent System

These exercises use a **subset** of the lesson's own **Thornwick
Marketplace Collective** — just Buyer Concierge and Fraud & Dispute
Review, with the Maker Fulfillment component removed — against the
SAME decision framework the lesson applies at full scale
(`characterize_problem`/`select_mechanisms`/`reliability_cost_budget`/
`architecture_smell_check`/`build_adr`). Removing one component
removes BOTH the overnight-unattended fact and the shared-inventory
race, which should flip the operating layer AND peer communication
from load-bearing to NOT load-bearing — while leaving memory,
reflection, guardrails, reliability measurement, cost control, and
multi-agent dispatch untouched. Recalling the lesson's full-system
verdicts by heart will get half of this wrong — the point is tracing
each verdict back to the specific fact that changed.

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
your score climb toward the total (17 points across 7 tasks).

## The seven tasks

1. **Map facts to decision-framework concepts** — assign the correct
   concept (characterization, operating-layer NOT load-bearing,
   peer-communication NOT load-bearing, reflection load-bearing,
   guardrails load-bearing) to five subset facts.
2. **Reasoning question** — decide whether removing Maker Fulfillment
   also removes the justification for multi-agent dispatch itself.
3. **`characterize_problem` on the subset** — confirm the framework
   still reaches multi-agent, and for which specific reason.
4. **`select_mechanisms` on the subset** — confirm memory, reflection,
   guardrails, and multi-agent dispatch are still load-bearing, and
   peer communication and the operating layer are NOT.
5. **`reliability_cost_budget` on the subset** — confirm the tighter,
   irreversible-action tier still applies (the refund action didn't
   go anywhere).
6. **`architecture_smell_check`** — confirm a correct selection raises
   zero flags, and a selection that forgets memory (despite the
   allergy preference needing to persist) raises exactly one.
7. **`build_adr`** — assemble a consistent Architecture Decision
   Record for the subset and confirm it does NOT name the operating
   layer as load-bearing.

## Files

- `starter.py` — the scaffold with 9 `# TODO`s and the score report.
- `solution.py` — the fully filled-in reference; scores 17/17.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a
  second, unnamed marketplace.
