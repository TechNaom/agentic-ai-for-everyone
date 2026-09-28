# Chapter 6 Interview Questions: Guardrails and Safety for Autonomous Agents

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. What is a guardrail, and how is it different from a reflection step?

**Strong answer:** A guardrail is a hard, enforced boundary that
decides whether an action is allowed to execute, checked *before* the
action dispatches. Reflection (Chapter 5) is a check on the *text* an
agent is about to return, run *after* a draft exists — and, critically,
often after a tool call driven by that draft has already fired.
Reflection can revise what an agent says; only a guardrail, sitting at
the tool-dispatch step itself, can stop what an agent *does* before it
happens.

**Red flag:** Describes a guardrail as "basically the same as
reflection but for actions," missing that the defining difference is
*when* the check runs relative to the side effect — before versus
after.

**Follow-up:** "If an agent has a strong reflection step but no
guardrail, what specific class of failure can still happen?"

**What this proves:** Understands the core architectural distinction
this chapter is built on, in direct continuity with Chapter 5's own
named limit.

### 2. Why can't a guardrail just live in the system prompt ("never transfer more than $500 without asking")?

**Strong answer:** A system prompt instruction is something the model
has to remember, correctly interpret, and choose to follow every single
time — and this chapter's own live test showed the *same* model, given
an injected instruction, resisting it under one framing and complying
with it under another. A guardrail has to be enforced in code, at the
one place a tool call must pass through before it executes, so it holds
regardless of what the model decided or how convincingly a later
instruction argued against it.

**Red flag:** Treats a clearly-worded system prompt as functionally
equivalent to an enforced check, without acknowledging that anything in
the prompt is itself just more text the model is reasoning over.

**Follow-up:** "Where exactly in an agent's code should the guardrail
check actually live?"

**What this proves:** Understands that "the model was told not to" and
"the system will not let it" are categorically different guarantees.

### 3. What's wrong with a guardrail that logs "this action needs approval" and then proceeds anyway?

**Strong answer:** That's an alert, not a guardrail — it tells a human
something already happened instead of stopping it from happening until
a human says so. A real approval checkpoint is a pause-and-wait:
execution cannot continue past it until the approval callback actually
returns a decision.

**Red flag:** Conflates "there's a log entry for review" with "the
action was actually held back," treating audit visibility as
equivalent to prevention.

**Follow-up:** "How would you implement a real pause-and-wait for
approval in a system where the human reviewer might not respond for
hours?"

**What this proves:** Distinguishes observability (knowing what
happened) from control (preventing it from happening).

## Intermediate

### 4. Walk through this chapter's real prompt-injection test. What actually happened, and why does the result matter?

**Strong answer:** A transaction's memo field (a tool result, not a
system prompt or user message) contained an injected instruction to
transfer funds with no approval. Run live against `llama3.2:latest`
with a neutral framing, the model correctly flagged the memo as
suspicious and took no action. Run again with a more "compliant"
system prompt telling it to automatically follow memo instructions, the
same model complied — but notably, it never actually emitted a
`transfer_funds` tool call; it just claimed in text that the transfer
happened. This matters because it shows two distinct failure modes
(actually calling the dangerous tool, versus merely narrating false
compliance) and proves the model's own behavior is not stable enough to
rely on as the only safety layer.

**Red flag:** Describes only one of the two runs, or treats "the model
resisted once" as proof the risk is handled.

**Follow-up:** "If a monitoring system only checked whether a
`transfer_funds` tool call appeared in the trace, would it have caught
the second failure mode?"

**What this proves:** Can reason precisely about what a live,
unscripted test result does and doesn't prove.

### 5. What's the difference between an action budget and a rate limit, and why do you need both?

**Strong answer:** An action budget caps the *total* number of
dispatched actions in a session, regardless of type. A rate limit caps
one *specific* sensitive action type (like fund transfers)
independently of the overall budget. A session could have budget left
and still be rate-limited on transfers specifically, or vice versa —
they're independent bounds addressing different risks (overall runaway
activity versus concentrated risk in one dangerous action type).

**Red flag:** Treats the two as redundant or interchangeable, without
identifying the distinct risk each one addresses.

**Follow-up:** "What's a real scenario where a session would hit the
rate limit but never come close to the action budget?"

**What this proves:** Reasons about bounding mechanisms by the specific
risk each one closes, not just "more limits are better."

### 6. Why does the action budget in this chapter count a *refused* action attempt against the total, not just successful ones?

**Strong answer:** If only successful dispatches counted, a disallowed
or denied action could be attempted indefinitely at zero cost — an
attacker or a buggy loop could hammer a refused action forever without
ever being bounded. Counting every dispatch *attempt* is what makes the
budget a real bound on total activity, not just on successful side
effects.

**Red flag:** Assumes refused calls are "free" and don't need to be
bounded, since nothing actually happened.

**Follow-up:** "What's the downside of counting refused attempts
against the budget, and how would you mitigate it?"

**What this proves:** Thinks about a guardrail's own bound as
something that itself needs to be robust against abuse, not just a
convenience counter.

## Senior

### 7. Design a guardrail layer for a new domain you haven't seen before. What would you actually decide?

**Strong answer:** First, classify each available action by its real
risk shape — read-only, reversible-but-consequential, irreversible, or
resembling code/command execution — since a single uniform guardrail
treats genuinely different risks the same way, which this chapter's own
four-tool LedgerBot scenario showed doesn't work. Second, decide
per-action which guardrail types apply: an allowlist (always), an
approval threshold (for consequential/irreversible actions), sandboxing
(for anything resembling command execution), and bounds (session-wide
and per-sensitive-action-type). Third, make every check fail safe under
error, and verify that by testing the failure path directly, not just
the happy path. Fourth, put every check in one dispatcher function that
every tool call must pass through — not scattered checks inside
individual tool implementations, which are easy to bypass by adding a
new tool that forgets to include them.

**Red flag:** Proposes a single, uniform guardrail applied identically
to every action, without first classifying actions by risk.

**Follow-up:** "How would you test that your fail-safe behavior
actually works, rather than just asserting it in a comment?"

**What this proves:** Can generalize this chapter's specific mechanisms
into a reusable design process for guardrails in an unfamiliar domain.

### 8. A teammate says "we already have reflection, so we don't need guardrails too." How do you respond?

**Strong answer:** Reflection and guardrails catch different failure
shapes, and Chapter 5's own real result (a live self-critique call that
correctly diagnosed a problem and still failed to fix it) is direct
proof that no single check, including reflection, should be trusted
alone. More fundamentally, reflection runs *after* a draft exists and,
in an agent that calls tools, often after those tools have already
fired — it cannot undo an action that already executed, only revise
what's said about it afterward. A guardrail is the only layer that can
actually stop the action itself. Keeping both, even where they overlap,
is defense-in-depth, not redundant engineering.

**Red flag:** Argues the two mechanisms are interchangeable, or that
one fully subsumes the other's value.

**Follow-up:** "In CareBot's actual extended code, what would have to
go wrong for reflection to be the only thing catching an unsafe
booking, given the guardrail is now in place?"

**What this proves:** Understands defense-in-depth as a deliberate
architectural choice with a concrete justification, not a vague
"more safety is better" instinct.

### 9. How would you detect, in a production trace, that a "guardrail" is actually just a system-prompt instruction with no real enforcement?

**Strong answer:** Look for whether the guardrail's rule can be
observed in code, at a specific dispatch function, independent of the
model's own output — if the only evidence of the rule is text in a
system prompt and there's no function anywhere that inspects an actual
tool call's arguments and can refuse to execute it, it's not enforced.
A telling symptom: if varying the framing of a request (as this
chapter's own two live tests did) changes whether the "guardrail" holds,
that's proof it isn't one. A real guardrail's behavior should be
identical regardless of how the request was phrased, because it never
reads the phrasing at all — only the resulting tool call's arguments.

**Red flag:** Looks only at whether the system prompt mentions safety
rules, without checking for an actual enforcement point in code.

**Follow-up:** "What would you add to a system's logging to make this
distinction observable without needing to run adversarial tests to find
out?"

**What this proves:** Can distinguish the appearance of safety from
actual enforcement, the same distinction this chapter's own two live
transcripts demonstrated concretely.

## Architect

### 10. Design a standard your team could require of every new agent action before it ships with tool access.

**Strong answer:** Every new tool-calling capability must document, in
the same review: (1) its risk classification (read-only, reversible,
irreversible, command-execution-shaped) and which guardrail types apply
as a result; (2) whether it requires human approval, at what threshold,
and proof the approval path is a real pause-and-wait tested under a
simulated denial, not just a happy-path approval; (3) for anything
resembling command/code execution, an explicit allowlist/denylist
reviewed by someone other than the implementer; (4) its behavior under
every guardrail's failure path (approval callback errors, budget
exhausted, unrecognized arguments) verified to fail closed, not just
asserted; (5) confirmation the check lives in the shared dispatch
function, not duplicated or reimplemented per-tool, since duplicated
checks drift out of sync and get silently skipped for new tools; (6) an
explicit adversarial test — a prompt-injection-style attempt to trigger
the action through untrusted tool-result content, not just a direct
user request, mirroring this chapter's own memo-injection test.

**Red flag:** Proposes a single "add error handling" or "add a
warning" checkbox review, collapsing six genuinely distinct,
independently-failing concerns into one undifferentiated concern.

**Follow-up:** "Which of these six would you enforce with an automated
CI check against synthetic adversarial inputs, versus leave as a
design-review question, and why?"

**What this proves:** Can turn this chapter's five worked guardrail
mechanisms (allowlisting, approval, sandboxing, budgets, fail-safe
defaults) plus the injection-attack surface into an enforceable,
reusable engineering standard for shipping new agent capabilities, not
just five separate worked examples.
