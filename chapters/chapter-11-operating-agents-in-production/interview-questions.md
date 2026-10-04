# Chapter 11 Interview Questions: Operating Agents in Production

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. What does "operating" a multi-agent system add on top of Chapters 9-10's coordination mechanisms, and what does it deliberately NOT change?

**Strong answer:** Operating adds mechanisms AROUND the agents' own
decisions -- retries, timeouts, structured logging, and run summaries
-- so the same correct system can run unattended, many times, and
still be trusted and debugged afterward. It does not change what any
agent decides, how dispatch is routed (Chapter 9), or how peer messages
are validated and claimed (Chapter 10). Those mechanisms are reused
unchanged; this chapter wraps them.

**Red flag:** Describes "production-readiness" as rewriting the
agents' own logic, or can't name a single mechanism that's reused
unchanged from Chapters 9-10.

**Follow-up:** "If you had to remove ONE of retries, timeouts,
logging, or run summaries to ship faster, which would you keep last,
and why?"

**What this proves:** Understands operating concerns as an additive
layer, not a rewrite of coordination logic.

### 2. This chapter's own live test ran the identical request twice and got two different argument shapes back from the model (one call included an extra `"vehicle"` field). Why does that matter for retries specifically?

**Strong answer:** If a retry system treats two calls as "the same
attempt" only when their raw arguments match exactly, this real result
shows that comparison can fail even when the underlying action is
genuinely identical -- the system would then see two DIFFERENT actions
and risk committing the same side effect twice. The fix is to key
"sameness" on the fields that actually define the side effect (agent,
shipment, action), not on the full argument payload a model happens to
produce on a given call.

**Red flag:** Assumes a model will always produce byte-identical output
for "the same" request, or proposes string-equality on the full
argument JSON as a deduplication strategy.

**Follow-up:** "What's a real-world side effect where a double-commit
caused by this exact mistake would be expensive, not just annoying?"

**What this proves:** Connects a real observed quirk to a concrete
engineering consequence, rather than treating idempotency as an
abstract best practice.

### 3. Why are three independent timeout layers (per-call, per-agent, per-exchange) each necessary, rather than one timeout value applied everywhere?

**Strong answer:** Each layer catches a failure the others cannot see.
A per-call timeout catches one hung network request but says nothing
about an agent's own loop running long across many individually-fast
calls. A per-agent timeout catches that, but says nothing about
whether a multi-message exchange between two agents is converging at
all (Chapter 10's deadlock). A single shared timeout value conflates
all three failure shapes and will either be too tight for the slowest
legitimate layer or too loose to catch the fastest real failure.

**Red flag:** Treats "add a timeout" as a single, undifferentiated
fix, or can't name a concrete failure each layer catches that the
others miss.

**Follow-up:** "If a per-call timeout keeps firing but the per-exchange
timeout never does, what does that combination tell you about where
the problem actually is?"

**What this proves:** Distinguishes the three layers by the specific
failure each is designed to catch, not just by name.

## Intermediate

### 4. This chapter's own live timeout test configured a 0.5-second client timeout but the real exception fired at 3.07 seconds. How should a production system account for that gap?

**Strong answer:** A configured timeout value is a floor the HTTP
stack enforces approximately, not an exact wall-clock guarantee --
connection setup, internal library retries, and OS-level buffering all
add real overhead on top of the configured value. A production system
should budget headroom above every configured timeout (this course's
own 450-second live-call budget is exactly this kind of headroom) and
never assume a timeout fires at precisely its configured value.

**Red flag:** Assumes a configured timeout is exact, or designs
downstream logic (e.g., a retry schedule) that depends on a timeout
firing at precisely its stated value.

**Follow-up:** "How would you detect, from logs alone, that a
timeout's real firing delay had grown significantly larger than its
configured value over many runs?"

**What this proves:** Understands the practical gap between a
configured budget and the real clock, and designs around it rather
than assuming precision.

### 5. Why must a run summary be computed by re-parsing a structured log, rather than from counters incremented in memory during the run?

**Strong answer:** An in-memory counter is gone the instant the
process crashes -- if the crash happens one event before the summary
would have been computed, the operator learns nothing. A structured
log is flushed to disk one line at a time as events happen, so a
summary computed by re-parsing it afterward is reproducible even if
the process that produced the log crashed immediately after the last
line was written. This is the same "survive the crash" property
Chapter 4's persisted memory store needed across sessions, now applied
to run telemetry instead of conversational facts.

**Red flag:** Proposes keeping richer in-memory state as the primary
fix for crash-survivability, rather than deriving state from something
already durably written.

**Follow-up:** "If the log file itself could be corrupted by a crash
mid-write, what would you change about how each line is written?"

**What this proves:** Connects crash-survivability to where state is
durably stored, not to how carefully in-memory state is tracked.

### 6. How does `which_agent_caused_miscommunication` (Chapter 10) stay answerable in production, after the process that ran the exchange has already exited?

**Strong answer:** The function itself doesn't change -- it still
walks a `(sender, type, interpreted_ok)` sequence. What changes is
where that sequence comes from: instead of an in-memory list built
during the live run, it's reconstructed by re-parsing the structured
log's own JSON lines after the fact. As long as the log records
sender, message type, and whether it was interpreted successfully,
Chapter 10's function can be called on it unchanged, days later.

**Red flag:** Proposes rewriting `which_agent_caused_miscommunication`
for "production use," rather than reusing it unchanged against a
reconstructed trace.

**Follow-up:** "What's the minimum set of fields the log must capture
per event for this reconstruction to be possible at all?"

**What this proves:** Recognizes that making a function
production-answerable is about log design, not about rewriting the
function.

## Senior

### 7. Design the idempotency and retry layer for a payment-confirmation agent action that must NEVER be charged twice, using this chapter's own real argument-drift result as your design constraint.

**Strong answer:** Build the idempotency key from the fields that
define the charge (customer id, invoice id, amount), not from the full
tool-call argument payload -- this chapter's own real result (the same
"confirm the claim" request producing two different argument shapes
across two calls) shows that raw-argument equality would NOT reliably
catch a retry as a duplicate. Wrap the actual charge call in
`commit_once` keyed this way, with a bounded, backed-off retry wrapper
around the CALL layer only -- never around the commit layer, where a
"retry" of an already-committed charge must replay the first result,
not re-invoke the charge function. Every attempt, success, and replay
should be logged with the same correlation id for the audit trail a
real payment system requires.

**Red flag:** Retries the raw payment call directly without an
idempotency boundary, or conflates "retry the network call" with
"retry the side effect" as the same operation.

**Follow-up:** "A duplicate charge actually lands despite this design.
Walk through exactly which component you'd suspect first, and why."

**What this proves:** Can design a correctly layered retry/idempotency
boundary for a side effect where a mistake has real financial
consequences, not just a wrong answer.

### 8. A post-incident review says "the system was slow and sometimes failed overnight." What's missing from that sentence, and how would this chapter's structured logging and run summary turn it into something actionable?

**Strong answer:** "Slow" and "sometimes failed" are not attributable
to any specific call, agent, timeout layer, or run -- they describe a
vague impression, not a diagnosis. With structured logging, each
run's correlation id ties every dispatch, retry, timeout, and commit
together; `run_summary_from_log` turns that into concrete numbers
(retries used, timeouts hit at which layer, deadlocks broken,
duplicates skipped) per run, and `which_agent_responsible`/
`which_agent_caused_miscommunication` can attribute a specific bad run
to a specific agent or message. The incident review should cite a
correlation id and the summary it produced, not an adjective.

**Red flag:** Accepts "slow and sometimes failed" as sufficient
incident detail, or proposes adding more logging without naming what
question each new field would answer.

**Follow-up:** "Which single summary field would you check FIRST to
distinguish 'retries are masking a flaky dependency' from 'the exchange
itself is deadlocking'?"

**What this proves:** Can translate a vague operational complaint into
the specific structured-log fields and functions that would make it
diagnosable.

## Architect

### 9. A stakeholder asks why this course doesn't just adopt an existing observability/APM framework instead of this chapter's from-scratch structured log and run summary. Defend the from-scratch choice and name its real limits.

**Strong answer:** This course's own no-framework discipline (stated
since Chapter 1) is deliberate: the goal is to understand WHAT an
agent system needs to be operable -- idempotent side effects, layered
timeouts, event-level attribution, crash-survivable summaries -- before
adopting any tool that automates it. A real production system should
very likely adopt a mature observability stack; this chapter explicitly
defers that deeper methodology to `llm-evaluation-for-everyone`
(evaluation methodology) and `ai-engineering-for-everyone` (production
LLM engineering infrastructure) by name. The real limit of this
chapter's own minimal version: no alerting, no retention policy, no
distributed trace correlation across process boundaries beyond a
shared id string, and no dashboarding -- all deliberately out of scope
here.

**Red flag:** Claims this chapter's structured log is production-
complete on its own, or can't name what a real observability stack
would add beyond it.

**Follow-up:** "If you had to add exactly ONE capability from a real
observability stack to this chapter's design before trusting it in
production, what would it be and why that one first?"

**What this proves:** Can defend a deliberately minimal, from-scratch
design choice while being honest and specific about where it stops
being sufficient.

### 10. Design the operating layer for a FIVE-agent production system (not two) with a supervisor and four peer-communicating workers, reusing as much of this chapter's two-agent design as possible. What changes, and what stays the same?

**Strong answer:** What stays the same: the idempotency-key pattern
(keyed on the fields defining each side effect), the three-timeout-
layer structure (per-call and per-agent scale to any agent count
unchanged; per-exchange needs to track convergence across however many
peers are exchanging messages, not just two), the structured-log event
shape (one JSON line, shared correlation id), and run-summary
computation from the log. What changes: the tie-breaker (Chapter 10's
alphabetically-first rule still works with five names, but the
deadlock condition itself is harder to define -- "all four workers
waiting on each other" is a cycle-detection problem, not a two-party
timeout), and attribution (`which_agent_responsible`/
`which_agent_caused_miscommunication` already return a single agent
name and need no change, but the SUPERVISOR's own per-agent budget
tracking, Chapter 9's mechanism, must now aggregate across four
workers' logs, not one).

**Red flag:** Assumes the two-agent deadlock/tie-breaker logic
generalizes to five agents with no change, or can't identify cycle
detection as the harder problem at scale.

**Follow-up:** "Sketch, at a high level, how you'd detect a
three-agent circular wait (A waiting on B, B on C, C on A) using only
this chapter's per-exchange timeout and structured log, without adding
a new mechanism."

**What this proves:** Can correctly identify which parts of a
two-agent operating design generalize directly and which require new
mechanisms at higher agent counts.
