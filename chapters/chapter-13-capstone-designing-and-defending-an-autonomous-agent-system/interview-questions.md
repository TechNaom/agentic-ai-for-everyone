# Chapter 13 Interview Questions: Capstone — Designing and Defending an Autonomous Agent System

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. What makes this chapter's problem an L4 Architecture Challenge rather than a bigger L3 Independent project?

**Strong answer:** L3 ("design and implement a reliability-
instrumented, cost-bounded AGENT for a given problem, no scaffold")
is about a single agent, however many mechanisms it needs. L4
("design and defend a complete MULTI-COMPONENT autonomous agent
SYSTEM; business/system problem only") requires the problem to
plausibly need genuine multi-agent coordination — more than one agent
acting, not just one agent with more tools. Thornwick Marketplace
Collective's three components (Buyer Concierge, Maker Fulfillment,
Fraud & Dispute Review) are distinct, specialized, and two of them
race each other on shared state — properties Chapter 12's own L3
project (Driftlight) deliberately did not have.

**Red flag:** Says L4 is "just L3 but bigger" or "with more code,"
without naming the actual difference in kind (multi-component
coordination, not scale).

**Follow-up:** "If Thornwick had only ONE component instead of three,
would it still be a valid L4 submission?"

**What this proves:** Understands that L4's defining property is
coordination need, not size or difficulty alone.

### 2. Name the two SEPARATE facts that justify multi-agent dispatch and peer communication, and say which of Thornwick's own facts trigger each.

**Strong answer:** Chapter 9's dispatch test: distinct, specialized
subtasks that can run independently (Buyer Concierge's conversational
skill vs. Maker Fulfillment's batch logistics vs. Fraud Review's
judgment — three different skills). Chapter 10's coordination test:
concurrent independent actors on shared state (Buyer Concierge and
Maker Fulfillment both read/write the same inventory ledger at the
same time). Thornwick triggers both, which is why it needs BOTH
mechanisms, not just one.

**Red flag:** Treats "multi-agent justified" as a single yes/no fact
rather than two independently-checkable tests, or can't name which
Thornwick fact triggers which test.

**Follow-up:** "If Maker Fulfillment were removed entirely, which of
the two tests would stop firing?"

**What this proves:** Can distinguish dispatch justification from
coordination justification, not just recognize "multi-agent: True."

### 3. Why does this chapter import Chapter 12's five framework functions instead of rewriting them?

**Strong answer:** `characterize_problem`, `select_mechanisms`,
`reliability_cost_budget`, `architecture_smell_check`, and `build_adr`
are already built and tested; rewriting them would risk silent drift
from the original logic and would violate the course's own stated
rule (this chapter's brief explicitly says not to redefine them a
third time). Module 6's own assessment already proved this import
pattern works for a sixth scenario — this chapter reuses the same
pattern for a seventh.

**Red flag:** Thinks reusing the functions is "cheating" or "less
thorough" than writing new ones, missing that reuse of a validated
decision tool is exactly what a real architecture practice does.

**Follow-up:** "What would you have to prove differently if you
rewrote `select_mechanisms` from scratch for this chapter?"

**What this proves:** Understands code reuse as a deliberate
engineering discipline, not corner-cutting.

## Intermediate

### 4. Why is `InventoryLedger.try_claim`'s lock check (`if sku in claimed_this_tick`) placed BEFORE the stock check, not after?

**Strong answer:** Placing the lock check first means a second
concurrent claim is rejected immediately, before it ever re-reads
stock — which is what makes it a genuine claim-CHECK (Chapter 10's
own fix) rather than an unlocked "read stock, then decrement"
sequence that could still let both claims see enough stock and both
succeed. If the stock check ran first, two concurrent claims could
both read "1 unit available" before either one commits its
decrement, and both could then claim the same unit.

**Red flag:** Can't explain why ORDER matters here, or thinks any
read-then-write sequence is equivalent to a lock.

**Follow-up:** "What's the smallest change to `try_claim` that would
silently reintroduce the overselling race?"

**What this proves:** Understands locking order as the actual
mechanism of correctness, not an incidental implementation detail.

### 5. `grounded_reflect` checks for the literal substrings "order_id", "amount", and "resolution" in a free-text explanation. What's a real weakness of this specific implementation, and how would you defend keeping it anyway for this chapter's purpose?

**Strong answer:** A real weakness: a model could satisfy the check
by including the words without actually using them meaningfully
(e.g., "order_id does not matter here"), so this is a necessary-but-
not-sufficient grounding check, not a full correctness proof. The
defense: this chapter's own point (per its disclosed Ollama decision)
is proving the ARCHITECTURE composes, not building a production-grade
grounding verifier — a stronger check is a legitimate extension, not
required to prove this capstone's own claim that reflection is
load-bearing and implementable.

**Red flag:** Either claims the check is fully robust with no
weakness, or dismisses it as "wrong" without acknowledging what it
does correctly prove (that reflection can be grounded in named facts
rather than being a bare retry).

**Follow-up:** "What's one additional check you'd add to make this
harder to satisfy by accident?"

**What this proves:** Can critique their own/the course's
implementation honestly, distinguishing "proves the concept" from
"production-ready."

### 6. A teammate proposes dropping the claim-check and instead just "running Maker Fulfillment's batch after business hours so it never overlaps with Buyer Concierge." Evaluate this.

**Strong answer:** This reduces the RISK of the race but doesn't
eliminate the FACT that justifies the mechanism — Buyer Concierge
could still process a late order during the batch window, a batch
could run long, or a future change could add a second overnight
process. The architecture-smell check doesn't have a rule for "risk
reduced by scheduling," and for good reason: a timing-based mitigation
is fragile and invisible in the ADR, while a claim-check is a
structural guarantee that holds regardless of scheduling.

**Red flag:** Accepts the scheduling fix as equivalent to the
claim-check, or can't articulate why a structural fix is preferred
over a timing-based one.

**Follow-up:** "Would you accept the scheduling fix as a TEMPORARY
mitigation while the claim-check is being built? Why or why not?"

**What this proves:** Distinguishes risk reduction from risk
elimination, and prefers structural guarantees over timing
assumptions.

## Senior

### 7. Thornwick selects all eight of Chapter 1-11's non-foundational mechanisms as load-bearing. How do you defend that this isn't itself an architecture smell (over-engineering), given the smell check doesn't flag it?

**Strong answer:** The smell check tests whether each SELECTED
mechanism is backed by a stated fact, not whether the overall COUNT
of selected mechanisms is high — a high count is only a smell if one
or more of those mechanisms lacks a supporting fact, which the check
already verifies, mechanism by mechanism, and found none. Thornwick's
own problem statement was deliberately built so all nine problem
facts are true; the high count is a consequence of the problem's own
shape, not a default over-addition. The real test for over-
engineering isn't "how many mechanisms," it's "is each one backed by
a fact" — and this chapter's own Section 10 proves that explicitly for
all eight.

**Red flag:** Either agrees the chapter IS over-engineered without
checking whether each mechanism is backed by a fact, or claims a high
mechanism count can never be a smell (missing that it CAN be, when
the facts don't support it — which is exactly what Section 11
demonstrates by dropping guardrails).

**Follow-up:** "If you removed ONE problem fact — say,
`runs_unattended` — which mechanism would the smell check start
flagging, and as which kind of smell?"

**What this proves:** Understands the smell check's actual criterion
(fact-backed, not count-based) and can apply it under a stress case.

### 8. How would you extend this chapter's harness to prove the claim-check holds under MANY concurrent claims, not just the two demonstrated in the lesson?

**Strong answer:** Generalize `simulate_thornwick_run`'s
`maker_fulfillment_claim_race` task to spin up N simulated claims
(not just two) against a stock count smaller than N, in the same
simulated "tick," and assert that the number of successful claims
exactly equals the starting stock count, never more. This proves the
INVARIANT (claims granted never exceed supply) rather than just one
hand-picked two-actor scenario, the same generalization Chapter 7's
own `pass_at_k` represents over a single pass/fail trial.

**Red flag:** Proposes adding more claims without stating what
invariant is actually being checked, or conflates "runs more trials"
with "proves a stronger guarantee."

**Follow-up:** "What would it mean if, under N=10 concurrent claims
against 3 units of stock, you measured exactly 3 successful claims
every single run, but ALSO exactly 3 when stock was 0? What would
that tell you about the test?"

**What this proves:** Can design a stronger, generalized proof for an
existing mechanism, and can reason about whether a test is actually
discriminating correct from incorrect behavior.

### 9. The capstone rubric lives in `assessments/architecture-challenges/`, separate from the project's own `README.md`/`solution.py`. Defend why these are two different documents rather than one.

**Strong answer:** `project/README.md` and `solution.py` are the
DELIVERABLE (the problem statement and the reference answer) — the
same role Chapter 12's L3 project's `README.md`/`solution.py` played.
`assessments/architecture-challenges/RUBRIC.md` is the GRADING
instrument applied to that deliverable, following the exact
separation `assessments/module-assessments/` already uses for every
module (a problem+solution pair plus a separate rubric). Keeping them
in different directories also matches the explicit, audited decision
that `architecture-challenges/` is reserved specifically for this
course's L4 capstone rubric, distinct from Module 6's own
Chapter-12-scoped assessment.

**Red flag:** Can't articulate the deliverable/rubric distinction, or
thinks they should be merged into one file "for simplicity."

**Follow-up:** "What would go wrong if the rubric criteria were
embedded directly inside `solution.py` as comments instead?"

**What this proves:** Understands the deliberate separation between a
reference answer and the instrument used to grade attempts against
it.

## Architect

### 10. Defend, end to end, why Thornwick Marketplace Collective is a legitimate L4 capstone and not merely "Chapter 12's framework applied to a bigger example." Include what would have made it illegitimate.

**Strong answer:** A legitimate L4 capstone has to do three things
Chapter 12's own L3 project did not: (1) characterize as genuinely
multi-agent, for BOTH of Chapter 9's and Chapter 10's own tests at
once, not just one; (2) require the FULL Chapter 1-11 mechanism
inventory simultaneously, proving the decision framework composes
under maximum load, not just on an easier subset; and (3) prove a
genuinely cross-component failure mode (the shared-inventory
overselling race) with a real, executed claim-check — a risk that
simply does not exist in any single-agent system, however many
mechanisms it has. It would have been ILLEGITIMATE if, for example,
Thornwick's three "components" never actually shared state or never
needed to coordinate at all (making it three independent single-agent
systems bolted together under one name with no real multi-agent
property), or if the claim-check were asserted in prose without a
harness that actually races two concurrent claims and shows the
result. The distinguishing test throughout is the same one this
course's own smell check applies at the mechanism level: is each
claimed property backed by something that was actually checked, not
just described plausibly.

**Red flag:** Defends the capstone by appeal to its size or mechanism
count alone, without naming the specific cross-component coordination
property that makes it genuinely different in kind from a scaled-up
single-agent project, or can't state what would have made the same
scenario illegitimate.

**Follow-up:** "Driftlight (Ch.12's L3) also has real stakes and real
code. What is the ONE property Thornwick has that Driftlight
structurally cannot, no matter how many mechanisms Driftlight adds?"

**What this proves:** Can defend an architecture decision's category
(not just its content) with the same rigor Section 9 of the lesson
demands for rejecting an alternative — a named property, not a vibe.
