# Chapter 7 Interview Questions: Evaluating Agent Reliability

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. What's the difference between task-success rate and trajectory correctness?

**Strong answer:** Task-success rate checks whether the trace contains
the tool calls that actually produce a correct outcome, regardless of
order or extra steps -- a forgiving metric. Trajectory correctness
checks whether the right tools were called, with the right arguments,
in the right order, compared against a ground-truth expected
trajectory -- a strict metric. A run can pass the first and fail the
second, as this chapter's own T4 task showed (100% task success, only
60% trajectory correctness).

**Red flag:** Treats the two as interchangeable, or assumes a high
task-success rate implies a well-behaved process.

**Follow-up:** "If you could only track one of these two metrics in
production, which would you pick, and what would you lose?"

**What this proves:** Understands that "it worked" and "it worked the
right way" are separate, both-necessary questions for a multi-step
agent.

### 2. Why can't a single test run tell you whether an agent is reliable?

**Strong answer:** This chapter's own live result is the direct proof:
the identical task, sent to the same model six separate times, picked
four different first tool calls, and only 1 of 6 matched the correct
one. A single run -- pass or fail -- says nothing about how the agent
behaves on the next, statistically identical attempt. Reliability
requires running the same task multiple times and reporting a rate, not
a single pass/fail.

**Red flag:** Treats one successful manual test as evidence the agent
"works," with no repeated-trial measurement behind that claim.

**Follow-up:** "How many repeated runs would you want before trusting a
reported success rate, and why?"

**What this proves:** Understands non-determinism as a first-class
property of LLM-driven agents, not an edge case.

### 3. What does "cost-per-success" measure that "cost-per-run" doesn't?

**Strong answer:** Cost-per-run averages spend across every attempt,
including failed ones, which hides how expensive it actually is to get
one usable result. Cost-per-success divides total spend by the count of
*successful* runs only, so a task with a low success rate shows up as
expensive per success even if each individual run is cheap -- exactly
what this chapter's T5 task demonstrated (shortest trajectory, highest
cost-per-success, because more of its runs were wasted).

**Red flag:** Reports only an average per-call cost and never connects
it to the task's own success rate.

**Follow-up:** "If a task's cost-per-run is low but its success rate is
also low, what does that do to cost-per-success?"

**What this proves:** Understands that unsuccessful attempts are not
free, and that per-call cost alone is an incomplete efficiency signal.

## Intermediate

### 4. This chapter's cross_check_claim function said a $12M claim "matched" a $9.4M record. What kind of failure is that, and which of this chapter's metrics catches it?

**Strong answer:** This is a content-correctness failure, not a process
failure -- the tool ran, returned a result, and every tool in the
trajectory fired in the correct order, so trajectory correctness scores
this run as perfect, and task success (which only checks that a
citation was drafted) also scores it as a pass. Neither of this
chapter's own metrics catches it, because both check *process*, not the
*substance* of what a tool actually returned. Catching this specific
failure requires either a stricter tool implementation (compare the
actual numbers, not just word overlap) or a real content-correctness
judge -- the kind `llm-evaluation-for-everyone`'s own LLM-as-judge
chapters build.

**Red flag:** Claims trajectory correctness or task success "would
catch" this, revealing they don't understand what those two metrics
actually check.

**Follow-up:** "Where in this chapter's `build_eval_report()` is there
an explicit, named seam for a content-correctness check to plug in?"

**What this proves:** Understands the real boundary between this
chapter's process metrics and the sibling course's output-correctness
methodology -- not just that a boundary exists, but exactly where it
falls on a concrete example.

### 5. What is pass@k, and why report pass@1 alongside it instead of just the highest k you tested?

**Strong answer:** pass@k estimates the probability that at least one
of k randomly chosen attempts (out of n total, c of which succeeded) is
a success -- it models a retry policy. Reporting only a high-k number
(this chapter's own pass@3, which hit 1.0 off a 0.95 pass@1) can make an
agent look far more reliable than its actual single-shot behavior,
because it's really measuring the retry budget's effect, not the
agent's own per-attempt quality. pass@1 is the honest single-shot
number; higher-k numbers should always be reported alongside it, not
instead of it.

**Red flag:** Reports a single "reliability: 98%" number derived from
pass@5 or higher with no mention of pass@1, or doesn't know the
difference.

**Follow-up:** "If an agent's pass@1 is 40% but pass@5 is 95%, what does
that combination tell you about designing its retry policy and its real
cost?"

**What this proves:** Understands non-determinism metrics well enough
to avoid (or catch) a common way reliability numbers get inflated.

### 6. What is multi-turn drift, and why is it specific to agents rather than single LLM calls?

**Strong answer:** Multi-turn drift is a decline in trajectory
correctness (or task success) as a session accumulates more turns --
this chapter's own seeded demo showed average correctness drop from 0.8
in the first five turns to 0.6 in the second five of a ten-turn
session. It's specific to agents because it's a property of a *loop*
running across multiple turns/steps, with accumulating context and
state; a single, isolated LLM call has no "turn 7" to degrade relative
to "turn 1." That's exactly why this question belongs in this course
and not in a course that evaluates single-call output quality.

**Red flag:** Describes drift as "the model getting worse over time" in
a way that implies model degradation, rather than a property of a
specific session's accumulating context.

**Follow-up:** "What would you log, per turn, to actually detect drift
in a production agent, rather than only seeing it in hindsight from a
full transcript?"

**What this proves:** Correctly scopes drift as a loop/session property
that requires per-turn instrumentation to see at all.

## Senior

### 7. Design an eval harness for a customer-support agent that can look up an order, issue a refund, or escalate to a human. What would your task set and metrics look like?

**Strong answer:** A real answer defines, per task: a claim/request, a
ground-truth expected tool-call trajectory (e.g., look-up-order before
refund, never refund before confirming order exists), and a separate,
more forgiving success condition (did a refund or escalation actually
happen, regardless of exact order). It runs each task N times with a
fixed seed (or N live calls, budgeted), computes task-success rate AND
trajectory-correctness rate separately, computes pass@k for at least
k=1 and one higher k tied to the real retry policy, tracks cost-per-
success (not cost-per-run), and -- since support sessions are
multi-turn -- tracks trajectory correctness per turn to catch drift
across a long session. It explicitly does NOT try to grade whether the
refund amount's wording is polite or well-written -- that's
`llm-evaluation-for-everyone`'s output-quality territory.

**Red flag:** Proposes a single "did the conversation resolve
successfully" binary with no separate trajectory check, no repeated
runs, and no cost or drift tracking.

**Follow-up:** "Your refund task might require looking up the order
either before or after checking the customer's account standing --
does a strict ordered-trajectory match actually work here, or does this
call for something looser?"

**What this proves:** Can apply this chapter's full metric set to a
genuinely new scenario, including recognizing when strict ordering is
or isn't the right ground truth.

### 8. A trajectory-correctness check is collapsing consecutive duplicate tool calls before comparing against the expected trajectory. Why, and what's the risk of that choice?

**Strong answer:** Collapsing consecutive duplicates lets a deliberate,
cautious re-check (the agent calling the same tool twice in a row on
purpose, e.g. to re-verify) pass without being penalized as an
out-of-order or extra step -- this chapter's own `trajectory_
correctness()` does exactly this. The risk: it also silently forgives a
wasteful or buggy agent that calls the same tool twice for no good
reason, since the check can't distinguish "deliberate re-check" from
"redundant retry with no new information." A stricter implementation
might cap how many consecutive duplicates are tolerated, or log
duplicate-call counts as a separate signal even while not treating them
as outright failures.

**Red flag:** Doesn't recognize the trade-off at all, or assumes any
de-duplication logic is purely a "nice to have" with no downside.

**Follow-up:** "How would you tell, from the trace alone, whether a
duplicate call was a deliberate re-check or a bug?"

**What this proves:** Can reason about the second-order consequences of
a metric-design choice, not just implement the metric as given.

## Architect

### 9. Your team reports 95% task success and 92% trajectory correctness for a production agent, both measured from a 20-run seeded simulation, not live traffic. What's your first question back to them?

**Strong answer:** Whether that simulation's error-rate parameters were
ever calibrated against real behavior, and how recently -- this
chapter's own harness explicitly discloses that its simulation's 0.17
step-error rate came from a live 1-in-6 result, not an invented number,
specifically so the gap between "what we measured" and "what we're
claiming about production" stays visible. A simulation that was
calibrated once, months ago, against an older model version or an
earlier tool set, can silently drift out of sync with real production
behavior while continuing to report a stable, reassuring number. The
senior/architect-level question is always: when was this simulation
last checked against a real sample of live traffic, and by how much did
they diverge.

**Red flag:** Accepts the reported numbers at face value with no
question about calibration provenance or recency.

**Follow-up:** "How would you design a lightweight, ongoing process to
re-calibrate that simulation against a small live sample on a
schedule, without paying for full live-traffic evaluation on every
run?"

**What this proves:** Understands that a disclosed simulation is a
legitimate engineering trade-off only as long as its calibration is
tracked and refreshed -- not a one-time excuse to avoid live
measurement forever.

### 10. How would you decide whether a regression in trajectory correctness across a model or prompt change is real, or just noise from this chapter's own kind of run-to-run variance?

**Strong answer:** This chapter deliberately stops short of answering
this -- it's exactly `llm-evaluation-for-everyone`'s own territory
(sample size, confidence intervals, and significance testing, that
course's Chapters 7-8). The honest architect-level answer names that
boundary explicitly: compute a confidence interval around each
version's trajectory-correctness rate using that course's methodology,
and run a significance test (e.g. a two-proportion test) before
concluding a drop is real rather than an artifact of this chapter's own
documented run-to-run non-determinism (Section 11's pass@1 vs. pass@3
gap is a small-scale preview of exactly this problem). Treating any
single before/after delta as conclusive, without that statistical step,
is the mistake this question is designed to surface.

**Red flag:** Proposes just re-running once more and eyeballing whether
the new number "looks lower," with no statistical framework at all.

**Follow-up:** "Given this chapter's own n=20 runs per task, is that
sample size even large enough to detect a meaningful regression with
reasonable confidence?"

**What this proves:** Correctly routes a genuinely different, harder
question to the right body of methodology instead of improvising a
weaker answer inside this chapter's own, deliberately narrower scope.
