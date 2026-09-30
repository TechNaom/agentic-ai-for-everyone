# Chapter 9 Interview Questions: Multi-Agent Orchestration Patterns

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. What genuinely new work does a supervisor do that a single-agent loop (Chapters 1-8) never had to do?

**Strong answer:** Three things that simply don't exist for one loop:
decomposition (breaking a goal into sub-tasks), routing (choosing
which worker handles each sub-task), and aggregation (combining worker
results into one outcome). Each individual worker underneath is still
an ordinary Chapter 1-8 loop -- it has its own tools, its own budget,
its own measurement. The supervisor's own tool surface is
dispatch-only; it never calls a flight, hotel, or activity API
directly.

**Red flag:** Describes a supervisor as "just a bigger agent with more
tools," missing that its own tool surface is dispatch, not
domain-specific action.

**Follow-up:** "If a supervisor's dispatch tool schema let it call
`search_flights` directly instead of only `dispatch_to_worker`, what
would that actually break about the pattern?"

**What this proves:** Understands the supervisor/worker split as an
architectural boundary, not just "more tools in one agent."

### 2. This chapter's own live test showed a supervisor call return a fully-formed dispatch plan as plain text instead of a real tool call. Why is that dangerous if unchecked?

**Strong answer:** `msg.tool_calls` came back empty even though the
model clearly intended to make calls -- it wrote the plan as
JSON-shaped text content instead. A supervisor that assumes "no tool
call means nothing to dispatch" would silently DROP the entire plan
with no error, no exception, and no log entry showing anything went
wrong. The fix is to check `tool_calls is None` explicitly and retry
the same sub-task, never assume absence of a tool call means absence
of intent.

**Red flag:** Assumes an empty `tool_calls` field always means "the
model decided nothing needs to happen," rather than a possible
protocol-adherence failure.

**Follow-up:** "How would you distinguish, in your logging, between a
model that genuinely decided no dispatch was needed and one that
intended to dispatch but failed to emit a real tool call?"

**What this proves:** Recognizes that an empty tool-call field is
ambiguous and must be investigated, not assumed benign.

### 3. Why does the router in this chapter return `None` instead of always picking SOME worker?

**Strong answer:** Some sub-tasks are genuinely ambiguous ("book
something nice" could be a hotel or an activity). A router that always
returns a best-scoring worker, even at a zero or tied score, silently
misroutes ambiguous requests to whichever worker happens to score
highest by coincidence. Returning `None` lets the supervisor escalate
or ask a clarifying question instead of guessing and dispatching
anyway -- the same fail-closed discipline Chapter 6's guardrails use.

**Red flag:** Treats "always dispatch to somebody" as safer than
"sometimes dispatch to nobody."

**Follow-up:** "What should the supervisor actually DO when the router
returns `None` -- what are the options, and which is safest?"

**What this proves:** Applies the fail-closed principle to a routing
decision, not just to a safety/approval gate.

## Intermediate

### 4. How is a sequential pipeline different from supervisor/worker, given that both involve more than one agent-shaped step?

**Strong answer:** In a pipeline, the stage order IS the architecture
-- stage 2 always runs after stage 1 on stage 1's output, with no
decision about WHICH stage handles what; the only thing that could go
wrong is a wrong stage ORDER, which is a code bug, not a
reasoning failure. In supervisor/worker, routing is a LIVE decision
the supervisor makes per sub-task -- which worker handles this
specific sub-task is not fixed in advance the way pipeline stage order
is.

**Red flag:** Describes them as the same pattern under two names, or
says "pipeline" whenever more than one agent-like step exists.

**Follow-up:** "Could a supervisor's dispatch decision feed the FIRST
stage of a pipeline? Are these two patterns mutually exclusive?"

**What this proves:** Distinguishes a fixed-order coordination
mechanism from a live-routing one, even when both involve multiple
agent-shaped steps.

### 5. This chapter's live fan-out test measured roughly a 3.5x speedup running three workers concurrently vs. sequentially. What's the one precondition that makes that speedup safe, and what breaks it?

**Strong answer:** The three workers (flight, hotel, activity search)
must be genuinely INDEPENDENT -- none needs another's result to do its
own job. If, say, the activity-search worker needed the hotel worker's
chosen neighborhood to recommend a nearby tour, running them in
parallel would risk the activity worker acting on stale or missing
data -- a correctness bug, not a speed win. The test for safety is
"does fan-in need to feed back into fan-out," and if yes, the workers
aren't independent.

**Red flag:** Treats parallelization as always safe once multiple
workers exist, without checking for a data dependency between them.

**Follow-up:** "If you discovered mid-project that ExcursionScout
actually DOES need StayScout's chosen neighborhood, how would you
restructure the coordination -- fan-out/fan-in, a pipeline, or
something else?"

**What this proves:** Applies the independence test correctly, the
same test Chapter 8 used for parallel tool calls within one loop, now
one level up at the multi-agent layer.

### 6. What's the most dangerous failure mode a supervisor/worker system can have, and why is it harder to catch than a worker crashing?

**Strong answer:** A worker returning a well-formed, confident,
plausible-looking result that is simply WRONG -- this chapter's
StayScout example returned a real hotel name in the wrong city
(Porto instead of Lisbon) with no exception, no missing tool call, and
no ambiguous routing to flag it. A crash is self-announcing (an
exception the isolation boundary catches); a plausible-but-wrong
result requires actively verifying the RESULT'S CONTENT against what
was requested -- there's no automatic signal that anything went wrong
at all.

**Red flag:** Lists only crash-handling (try/except) as "failure
handling," with no mention of content verification for
non-crashing-but-wrong results.

**Follow-up:** "Design a verification check for a flight-search
worker, analogous to this chapter's `verify_worker_result` city check.
What field(s) would you check, and what would a false result look
like?"

**What this proves:** Distinguishes crash-shaped failures from
silent-content failures and knows both need separate handling.

## Senior

### 7. Design the retry policy for a supervisor dispatching to 3 workers, where dispatch itself is occasionally unreliable (per this chapter's own real, observed malformed-dispatch results). What's the failure mode of a naive retry, and how do you avoid it?

**Strong answer:** A naive "retry whenever `tool_calls` is empty"
policy, applied without tracking what's already been dispatched, can
DOUBLE-DISPATCH the same sub-task -- if the first attempt actually
succeeded internally but the response was malformed on the WAY back,
a retry re-sends the same sub-task to a whole separate worker run,
multiplying that worker's own cost (which may itself involve several
LLM/tool calls), not just retrying one cheap step. The fix is an
idempotent dispatch log keyed on `(subtask, worker)`: before
dispatching, check whether this exact pair has already been
successfully dispatched, and skip if so. This must be a specific
`(subtask, worker)` key, not a coarser "worker already used" key,
since a supervisor legitimately dispatches to the same worker multiple
times for different sub-tasks across one run.

**Red flag:** Proposes a retry policy with no idempotency tracking at
all, or proposes deduplicating on worker name alone (which would
wrongly block a second, legitimate dispatch to the same worker).

**Follow-up:** "How would you handle a sub-task whose EXACT text
varies slightly between attempts (e.g., due to upstream
normalization) -- would your (subtask, worker) key still work?"

**What this proves:** Can design a retry mechanism that solves the
real reliability problem (Section 4/5's malformed dispatch) without
introducing a new cost problem (Section 13's redundant dispatch).

### 8. Your team ships a supervisor/worker system where the supervisor logs "the run failed." What's missing from that log line, and why does it matter operationally?

**Strong answer:** WHICH agent failed, and at what stage. A
supervisor-level bug (misrouting an ambiguous sub-task) and a
worker-level bug (a worker returning wrong content) look IDENTICAL
from outside the system -- both produce a wrong final result -- but
require completely different fixes. `which_agent_responsible`
(extending Chapter 7's `trajectory_correctness` from "which tool" to
"which agent") is the mechanism that turns "the run failed" into
"StayScout returned the wrong city," saving an entire investigation
cycle that would otherwise start by (wrongly) auditing the
supervisor's own routing logic.

**Red flag:** Treats "the run failed, we'll look into it" as
sufficient operational signal, with no mention of attributing the
failure to a specific agent.

**Follow-up:** "How would you extend `which_agent_responsible` to
report not just the FIRST failing agent, but every agent that failed
in a run where more than one sub-task went wrong?"

**What this proves:** Understands that failure attribution, not just
failure detection, is what makes a multi-agent system's failures fast
to fix rather than a mystery.

## Architect

### 9. A stakeholder proposes replacing this chapter's plain-Python supervisor/worker system with a heavy agent framework's built-in graph/crew abstraction, arguing it will handle "all the coordination edge cases automatically." How do you evaluate that claim, given this chapter's own real test results?

**Strong answer:** This chapter's own Section 4 result is direct
counter-evidence to "automatically handled": a framework sitting on
top of the SAME underlying model would still receive the same
malformed, tool-calls-empty response from Ollama -- the framework
doesn't change what the model returns, only how much of the handling
is visible to the engineer. The real question to ask the framework
vendor or maintainer, concretely: how does IT detect a missing tool
call, how does IT decide whether a retry is idempotent, and how does
IT attribute a failure to a specific agent versus the orchestrator?
If those answers are "it just works," that's a red flag, not
reassurance -- the same failure modes this chapter demonstrated live
don't disappear because they're hidden behind an abstraction; they
just become harder to observe and debug when they do occur.

**Red flag:** Accepts "the framework handles it automatically" as
sufficient evidence without asking how, or assumes a framework
eliminates model-level unreliability rather than just wrapping it.

**Follow-up:** "If you had to justify keeping the current plain-Python
version instead of migrating, what's the single strongest
observability argument you'd make?"

**What this proves:** Evaluates a framework claim by checking it
against this chapter's own concrete, observed failure modes rather
than trusting a marketing-level claim.

### 10. Design the budget architecture for a supervisor dispatching to workers whose OWN sub-dispatches might recursively spawn further workers (a worker that is itself a small supervisor). What breaks if each level only enforces its own local budget?

**Strong answer:** A budget enforced only at each individual level
(the top supervisor caps its own steps/cost, each worker caps ITS OWN
steps/cost) can still let the AGGREGATE cost across the whole recursive
tree run far higher than any single level's cap suggests, since
nothing tracks a GLOBAL running total across levels. The correct
architecture threads a single shared budget context (similar to this
chapter's `Blackboard`, but for budget specifically) down through every
level of dispatch, so a worker-that-is-a-supervisor checks the
REMAINING global budget, not just its own local cap, before dispatching
further. Getting this wrong produces a real, silent cost blowup: each
level individually reports "within budget" while the sum across all
levels is not.

**Red flag:** Proposes only per-level local budgets with no shared
global tracking, or assumes recursion "naturally" stays bounded
because each level has its own cap.

**Follow-up:** "How would you detect, from logs alone, that this
exact failure had already happened in a production system, after the
fact?"

**What this proves:** Reasons correctly about budget composition
across a genuinely recursive multi-agent structure, not just the flat
one-supervisor/several-workers case this chapter built.
