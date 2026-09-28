# Chapter 5 Interview Questions: Reflection and Self-Correction

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. What is reflection, and how is it different from just writing a better prompt?

**Strong answer:** Reflection is a second, genuinely separate step
that evaluates a draft response against a standard (correctness,
completeness, policy compliance) and revises it if that standard
isn't met. A better or more careful-sounding prompt ("think step by
step and double-check your work") is still one pass — nothing
independently checks what that one pass produced. Reflection requires
an actual second evaluation, with its own inputs and its own pass/fail
criteria, not just more effort spent up front.

**Red flag:** Describes reflection as "just prompting the model to be
more careful," missing that the defining feature is a separate check,
not a more elaborate first attempt.

**Follow-up:** "If an agent has no reflection step at all, what
specifically can go wrong that a careful prompt alone can't prevent?"

**What this proves:** Understands the core architectural distinction
this chapter is built on — reflection as a designed component, not a
prompting trick.

### 2. Why does a "grounded" reflection check (like this chapter's verify_draft()) matter more than a model reviewing its own answer?

**Strong answer:** A grounded check independently re-derives the
correct facts (recomputing a price from a rate card, for example)
rather than trusting whatever the draft claims, then compares. A model
reviewing its own answer in isolation has nothing but its own
judgment to rely on, and this chapter's own real session showed that
judgment can correctly name a problem and still produce a "fix" that
doesn't actually solve it. Grounded checks catch what ungrounded
self-review can miss.

**Red flag:** Assumes any second model call automatically counts as a
reliable check, without asking what it's actually being compared
against.

**Follow-up:** "What do you do when there's no independently-derivable
ground truth to check against at all?"

**What this proves:** Recognizes that not all "reflection" is equally
reliable, and can name why.

### 3. What's wrong with "reflection" that just re-asks the model the same question a second time?

**Strong answer:** That's a retry, not reflection — no independent
check ever runs against anything, so a systematic error (the kind a
model tends to reproduce on the same prompt, not roll differently each
time) is likely to come back unchanged, or changed only by chance.
Reflection requires a genuinely separate evaluation step with its own
criteria, not just another attempt at the original task.

**Red flag:** Treats "ask again" and "reflect" as interchangeable,
without acknowledging that a retry has no mechanism for actually
catching what went wrong the first time.

**Follow-up:** "How would you tell, from a production trace alone,
whether a system is doing real reflection or disguised retries?"

**What this proves:** Doesn't mistake superficially similar-looking
mechanisms for the same thing.

## Intermediate

### 4. Walk through a real reflection step catching an arithmetic error. What made the check reliable?

**Strong answer:** This chapter's BikeBot pricing example: a naive
draft understated a price by one dollar, and a verifier function
independently recomputed the correct price from the rate card and
hours, rather than trying to "read" whether the draft's number sounded
right. Comparing the draft's claimed number against that independently
computed value is what made the check reliable — it didn't matter how
plausible the draft looked, only whether the number matched.

**Red flag:** Describes the check only as "the model looked at its own
answer again," missing the independently-computed value that made the
comparison meaningful.

**Follow-up:** "What would you change if the correct value wasn't
computable from a fixed formula, but depended on a live lookup?"

**What this proves:** Can explain a grounded check mechanically, not
just describe its outcome.

### 5. This chapter's own real self-critique call correctly said a draft was "INCOMPLETE" but its own revision still didn't fix the gap. Why does this happen, and what's the fix?

**Strong answer:** The critique call was asked to judge completeness,
which it did correctly, but nothing forced its own revision to
actually compute and state the missing number — it just reworded the
same deferred question. This happens because a model producing a
"fix" is still just generating plausible-sounding text, with no
built-in mechanism guaranteeing the fix satisfies the original
standard. The fix is layering a grounded, deterministic check on top
of (or instead of) the live critique, so the final output is verified
against real facts, not just a second round of the model's own
judgment.

**Red flag:** Assumes a model that correctly diagnoses a problem will
also reliably fix it, without a separate verification step confirming
the fix actually worked.

**Follow-up:** "If you only had a live critique call available, with no
computable ground truth, how would you reduce this risk?"

**What this proves:** Understands that diagnosis and correction are
two separate capabilities that can fail independently.

### 6. What's the difference between "revise-the-answer" correction and "gather-more-evidence" correction?

**Strong answer:** Revise-the-answer correction rewrites a response
using facts the agent already has — fixing a wrong number or missing
detail by rewording. Gather-more-evidence correction recognizes the
draft can't be fixed by rewording at all, because the agent never had
the right information, and triggers a different tool call (or the same
tool with different arguments) instead. The first is purely about
presentation; the second is about deciding more information is needed
before any answer can be trusted.

**Red flag:** Treats every correction as a rewording problem, without
recognizing that some drafts are wrong because of a missing tool call,
not a wording issue.

**Follow-up:** "How would a reflection step decide which of the two
corrections a given draft needs?"

**What this proves:** Distinguishes two genuinely different repair
strategies that a single "just fix it" mental model conflates.

## Senior

### 7. Design a reflection step for a new domain you haven't seen before. What would you actually decide?

**Strong answer:** First, what's actually checkable — is there a
computable ground truth (a price, a policy rule, a required field) to
compare a draft against, or only a live model's own judgment available?
This chapter proved grounded checks catch failures ungrounded review
misses, so use one wherever a computable standard exists. Second, what
specific failure classes matter enough to check for at all (this
chapter checked price correctness and one policy rule; a different
domain needs its own list) rather than a vague "check if this seems
right." Third, decide the iteration bound and escalation path before
shipping, not after a runaway loop is observed in production. Fourth,
decide explicitly when reflection should NOT run — for low-stakes,
easily-verified requests, the extra cost isn't worth it.

**Red flag:** Jumps straight to "add a review step" without first
asking whether there's anything concrete to check the draft against.

**Follow-up:** "What would you log to detect, after the fact, whether
your reflection step is actually catching real problems or just adding
latency?"

**What this proves:** Can generalize this chapter's specific
mechanisms into a reusable design process for reflection in an
unfamiliar domain.

### 8. A teammate proposes running a full reflection pass (a second model call) on every single request, "to be safe." What's the actual cost of this?

**Strong answer:** Beyond the direct latency and API cost of a second
call on every request (this chapter's own live self-critique call took
over 40 seconds), the deeper cost is that reflection provides zero
benefit on requests with an obviously correct, unambiguous first
answer — this chapter's own live example (a simple 7-hour multiplication
the model got right unprompted) showed a reflection step correctly
finding nothing wrong, meaning the extra call bought nothing. Applied
universally, that "nothing" happens on most requests, most of the
time, while the cost is paid on all of them. The right design routes
reflection to where a wrong answer has real cost and something
checkable exists, not everywhere by default.

**Red flag:** Argues reflection is "basically free" or treats
latency/cost as a minor afterthought rather than a real trade-off tied
directly to how often reflection actually changes the outcome.

**Follow-up:** "How would you measure, in production, whether your
reflection step is worth its cost?"

**What this proves:** Reasons about reflection as a cost/benefit
trade-off, not just a safety feature that's always worth adding.

### 9. How would you detect, in a production trace, that a system's "reflection" step is actually a disguised retry?

**Strong answer:** Look for whether the same underlying error type
recurs across sessions despite "reflection" supposedly having run —
if the corrected output isn't meaningfully different from the
original, or fails the exact same way on a similar input, that's a
signal no independent check ever actually ran. A genuine reflection
step's revision should trace back to a specific, nameable problem it
caught (a specific field, a specific fact that didn't match); a
disguised retry's "revision" has no such traceable cause — it's just
a different generation.

**Red flag:** Looks only at whether the final output changed between
attempts, missing that a disguised retry can also produce different
output by chance without ever having actually checked anything.

**Follow-up:** "What would you add to the system's logging to make
this distinction observable without having to infer it after the
fact?"

**What this proves:** Can reason about a subtle process failure from
its observable symptom pattern, not just assume any retry loop is
functioning as reflection.

## Architect

### 10. Design a standard your team could require of every new agent's reflection system before it ships.

**Strong answer:** Every new reflection system must state, in the same
review: (1) exactly what standard(s) it checks a draft against, named
concretely (a specific computable fact, a specific policy rule) rather
than a vague "does this look right"; (2) whether each check is
grounded (independently computed) or relies on a live model's own
judgment, with a plan for the latter's known unreliability (this
chapter's own real example of a correct diagnosis with an incorrect
fix); (3) a hard iteration bound with a defined escalation path,
tested against an input specifically designed to never satisfy the
check, since an unbounded loop is invisible until exactly that case
occurs; (4) an explicit routing policy for when reflection runs versus
skips, backed by a stated reason (stakes, checkability) rather than
"always" or "whenever it seems safer"; (5) a stated boundary on what
reflection can and cannot undo — text it hasn't returned yet, versus
an action (a tool call) that already executed, which is a guardrail's
job, not reflection's.

**Red flag:** Proposes a single "make sure reflection exists" checkbox
review, collapsing five genuinely distinct, independently-failing
concerns back into one undifferentiated concern.

**Follow-up:** "Which of these five would you automate as a CI check
that runs against synthetic adversarial inputs, versus leave as a
design-review question, and why?"

**What this proves:** Can turn this chapter's five worked mechanisms
(grounded checking, the ungrounded-critique limit, iteration bounding,
selective routing, and reflection's action-vs-text boundary) into an
enforceable, reusable engineering standard, not just five separate
worked examples.
