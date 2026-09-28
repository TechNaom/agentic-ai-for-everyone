# Chapter 3 Interview Questions: Tool Use and Function Calling

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. Why does topical-keyword tool selection fail on a genuinely overlapping tool set?

**Strong answer:** When more than one tool could plausibly explain the
same symptom, the user's wording doesn't carry the information needed
to disambiguate between them — only the tools' own results do. The
lesson's `naive_first_match` matched "internet is down" to
`run_line_diagnostic` every time, even for a customer whose account
was simply suspended for non-payment, because the keywords "internet"
and "down" sound topically related to a line diagnostic regardless of
what's actually wrong.

**Red flag:** Proposes a bigger or smarter keyword list as the fix,
rather than recognizing that keyword matching on the request's wording
is the wrong signal entirely.

**Follow-up:** "What signal should selection actually be ordered by,
instead of topical similarity?"

**What this proves:** Understands that the failure is structural (the
wrong information source), not a tuning problem.

### 2. What's the difference between a timeout failure and a malformed-output failure?

**Strong answer:** A timeout is when a call never returns anything at
all within a reasonable budget — no data, no error, just silence. A
malformed-output failure is when a call *does* return something, but
not in the expected shape (a raw string instead of a dict, or a dict
missing expected fields). They need opposite retry policies: timeouts
are often transient and worth a bounded retry; malformed output
reproduces identically on retry, so retrying wastes a call for no
benefit.

**Red flag:** Treats both as "the call failed" and proposes the same
generic retry-on-error handling for each.

**Follow-up:** "How would code even detect the difference between
these two, mechanically?"

**What this proves:** Distinguishes failure detection from failure
response, and knows both differ by failure type.

### 3. What is a "succeeds but wrong answer" tool failure?

**Strong answer:** A tool call that returns a perfectly well-formed,
successful-looking result — no error, no malformed shape — that simply
doesn't mean the underlying problem was actually solved. The lesson's
`restart_modem` always returns `{"restarted": True}`, even when the
real cause of the outage was an area-wide fiber cut that a modem
restart can't fix. Nothing about the call itself signals a problem.

**Red flag:** Conflates this with a malformed-output failure, since
both eventually get "caught" by more careful code — the detection
mechanism is entirely different (independent outcome verification, not
shape-checking the response).

**Follow-up:** "Why can't a retry policy help with this failure type at
all?"

**What this proves:** Recognizes that a "successful" tool call can
still represent a failure at the level of the actual goal.

## Intermediate

### 4. Walk through why the lesson orders NetBot's tool checks account-status, then outage-status, then line-diagnostic — not some other order.

**Strong answer:** Each check is ordered by cost and decisiveness, not
topical relevance. `check_account_status` goes first because a
suspension is a single cheap lookup that, if true, fully explains the
symptom with no further evidence needed. `check_outage_status` goes
second for the same reason — still cheap, still fully decisive when
true. `run_line_diagnostic` goes last because it's the most expensive
of the three and the least likely to be needed once the two cheaper,
equally decisive explanations are ruled out.

**Red flag:** Says the order is "just how the tools happen to be
listed" or defends it by topical relevance rather than cost/
decisiveness.

**Follow-up:** "How would this ordering change if `run_line_diagnostic`
became the cheapest of the three tools to call?"

**What this proves:** Can articulate the actual design principle behind
an ordering decision, not just describe the order itself.

### 5. A teammate proposes wrapping every tool call in one shared `try/except: retry up to 3 times` helper. What's wrong with that, specifically?

**Strong answer:** It actively under-serves two of the three failure
types this chapter identified. Applied to a malformed-output failure,
it wastes up to 3 calls retrying something that will return the
identical malformed result every time (proven directly in the
lesson). Applied to a succeeds-but-wrong-answer failure, it does
nothing at all, because nothing ever raises an exception in the first
place — the loop would never even trigger.

**Red flag:** Defends the shared wrapper as "simpler" without
acknowledging the two concrete failure modes it doesn't handle
correctly.

**Follow-up:** "What would you need to add to make one wrapper capable
of handling all three failure types correctly?"

**What this proves:** Can name the specific, concrete cost of a
tempting-but-wrong simplification, not just gesture at "it's not
robust."

### 6. Why are `normalize_account_id` and `normalize_zip` written as two separate functions instead of one shared string-cleanup helper?

**Strong answer:** Each argument type drifts in its own way, shaped by
whatever upstream system produces it — account IDs pick up dashes,
spaces, and stray punctuation; ZIP codes pick up a ZIP+4 suffix or
arrive as a raw `int`. A single shared strip-and-lowercase helper would
under-handle at least one of these drift patterns (it wouldn't extract
digits from `"Acct #1029"`, and it wouldn't split off a ZIP+4 suffix).
Writing them separately, each matched to its own argument's real drift
pattern, catches both correctly.

**Red flag:** Argues for one generic normalizer "to keep the code
DRY" without checking whether it actually covers both real drift
patterns.

**Follow-up:** "What's a normalize function's failure mode when it's
too generic, versus too narrow?"

**What this proves:** Distinguishes real code reuse from
superficially-similar functions that would actually behave
differently under real drift.

## Senior

### 7. Design a tool-failure classification function for a system you don't control the tools for. What would you actually check?

**Strong answer:** Check, in order: did the call return within budget
at all (timeout, detected by a bounded-wait wrapper like
`call_with_timeout`)? If it returned, is the result the expected shape
(a dict, with the expected keys) — if not, malformed output, and it
should never be retried, since the same input reproduces it. If it's a
well-formed success, is there independent evidence that would confirm
or contradict the claimed outcome, if any evidence source exists for
this particular tool? If none exists, that tool is structurally exposed
to an undetectable succeeds-but-wrong-answer failure, and that's worth
flagging as a design gap, not silently accepting.

**Red flag:** Proposes checking only for exceptions or non-2xx status
codes, missing that a "successful" response can still be wrong.

**Follow-up:** "Which of NetBot's tools has no available independent
evidence source at all, and what would you do about that?"

**What this proves:** Can generalize this chapter's three-type
classification into a reusable design process for tools not seen
before.

### 8. How would you detect a succeeds-but-wrong-answer failure in a production trace, given that nothing errors and nothing looks malformed?

**Strong answer:** The same way Chapter 2's wrong-plan failures get
caught — not at the execution level (nothing there signals a problem),
but at the outcome level: does the final state actually match what the
tool claimed? For `restart_modem`, that means checking outage status
again after the "successful" restart and comparing. This requires the
tool's *claim* and independent *evidence* to be logged separately, so
a reviewer (human or automated) can compare them after the fact —
logging only "restart_modem: success" throws away the information
needed to ever catch this.

**Red flag:** Assumes tool-level success/failure logging alone would
eventually surface this, without addressing that the log itself never
contains contradicting evidence.

**Follow-up:** "What would you log about `restart_modem` specifically,
beyond its own return value, to make this failure reviewable later?"

**What this proves:** Understands that observability for this failure
type requires capturing evidence the tool itself doesn't report.

### 9. When should a system add an outcome-verification step for every tool, and when is it overkill?

**Strong answer:** Add it when a tool's own success signal could
plausibly be wrong for a reason the tool has no way to detect itself
(a root cause outside its own scope, like `restart_modem` being unable
to detect an area outage). It's overkill for tools where success
genuinely means success with no gap — `check_account_status` returning
real account data doesn't need independent verification, because
there's no way for that read to "succeed" while being wrong about what
it read. The decision hinges on whether the tool *acts* on the world
(where a gap between "the action was taken" and "the problem was
solved" can exist) versus whether it only *reports* on the world.

**Red flag:** Proposes outcome verification for every single tool
uniformly, without distinguishing action tools from read-only tools.

**Follow-up:** "Is a tool that both reads and writes (like a combined
check-and-fix endpoint) more like an action tool or a read tool, for
this purpose?"

**What this proves:** Applies the concept selectively based on a real
mechanism (action vs. report), not as a blanket policy.

## Architect

### 10. Design a standard your team could require of every new tool before it ships, covering both selection and failure handling.

**Strong answer:** Every new tool's description must state, in the
same review, (1) what other existing tools it overlaps with in what
they could answer, and where in the cost/decisiveness ordering it
belongs relative to those; (2) every real argument-formatting
variation it's likely to see in production, with a normalizer matched
to that specific drift pattern, not a generic one; (3) which of the
three failure types (timeout, malformed output, succeeds-but-wrong-
answer) apply to it, with an explicit, named policy for each that does
apply — and if succeeds-but-wrong-answer applies but no independent
evidence source exists to verify it, that gap must be flagged and
either accepted explicitly or fixed before shipping, not silently
inherited by everything downstream that calls this tool.

**Red flag:** Proposes a single "add error handling" checkbox review
step instead of the three-part standard above, collapsing distinct
failure types back into one undifferentiated concern.

**Follow-up:** "How would you enforce this standard automatically,
rather than relying on a reviewer remembering to ask all three
questions?"

**What this proves:** Can turn this chapter's three worked mechanisms
(selection ordering, drift-specific normalization, differentiated
failure policy) into an enforceable, reusable engineering standard, not
just three separate worked examples.
