# Chapter 8 Interview Questions: Cost and Latency Control of Agent Loops

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. What's the difference between a fail-closed budget and a fail-open one, and why does this chapter insist on fail-closed?

**Strong answer:** A fail-closed budget denies the next step the
moment any cap (steps, tokens, time, or cost) is exceeded -- the
default is "stop." A fail-open budget would let a step through unless
explicitly blocked, or would only log a warning and continue. This
chapter's `BudgetGuard` raises `BudgetExceeded` and the caller must
decide what "denied" means, mirroring Chapter 6's own fail-closed
guardrail discipline (`human_approved` defaulting to `False`). An
unbounded loop that only warns on overrun can still run up unlimited
real cost while the warning is being read.

**Red flag:** Thinks a budget that "logs a warning past the limit" is
equivalent to one that actually stops execution.

**Follow-up:** "If a budget check silently clamped a step's token
count instead of denying the step outright, what would that hide?"

**What this proves:** Understands that a budget only controls cost if
it can actually refuse to run, not just observe.

### 2. What's the difference between early termination (this chapter) and Chapter 1's max_iterations?

**Strong answer:** `max_iterations` is a safety cap: it exists to stop
a runaway loop that never converges, and hitting it usually means
something went wrong. Early termination is the opposite direction --
it stops a loop EARLY, as soon as the trace already satisfies the
task's success condition, specifically to avoid paying for unnecessary
extra steps on a run that's already succeeding. One is a worst-case
backstop; the other is a best-case efficiency win.

**Red flag:** Describes them as the same mechanism with different
names.

**Follow-up:** "Could a loop have both a max_iterations cap AND an
early-exit check? What would each one catch that the other wouldn't?"

**What this proves:** Distinguishes a safety bound from a cost/latency
optimization, even though both involve "stopping a loop early."

### 3. Why is cost-per-run not enough, and what does cost-per-success add?

**Strong answer:** Cost-per-run averages spend across every attempt,
including failed ones that consumed tokens and time but produced
nothing usable. Cost-per-success (built in Chapter 7, reused here)
divides total spend by only the successful runs, so a technique that
makes runs cheaper but also less likely to succeed can still come out
looking WORSE on cost-per-success even though cost-per-run dropped --
exactly the honest check this chapter's own Section 13 ran before
calling its before/after result a real win.

**Red flag:** Reports only a raw cost reduction percentage with no
mention of whether success rate changed at all.

**Follow-up:** "If a change cuts cost-per-run by 80% but also cuts
success rate in half, what happens to cost-per-success?"

**What this proves:** Understands why a cost-reduction claim needs a
success-rate check attached to be trustworthy.

## Intermediate

### 4. This chapter's live test showed a ~20x latency gap between a capped, one-word decision call and an open-ended reasoning call for the exact same model and the exact same task. What does that actually demonstrate, and what doesn't it demonstrate?

**Strong answer:** It demonstrates that PROMPT SHAPE and output-length
capping alone -- with no model change at all -- can produce a huge
real latency difference, which is why model routing (Section 7) works
even in a sandbox with only one model pulled. It does NOT demonstrate
that a genuinely smaller/cheaper separate model would show the exact
same ratio -- that's a related but different lever (a different model,
not just a different prompt/cap), named but not tested live in this
chapter.

**Red flag:** Concludes "cheaper models are always ~20x faster" from
this one result, conflating prompt-shape effects with model-choice
effects.

**Follow-up:** "If you had two genuinely different models available,
how would you design a fair live comparison, controlling for prompt
shape and output length on both sides?"

**What this proves:** Can separate the specific variable a live result
actually isolated from other plausible causes of the same outcome.

### 5. Why does this chapter keep `cross_check_claim` on the strong model tier instead of routing every step to the cheapest option?

**Strong answer:** Chapter 7's own real bug ($12M claim reported as
"matching" a $9.4M record via a naive word-overlap heuristic) was a
content-judgment failure specifically in that step. Routing the step
most prone to that exact failure to an even less careful tier would
make the bug MORE likely, not less. Model routing is about matching
model strength to a step's actual difficulty and risk, not minimizing
cost everywhere indiscriminately.

**Red flag:** Treats "route everything to the cheapest model" as an
unqualified win with no consideration of which steps carry judgment
risk.

**Follow-up:** "How would you decide, for a brand-new tool you've never
seen fail, whether it belongs on the cheap tier or the strong tier?"

**What this proves:** Applies model routing as a risk-aware design
decision, not a blanket cost-minimization rule.

### 6. Why is caching without invalidation described in this chapter as a real, disclosed limitation rather than a finished feature?

**Strong answer:** The chapter's `ToolCache` never expires or
invalidates an entry -- it assumes the underlying fact never changes
during the cached period. That's fine for FactScout's own fixed
archive within one session, but genuinely wrong for any tool whose
answer can legitimately change (a source's credibility being
re-evaluated, a claim's status being updated). Shipping this cache
as-is against a tool with mutable underlying state would silently
serve stale results forever.

**Red flag:** Treats caching as risk-free once hit/miss counters exist,
with no mention of staleness.

**Follow-up:** "What would you add to this cache to make it safe for a
tool whose underlying data changes daily?"

**What this proves:** Recognizes that a cache's correctness depends on
data volatility, not just on whether hits/misses are being counted.

## Senior

### 7. Design the cost/latency control layer for a research agent that fires 4 independent lookup tools per query and sometimes needs a 5th, dependent synthesis step. What would you parallelize, and what would you NOT parallelize?

**Strong answer:** The 4 independent lookups (by definition, none needs
another's result) are exactly the safe case for `ThreadPoolExecutor`-
style concurrency, mirroring this chapter's own 3.2x measured
real-call speedup on two independent lookups. The 5th synthesis step
depends on the first 4's combined output, so it must run strictly
after all 4 complete -- running it in parallel with any of them risks
synthesizing from partial or missing data, the same dependency bug this
chapter's Section 9 explicitly calls out with `cross_check_claim`. A
complete answer also adds a budget covering all 5 steps together (not
per-lookup), since the parallel lookups' wall-clock savings shouldn't
be allowed to mask a runaway total-cost number if all 4 lookups
individually route to an expensive tier.

**Red flag:** Proposes parallelizing all 5 steps including the
synthesis step, or doesn't distinguish independent from dependent
steps at all.

**Follow-up:** "If one of the 4 lookups is consistently the slowest,
does that change anything about how you budget or route it?"

**What this proves:** Can apply the independence test correctly to a
new, more complex tool graph, not just repeat this chapter's own
5-tool example.

### 8. Your team reports "we cut cost by 60%" after adding model routing and caching. What's the first number you ask for before believing that's a real win?

**Strong answer:** The before-and-after success rate (or, ideally,
cost-per-success directly) for the same task set, not just the raw
cost delta. This chapter's own Section 13 result (51% cost reduction,
92.3% latency reduction, with an honestly disclosed small per-task
success dip) only counts as a real win because cost-per-success was
recomputed and shown to improve DESPITE that dip -- a team that reports
only the cost delta could be quietly hiding a success-rate regression
serious enough to make the change a net loss once cost-per-success is
computed.

**Red flag:** Accepts "we cut cost by 60%" as sufficient evidence of
improvement with no success-rate context at all.

**Follow-up:** "If the same team's success rate dropped from 90% to
40%, would you still call this a win? How would you phrase the
trade-off to a stakeholder?"

**What this proves:** Treats a raw cost-reduction claim as incomplete
until paired with a success-rate check, matching this chapter's own
central discipline.

## Architect

### 9. This chapter's before/after uses a seeded simulation calibrated from Chapter 7's own live 1/6 result, run at scale (20 runs x 5 tasks) rather than live model calls. What's the architect-level risk of shipping a cost/latency-control redesign based only on this kind of offline measurement?

**Strong answer:** The simulation's error-rate parameters (and
everything downstream of them -- the reported cost reduction,
latency reduction, and cost-per-success deltas) are calibrated from a
small, specific live sample taken at one point in time. Real
production traffic could have a materially different failure
distribution (different claim types, different edge cases, provider-
side latency variance this local sandbox never sees), meaning the
offline numbers could overstate or understate the real-world
before/after gap. The correct architect-level move is to treat this
chapter's own reported percentages as a hypothesis to validate with a
staged rollout against real traffic (e.g., a canary or shadow
deployment comparing before/after cost-per-success on live requests),
not as a guaranteed production outcome.

**Red flag:** Treats the simulated percentages (51% cost reduction,
92.3% latency reduction) as production-guaranteed numbers with no
mention of validating them against real traffic.

**Follow-up:** "How would you design a canary rollout that measures
real cost-per-success before fully committing to this redesign?"

**What this proves:** Understands the difference between a
well-calibrated offline estimate and a validated production result,
and knows the next concrete step to close that gap.

### 10. A stricter fail-closed BudgetGuard denies a step once any single cap is exceeded -- but the actual step that would have completed the task was the one denied. How do you decide what "denied" should mean for a real product, and what's the failure mode of getting this wrong?

**Strong answer:** "Denied" needs its own policy, separate from
detecting the violation -- this chapter deliberately left that
decision to the caller, the same split Chapter 6's dispatcher used
between detecting a guardrail violation and deciding the response. For
a real product, reasonable options include: return the best partial
result gathered so far with an explicit "budget-limited" flag (honest
partial success), escalate to a human or a more expensive tier as a
one-time exception, or fail the request outright and surface the exact
budget that was hit so an operator can decide whether to raise it. The
failure mode of getting this wrong either way: silently returning a
wrong/incomplete answer as if it were a normal success (hiding the
budget hit from the user) or blocking a customer-facing request with no
explanation at all, when a small, deliberate one-time budget increase
would have been the right call.

**Red flag:** Assumes "denied" always means the request simply fails
with no further design thought, with no consideration of partial-
result or escalation policies.

**Follow-up:** "Would you ever let a specific, logged, human-approved
exception override a budget cap for one single request? What would
have to be true for that to still be safe?"

**What this proves:** Recognizes that fail-closed enforcement and
graceful, honest denial-handling are two separate design decisions,
and can reason about both without conflating "safe" with "silent."
