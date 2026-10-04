# Chapter 12 Interview Questions: Designing Agent Architectures

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. What does this chapter teach that Chapters 1-11 did not?

**Strong answer:** Chapters 1-11 each taught how to BUILD one
mechanism (the loop, planning, tools, memory, reflection, guardrails,
reliability measurement, cost control, dispatch, peer communication,
operating). This chapter teaches the decision layer above all of
them: given a new problem, which of those eleven mechanisms are
actually load-bearing, and how to defend that choice in writing. It
re-teaches none of the mechanics.

**Red flag:** Describes this chapter as "a review of Chapters 1-11,"
or can't distinguish "building a mechanism" from "deciding whether a
problem needs it."

**Follow-up:** "Name one mechanism from Chapters 1-11 that a GIVEN
problem might NOT need, and the fact that would tell you so."

**What this proves:** Understands this chapter's role as a decision
framework, not a recap.

### 2. What two facts, either one of which is sufficient, justify a multi-agent architecture over a single agent?

**Strong answer:** (1) The problem has distinct, specialized subtasks
that can run independently (Chapter 9's dispatch shape), or (2) the
problem requires multiple independent actors to act concurrently on
shared state (Chapter 10's coordination shape). Neither is "the
problem sounds complicated."

**Red flag:** Justifies multi-agent from topic complexity, team size,
or "it felt like it needed more than one agent," without naming either
concrete fact.

**Follow-up:** "A single agent with four tools and a long system
prompt -- does that alone justify splitting it into four agents?"

**What this proves:** Can name the actual test, not a vibe-based
justification for architecture complexity.

### 3. Why did Copperfield Municipal Utilities' outage/billing problem characterize as single-agent, not multi-agent?

**Strong answer:** Both request types (outage reports, billing
disputes) read and write the SAME customer and grid state, and no
concurrent independent actor is required -- one customer interacts
with the system at a time. Splitting it into two agents would add
Chapter 9's dispatch/attribution overhead and risk the exact
duplicate-work race Chapter 10's claim-check exists to prevent, for no
benefit.

**Red flag:** Says "because it's simple," without naming the two
specific facts (shared state, no concurrent actors) that make it so.

**Follow-up:** "What single new fact about Copperfield's business
would flip this verdict to multi-agent?"

**What this proves:** Can trace a characterization verdict back to
the specific facts that produced it.

## Intermediate

### 4. A problem has a $5,000 irreversible wire transfer action. Which Chapter 1-11 mechanisms become load-bearing because of that one fact, and why?

**Strong answer:** Guardrails (Chapter 6) -- specifically a
human-approval checkpoint before the transfer, the same pattern as
LedgerBot. Reliability measurement (Chapter 7) becomes load-bearing
because a wrong transfer is exactly the costly-failure case Chapter
7's `pass_at_k` exists to catch. Cost control (Chapter 8) is load-
bearing if the system runs at volume. Memory, reflection, and
multi-agent dispatch are NOT automatically triggered by this one fact
alone.

**Red flag:** Adds every mechanism "to be safe" without tracing each
one to a specific fact, or misses the guardrail entirely.

**Follow-up:** "If the SAME action were reversible within 24 hours,
which of your answers would change?"

**What this proves:** Applies mechanism-selection reasoning
correctly under a single strong signal, without over-adding.

### 5. What is an "architecture smell," and name one over-engineering smell and one under-engineering smell from this chapter.

**Strong answer:** A smell is a selected-mechanism choice that isn't
backed by a stated problem fact, caught by comparing the selection
against the facts automatically. Over-engineering example:
multi-agent dispatch chosen when no distinct, independently-runnable
subtasks exist (Chapter 9's overhead bought for nothing).
Under-engineering example: an irreversible/costly action with no
guardrail (Chapter 6's fail-safe-default lesson violated directly).

**Red flag:** Can only name one direction (e.g., only over-
engineering), or describes a smell as a style preference rather than a
fact-selection mismatch.

**Follow-up:** "Why does the smell check need the PROBLEM facts and
the SELECTED mechanisms both, rather than just one or the other?"

**What this proves:** Understands a smell check as a cross-check
between two independent inputs, not a standalone rule.

### 6. Why does a reliability/cost budget get stated as numbers (a minimum success rate, a cost ceiling) rather than "we'll measure it and see"?

**Strong answer:** A number is checkable against Chapter 7's
`pass_at_k`/`run_harness` and Chapter 8's `is_within_budget`/
`cost_per_success` -- it turns a budget into a pass/fail gate a real
harness run can confirm or violate. "We'll measure it and see" has no
gate; it can't tell you after the fact whether the system actually met
its own design intent.

**Red flag:** Treats the budget as documentation only, with no
connection to an actual harness run that could fail it.

**Follow-up:** "Chapter 8's `cost_per_success` for a task came back at
$0.11 against a stated $0.08 ceiling. What does the architect do now?"

**What this proves:** Connects a stated budget to a real,
re-runnable check, not just a planning artifact.

## Senior

### 7. A junior engineer proposes a 3-agent supervisor/worker system for a problem where one agent with five tools would work. How do you push back, concretely?

**Strong answer:** Ask them to state the specific fact from Chapter
9's own test (distinct, specialized subtasks that run independently)
or Chapter 10's test (concurrent independent actors on shared state)
that justifies the split. If they can't name one, run the smell check:
multi-agent chosen with no supporting fact is the exact over-
engineering flag this chapter's `architecture_smell_check` raises.
Point out the real cost: Chapter 9's dispatch/attribution overhead and
Chapter 10's coordination-failure surface (miscommunication, duplicated
work, deadlock) are all added for zero benefit if the facts don't hold.

**Red flag:** Pushes back on "complexity" or "cost" alone without
naming the specific missing fact, or can't explain what risk the
unjustified multi-agent split actually introduces.

**Follow-up:** "What would change your mind -- what NEW fact about
this problem would make the 3-agent design the right call?"

**What this proves:** Can conduct a real design-review pushback using
this chapter's own named tests, not just intuition.

### 8. Chapter 5 taught "retry is not reflection." How does that same distinction show up as an architecture-level smell in this chapter?

**Strong answer:** Reflection (Chapter 5) is only load-bearing when a
problem has a hard-to-verify free-text output -- something that can't
be checked by a grounded, deterministic rule. If reflection is chosen
for a problem whose outputs are all checkable facts (a confirmed
ticket, an applied credit), it's the architecture-level version of the
same mistake: an extra model call that looks like diligence but adds
no real correction capability, exactly as "retry is not reflection"
warned at the mechanism level in Chapter 5.

**Red flag:** Treats reflection as always "safer to include," or
can't connect the architecture-level smell back to Chapter 5's own
specific claim.

**Follow-up:** "A credit-dispute agent's final output is a one-
paragraph explanation to the customer. Does that reopen the case for
reflection? What fact decides it?"

**What this proves:** Carries a mechanism-level lesson up to the
decision layer and applies it correctly to a new case.

### 9. Walk through what happens if an architect skips Section 1 (characterization) and goes straight to mechanism selection.

**Strong answer:** Mechanism selection for dispatch, peer
communication, and the operating layer all depend on whether the
problem is single- or multi-agent -- skipping characterization means
guessing at that answer implicitly, usually by habit or by copying the
last project's shape. The smell check can still catch the resulting
mismatch (e.g., multi-agent chosen with no supporting fact), but by
then the design has already been built around the wrong assumption,
which is far more expensive to unwind than catching it at
characterization, before any mechanism was chosen.

**Red flag:** Says skipping characterization "doesn't matter much" or
can't explain why catching the error later costs more.

**Follow-up:** "What's the cheapest point in this four-question
framework to catch a wrong assumption, and why?"

**What this proves:** Understands why the framework's ORDER, not just
its content, matters.

## Architect

### 10. This course deferred its L3 Independent project across Chapters 8, 9, 10, and 11 -- five total sessions. Chapter 12's session decided to ship it as this chapter's own project. Defend that decision, including what would have made deferring it a SIXTH time the wrong call versus the right one.

**Strong answer:** L3's definition ("design and implement a
reliability-instrumented, cost-bounded agent for a given problem, no
scaffold") is, almost word for word, what an architect does when
applying THIS chapter's own framework to a brand-new problem:
characterize it, select mechanisms, state a budget, and then actually
build and instrument a small agent that meets that budget using
Chapter 7 and 8's real harnesses -- with no starter scaffold, since
the whole point of "independent" is that the learner is given a
problem, not a fill-in-the-blank file. Deferring a sixth time would
have been the WRONG call once a legitimate, non-forced fit existed;
deferring is only right when no honest fit exists and the reason is
specific (e.g., if Chapter 12's assessment had been purely a prose
document with no implementable system at all). The decision record
and its reasoning are stated explicitly in
`quality-audits/chapter-12-audit.md` precisely so it can be checked,
not taken on faith.

**Red flag:** Treats "we finally built it" as sufficient justification
on its own, without being able to state what would have made deferral
the CORRECT call in a different chapter's circumstances, or can't
name the specific definitional fit (implement, not just design) that
made this chapter's project a legitimate L3, not a relabeling.

**Follow-up:** "If Chapter 12's own assessment had turned out to be
pure prose with no working system at all, what should this session
have done instead, per its own stated decision tree?"

**What this proves:** Can defend a one-time process decision with the
same rigor this chapter asks of an architecture decision -- stated
facts, a named alternative, and why the alternative was rejected.
