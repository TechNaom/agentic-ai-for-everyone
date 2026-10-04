# Chapter 10 Interview Questions: Multi-Agent Coordination and Communication

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. How is peer-to-peer agent communication architecturally different from Chapter 9's supervisor/worker dispatch?

**Strong answer:** In supervisor/worker, one agent (the supervisor)
decides which sub-tasks exist and routes each to a worker -- every
interaction is mediated by that one decision-maker, and workers never
talk to each other. In peer-to-peer communication, two or more agents
of EQUAL standing exchange messages DIRECTLY, across multiple turns,
with no third agent deciding who talks to whom. This chapter's
DockScout and YardScout are genuine peers: neither dispatches to the
other.

**Red flag:** Describes peer-to-peer as "dispatch with extra steps" or
treats it as the same pattern just relabeled.

**Follow-up:** "If DockScout and YardScout both reported to a third
agent that made the final call, would that still be peer-to-peer
communication? Why or why not?"

**What this proves:** Understands that the absence of a mediating
decision-maker, not just the presence of multiple messages, is what
defines peer-to-peer coordination.

### 2. This chapter's own live test showed YardScout emit a message with keys like `" recipient "` (padded with whitespace). Why is normalizing that safe, but guessing that `"shipment"` means `"shipment_id"` is NOT safe?

**Strong answer:** Whitespace stripping can never change WHICH field a
value belongs to -- `" recipient "` and `"recipient"` are obviously the
same field under any reasonable interpretation. Guessing that a
differently-NAMED field maps to a known one is a genuine guess about
the sender's intent; if the guess is wrong, the receiving agent acts on
the wrong value with no indication anything went wrong. The parser
should normalize the first case and fail closed (return `ok: False`) on
the second, never treat them as the same kind of problem.

**Red flag:** Treats all message-shape mismatches as equally safe to
"fix" automatically, or proposes keyword-mapping unknown fields to
known ones.

**Follow-up:** "What's a concrete real-world case where guessing a
field mapping could cause real harm, not just a wrong answer?"

**What this proves:** Distinguishes genuinely safe normalization from
unsafe guessing, rather than treating "handle the malformed input
somehow" as one undifferentiated task.

### 3. Why does this chapter's claim-check need to happen inside ONE lock, covering both the check and the write?

**Strong answer:** If "check whether already claimed" and "add to
claims" were two separate locked operations, two agents could both
pass the check (neither sees the claim yet) before either one performs
the write -- a classic check-then-act race condition. Locking both
operations together as one atomic unit is what actually prevents two
peers from both believing they're the first to claim something.

**Red flag:** Proposes locking only the write, or only the check, not
both together as one atomic unit.

**Follow-up:** "What's the smallest possible example of two threads
racing through a check-then-act gap, even with each half separately
locked?"

**What this proves:** Understands atomicity requirements for a
check-and-claim pattern, not just "use a lock somewhere."

## Intermediate

### 4. Why is "duplicated work" in this chapter a genuinely different failure from Chapter 9's "redundant dispatch"?

**Strong answer:** Chapter 9's redundant dispatch was ONE supervisor
re-dispatching the SAME sub-task to the SAME worker, typically via a
careless retry -- a single decision-maker repeating itself. This
chapter's duplicated work involves TWO INDEPENDENT peer agents, each
reasoning correctly about its own half of the problem, with no shared
coordination mechanism forcing either one to check whether the other
had already acted. This chapter's own live test captured exactly this:
DockScout and YardScout each independently claimed the same shipment,
and neither one did anything individually wrong.

**Red flag:** Treats both as "the same kind of duplicate work problem"
requiring the same fix (idempotency keying alone), missing that the
peer case additionally needs a SHARED check that didn't exist before
either agent acted.

**Follow-up:** "Would Chapter 9's idempotent-dispatch fix, by itself,
have prevented this chapter's duplicated claim? Why or why not?"

**What this proves:** Distinguishes a single decision-maker's repeated
mistake from two independent agents' uncoordinated convergence, and
recognizes they need different fixes.

### 5. This chapter's own live attempt to reproduce a deadlock did NOT succeed -- both agents sent a message despite being told to "never go first." What does that result actually tell you, and why was constructing deadlock deterministically still the right next step?

**Strong answer:** It tells you a small local model does not reliably
follow a behavioral constraint stated only in a system prompt --
that's a real, useful finding, but it's a DIFFERENT finding from "no
deadlock risk exists." Deadlock is a structural property of the
coordination logic (two agents each conditioned on the other's prior
message, with neither one ever speaking first), not a property of
whether a particular model happens to obey an instruction on a given
run. Constructing it deterministically demonstrates the real
structural risk reliably, the same way Chapter 1's deterministic guard
demonstration didn't depend on the model actually running away.

**Red flag:** Concludes "deadlock isn't a real risk in this system"
from one non-reproducing live test, or claims the live test "proves"
deadlock can't happen.

**Follow-up:** "What change to the SYSTEM (not the prompt) would make
this chapter's own live deadlock test more likely to reproduce the
condition reliably?"

**What this proves:** Separates "this specific live run didn't show
it" from "the structural risk doesn't exist," and knows which kind of
evidence actually settles the question.

### 6. Why can't a simple majority vote reliably break a tie between exactly two peer agents?

**Strong answer:** With exactly two voters, any disagreement is
automatically a 1-1 tie -- there is no mathematical way for a 2-voter
majority vote to produce a winner when the two voters disagree with
each other. A real fix needs either a third, independent voice (an
observer agent) or a rule that doesn't depend on voting at all (a
pre-agreed, independently computable tie-breaker like sorting the
agent roster).

**Red flag:** Proposes "just take a vote" as sufficient for resolving
disagreement between exactly two agents, without noting the structural
tie problem.

**Follow-up:** "If you add a third agent purely to break ties, what
happens if THAT agent is unavailable when a tie occurs?"

**What this proves:** Reasons correctly about the mathematics of
2-party voting, not just "more coordination mechanisms generally
help."

## Senior

### 7. Design a message-validation layer for a peer-to-peer agent system where messages occasionally arrive with malformed field names (per this chapter's own real, observed result). What's the failure mode of validating too permissively, and too strictly?

**Strong answer:** Too permissive (guessing unknown field names map to
known ones) risks silently acting on the WRONG value when a guess is
wrong -- no error, no signal, just a bad outcome, the same risk
Section 7's "unrecoverable miscommunication" example demonstrated. Too
strict (rejecting any message that doesn't match the schema
byte-for-byte) means a harmless, obviously-safe variation like
whitespace padding causes a working exchange to fail entirely, wasting
a retry on something that didn't need one. The correct design
normalizes ONLY transformations that cannot change which field a value
belongs to (whitespace, case on keys if the schema is case-insensitive
by design) and fails closed, with a specific diagnostic reason, on
everything else.

**Red flag:** Proposes either extreme (accept anything that's
"close enough," or reject anything not byte-identical to the schema)
without naming the specific risk each extreme carries.

**Follow-up:** "How would you decide, for a NEW kind of malformation
you haven't seen yet, whether it's safe to normalize or should fail
closed?"

**What this proves:** Can draw the line between safe normalization and
unsafe guessing with a principled rule, not just a growing list of
special cases.

### 8. Your team ships a peer-to-peer agent system where a post-incident review says "the two agents miscommunicated." What's missing from that sentence, and how does `which_agent_caused_miscommunication` fix it?

**Strong answer:** WHICH agent's message was the one a receiver
misread, and at what point in the exchange. "The two agents
miscommunicated" is symmetric and uninformative -- it doesn't tell you
whether to audit the SENDER's message-construction logic or the
RECEIVER's message-parsing logic, and those are different fixes.
`which_agent_caused_miscommunication` extends Chapter 9's
`which_agent_responsible` from "which agent's dispatch step failed" to
"which agent's MESSAGE was misread," walking the exchange in order and
naming the first sender whose message caused a downstream problem.

**Red flag:** Treats "miscommunication happened somewhere in the
exchange" as sufficient incident detail, with no mention of
attributing it to a specific message or sender.

**Follow-up:** "Extend this function to report the RECEIVER's specific
misinterpretation, not just which sender's message was involved --
what additional data would you need to capture during the exchange
itself?"

**What this proves:** Understands that attribution must be granular
enough to point at a specific fixable cause, not just confirm that a
failure happened somewhere in a multi-turn exchange.

## Architect

### 9. A stakeholder proposes solving this chapter's duplicated-work problem by having each agent "just check with the other agent before claiming anything." Why doesn't that fully solve the problem on its own, and what does?

**Strong answer:** "Check with the other agent first" reduces the
WINDOW for a race but doesn't eliminate it -- if both agents check at
nearly the same instant, both can see "not yet claimed" before either
one commits, the exact race this chapter's lock prevents. A
peer-to-peer CHECK is still two separate operations (ask, then act)
unless the check-and-claim is atomic against a SHARED piece of state
both agents access through the same serialization point (a lock, a
database's unique constraint, a distributed lock service) -- asking a
peer a question and then acting on the answer is not the same
guarantee as an atomic compare-and-set.

**Red flag:** Accepts "they'll just ask each other first" as a
complete fix without identifying the remaining race window.

**Follow-up:** "In a system with 5 peer agents instead of 2, does
'ask everyone first' get worse, better, or structurally unchanged as a
race-avoidance strategy?"

**What this proves:** Distinguishes a request/response exchange
(which still has a race window) from a truly atomic operation, and can
articulate exactly why a seemingly reasonable fix is insufficient.

### 10. Design the attribution and tie-breaking architecture for a system with FIVE peer agents (not two) that occasionally disagree about who should handle a task. What changes from this chapter's 2-agent design, and what stays the same?

**Strong answer:** With 5 agents, majority voting becomes genuinely
useful (an odd number means ties are far less likely, though still
possible if agents abstain or split evenly across sub-groups), so
`resolve_conflicting_claims`'s voting mechanism becomes the PRIMARY
tie-breaker rather than a secondary one -- but the pre-agreed,
independently-computable fallback (sorted roster, lowest ID) still
needs to exist for the residual tie cases voting alone can't resolve.
Message-level attribution (`which_agent_caused_miscommunication`)
scales unchanged in PRINCIPLE but needs a genuinely O(n) or better
trace structure, since the exchange is no longer a simple 2-party
back-and-forth -- a real design has to decide whether every agent sees
every message (broadcast, which duplicates Chapter 9's blackboard
concern about shared-state contention) or only the messages addressed
to it (point-to-point, which risks a message never reaching an agent
that needed to see it for correct attribution).

**Red flag:** Assumes the 2-agent design "just works" unchanged at 5
agents, with no mention of the broadcast-vs-point-to-point tradeoff or
the residual-tie problem voting alone doesn't solve.

**Follow-up:** "At what agent count does a shared message bus's own
lock contention become the bottleneck, and what's the first
architectural change you'd make to address it?"

**What this proves:** Reasons correctly about how coordination
mechanisms designed for exactly two peers do and don't generalize to a
larger peer group, rather than assuming linear scaling.
