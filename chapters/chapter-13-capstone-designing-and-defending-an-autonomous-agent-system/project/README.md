# Chapter 13 Project: Thornwick Marketplace Collective — the L4 Architecture Challenge (the capstone)

**This IS Chapter 13's whole deliverable.** Per
`docs/curriculum/CURRICULUM_MAP.md`'s project ladder, L4 reads:
*"Design and defend a complete multi-component autonomous agent
system; business/system problem only."* Unlike Chapters 1-12, which
each had a lesson AND a separate project, this chapter has no such
split — the lesson (`lesson.html`) walks through building exactly
this file, and this file plus the capstone rubric in
`assessments/architecture-challenges/` together are what gets graded.

**There is deliberately no `starter.py`.** L4, like L3 before it, is
"business/system problem only" — no scaffold. `solution.py` is the
reference deliverable: read the problem statement below, then (before
looking at `solution.py`) try your own characterization, mechanism
selection, budget, implementation, and instrumentation. Compare your
own work against `solution.py` afterward and self-grade with
`assessments/architecture-challenges/RUBRIC.md`.

## The problem statement

**Thornwick Marketplace Collective** is a fictional online marketplace
connecting independent makers (small-batch artisans and producers) to
buyers. It has three distinct, specialized components:

1. **Buyer Concierge** — a conversational agent handling product
   questions, order placement, and return requests. A buyer who states
   an allergy or preference once (e.g., "no peanuts") must have that
   fact correctly inform **every later, separate order** — weeks or
   months afterward, not just the current conversation.
2. **Maker Fulfillment** — processes maker-side packing confirmations
   and inventory decrements, batched **overnight**, with no staff
   watching.
3. **Fraud & Dispute Review** — evaluates buyer chargeback disputes.
   Refunds above a dollar threshold require explicit human approval.
   The written explanation sent back to the maker and buyer, justifying
   a dispute's resolution, is free text that can't be checked by a
   simple rule — it has to actually ground itself in the real facts of
   the case (the order id, the amount, the resolution).

**The coordination problem that makes this genuinely multi-component,
not three separate single-agent systems bolted together:** Buyer
Concierge and Maker Fulfillment both read and write the **same shared
inventory ledger**. A buyer completing a checkout (Buyer Concierge) and
the overnight fulfillment batch committing a maker's own stock count
(Maker Fulfillment) can both try to claim the **same sku's last unit at
the same time**. An unlocked "check stock, then decrement" sequence can
oversell that unit to both sides — this is Chapter 10's own
coordination problem (concurrent independent actors on shared state),
not Chapter 9's dispatch problem (just routing distinct work to
distinct specialists) alone.

## Why this is a genuinely new, multi-component problem

Every one of Chapter 12's own worked examples (Copperfield, Lantern
Hill, Vantage Peak, Driftlight, Mirelake, Alderwood) needed at most
five of Chapters 1-11's eight non-foundational mechanisms, and none of
them needed **both** multi-agent dispatch (Ch9) **and** peer
communication (Ch10) **together with** memory (Ch4), reflection (Ch5),
guardrails (Ch6), reliability measurement (Ch7), cost control (Ch8),
**and** the operating layer (Ch11) all at once. Thornwick is
deliberately built so that **all eight** are load-bearing simultaneously
— exercising the full Chapter 1-11 mechanism inventory's range in one
system, which is exactly what an L4 Architecture Challenge is for.

## What `solution.py` actually does, in order

1. **Characterizes** the problem (`characterize_problem`, imported
   unchanged from Chapter 12's own `project/solution.py`) — reaches
   **multi-agent**, because the three components have distinct,
   specialized subtasks that can proceed independently.
2. **Selects mechanisms** (`select_mechanisms`) — confirms **all eight**
   of memory, reflection, guardrails, reliability measurement, cost
   control, multi-agent dispatch, peer communication, and the operating
   layer are load-bearing, each traceable to a specific Thornwick fact.
3. **States a reliability/cost budget** (`reliability_cost_budget`) —
   the tight, irreversible-action tier (95% minimum task-success rate,
   8-cent maximum cost per run).
4. **Implements** the selected mechanisms as real code:
   - `MemoryStore` — a buyer's allergy preference, proven to persist
     across two genuinely separate instantiations.
   - `InventoryLedger.try_claim` — a locked claim-check: the second of
     two concurrent claims on the same sku's last unit is rejected,
     never double-committed (Chapter 10's own coordination fix).
   - `apply_refund` — a fail-closed guardrail: refunds above $40
     require explicit `human_approved=True`.
   - `idempotency_key` + `commit_once` — an exactly-once commit layer
     for the overnight fulfillment side effect.
   - `grounded_reflect` — checks a dispute-resolution explanation
     actually names the order id, amount, and resolution, not just
     that text exists ("retry is not reflection," applied to free text).
5. **Instruments** the implementation with a deterministic reliability/
   cost harness (`run_thornwick_harness`, `cost_per_success`,
   `is_within_budget` — reused in logic from Chapters 7-8) across three
   task types (one per component), and **proves** the stated budget is
   actually met with real measured numbers.
6. **Assembles the Architecture Decision Record** (`build_adr`,
   imported unchanged) for the shipped design, naming all eight
   load-bearing mechanisms and three named-and-rejected alternatives.

## Why no live Ollama call

This capstone's own skill, like Chapter 12's L3 project before it, is
architecture judgment and proof-of-design against a written problem
statement — not a model's live behavior. A live call would illustrate
nothing this reference implementation doesn't already prove
deterministically, and would make grading depend on a running Ollama
server for no benefit. See `lesson.html` Section 2 and
`quality-audits/chapter-13-audit.md` for the full reasoning.

## How to run it

```bash
python3 solution.py
```

This prints the assembled ADR, then a 14-point self-check report, then
the harness's real measured numbers.

## How to check your own independent attempt

1. Write your own characterization, mechanism selection, budget,
   implementation, and harness for Thornwick **before** reading
   `solution.py`.
2. Run your own code and confirm your harness actually meets the
   budget you stated.
3. Compare your design against `solution.py`, not to match it
   line-for-line, but to check whether you reached the same
   load-bearing-mechanism verdicts for the same reasons — especially
   whether you caught BOTH the dispatch justification (Ch9) AND the
   shared-state coordination justification (Ch10), since a design that
   only catches one of the two is incomplete.
4. Self-grade against `assessments/architecture-challenges/RUBRIC.md`.

## Files

- `solution.py` — the reference deliverable; no scaffold, no starter,
  per L4's own "business/system problem only" definition. Scores
  14/14.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a
  second, unnamed marketplace.
