# Chapter 1 Interview Questions: The Agent Loop

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. What's the difference between "calling an LLM" and "running an agent"?

**Strong answer:** Calling an LLM is a single request/response — you
send a prompt, you get text back, done. An agent runs a loop where the
model's own output (does it want to call a tool, or is it done?)
decides whether another iteration happens. The calling code doesn't
decide how many steps the task takes — the model does, one decision at
a time, based on what it observed from its previous actions.

**Red flag:** Says "an agent just uses a bigger/smarter model" without
mentioning the loop or the model's role in deciding when to stop.

**Follow-up:** "If I call an LLM three times in a fixed sequence inside
my own code, is that an agent?"

**What this proves:** Understands the structural definition of an agent
rather than a vibes-based one ("it feels autonomous").

### 2. In the lesson's bare_call.py example, why did the model refuse to answer instead of just making something up?

**Strong answer:** The model had no way to check Eagle Ridge's actual
trail status — no tool, no data source, nothing but the prompt text.
Refusing was the model behaving correctly given what it had access to;
the real problem was architectural (no action or observation step
existed at all), not that the model needed better instructions.

**Red flag:** Blames the prompt ("it just needed a better system
message") instead of recognizing the missing loop machinery.

**Follow-up:** "What's the minimum you'd add to this code, not the
prompt, to make a real answer possible?"

**What this proves:** Separates a prompting problem from an
architecture problem.

### 3. What are the four steps of the agent loop, and give a one-sentence example of each from TrailBot?

**Strong answer:** Perception (the user's question, or a tool's
result, entering the message history) — "is Eagle Ridge open?" Reasoning
(the model deciding what to do with what it knows) — deciding to call
get_trail_status. Action (actually doing it) — the function executing
for real against TRAIL_STATUS. Observation (the result becoming new
information) — the dict {"status": "open", ...} appended as a
role:"tool" message.

**Red flag:** Can recite the four words but can't map them onto actual
code from the lesson.

**Follow-up:** "Which step is missing in a single LLM call with no
tools?"

**What this proves:** The mental model is concrete, not just memorized
vocabulary.

## Intermediate

### 4. Walk through exactly what happens, message by message, when TrailBot answers a two-tool question.

**Strong answer:** messages starts with system + user. Turn 1: the
model returns tool_calls for both get_trail_status and get_weather (no
content); both get appended, then both tool results get appended as
separate role:"tool" messages. Turn 2: the model, now seeing both
observations in its context, returns content with no tool_calls — the
loop sees that and stops, returning the content as the final answer.

**Red flag:** Describes it as "the model calls the functions" — the
model never executes anything; it only requests a call, which the
calling code executes.

**Follow-up:** "What would messages look like if the second tool call
had also failed?"

**What this proves:** Understands who does what — model requests,
calling code executes — a distinction beginners often blur.

### 5. What is a wrong-argument failure, and how is it different from the model choosing the wrong tool?

**Strong answer:** A wrong-argument failure is when the model picks the
*correct* tool but the argument value doesn't match your data exactly
— like passing "Cedar Hollow trail" when the lookup key is "cedar
hollow". A wrong-tool-choice failure is picking get_weather when the
user actually needed get_trail_status. They need different fixes:
argument mismatches get fixed by making the tool tolerant of realistic
input variation; tool-choice failures get fixed by improving the
tool's description or the system prompt.

**Red flag:** Treats any tool-calling failure as "the model got it
wrong" without distinguishing which part was wrong.

**Follow-up:** "Where in the code did the lesson fix the Cedar Hollow
bug, and why there and not in the prompt?"

**What this proves:** Can diagnose an agent failure precisely enough to
apply the correct, narrow fix instead of a broad one.

### 6. Why does the tool-result message need a tool_call_id, and what would break without it?

**Strong answer:** A single reasoning turn can request multiple tool
calls at once. tool_call_id is how each returned result gets matched
back to the specific call that asked for it. Without it, the model
(and the API's own validation) has no way to know which observation
answers which question when more than one tool was called in the same
turn — a real failure mode once an agent uses more than one tool per
step, which Chapter 1's own two-tool example already does.

**Red flag:** Assumes tool results are matched by position/order alone
and doesn't realize order isn't guaranteed or checked.

**Follow-up:** "What happens if you send a tool_call_id that doesn't
match any pending tool call?"

**What this proves:** Understands the actual protocol mechanics, not
just the high-level flow.

## Senior

### 7. A teammate wants to remove `max_iterations` because "the model always stops on its own anyway." How do you respond?

**Strong answer:** "Always" isn't true and isn't verifiable in advance
— models occasionally get stuck re-requesting the same or similar tool
call, especially smaller local models, and there's no way to prove in
general that a given prompt/tool combination will always terminate.
Without a hard cap, that failure mode becomes an unbounded loop: every
iteration is another model call (cost, Chapter 8's subject) and, if a
tool has side effects, every iteration could repeat that side effect.
The guard costs nothing when the agent would have stopped anyway, and
prevents a real, low-probability-but-nonzero failure when it wouldn't
have.

**Red flag:** Agrees to remove it because "it hasn't happened in
testing yet."

**Follow-up:** "Is a high enough max_iterations basically the same as
no guard at all?"

**What this proves:** Treats reliability engineering as designing for
the failure that hasn't happened yet, not just the one that has.

### 8. max_iterations stops a runaway loop. What does it *not* protect against, and what would?

**Strong answer:** It guarantees the loop eventually halts — it does
not guarantee any action taken during those iterations was safe. If
one of the tool calls before the cap was reached had a real side
effect (sending an email, charging a card, deleting a file), that
already happened; the guard didn't and couldn't undo it. What's needed
beyond it: guardrails scoped to the action itself — human-approval
checkpoints before destructive actions, sandboxing so a tool's blast
radius is contained, and rate limits independent of the iteration
count. This is Chapter 6's subject, and this chapter's guard is
explicitly named as only the first layer.

**Red flag:** Claims max_iterations alone makes an agent "safe."

**Follow-up:** "Design one guardrail that would still be needed even
with a very low max_iterations."

**What this proves:** Separates "the loop terminates" from "the system
is safe," a distinction that matters a lot once tools have real-world
side effects.

### 9. This sandbox's Ollama install hung for 432 seconds once. How should a production agent handle a reasoning step that just doesn't return?

**Strong answer:** Every call needs an explicit timeout, not an
indefinite wait — the lesson's call_with_budget wrapper is a minimal
version of this. Beyond the timeout itself, the agent needs a defined
fallback for what "no answer in time" means for that specific step:
retry once with backoff, degrade to a cached or simpler answer, or
surface a clear, bounded error to whatever's waiting on the agent
(a user, an upstream service, a queue). What it should never do is
block the whole system indefinitely on one slow call, especially inside
a loop that might be making several calls per task.

**Red flag:** Treats "the API hung" as purely an infrastructure problem
to escalate, with no code-level mitigation.

**Follow-up:** "Should the timeout budget be the same for every step in
a multi-step agent, or does it depend on the step?"

**What this proves:** Thinks about latency and failure handling as part
of agent *design*, not just deployment ops.

## Architect

### 10. You're advising a team building their first production agent. They ask: "should we use a framework like LangGraph, or build the loop ourselves like this chapter did?" What's your answer?

**Strong answer:** It depends on what they need to be true six months
from now, not on what's fastest to demo this week. Building it
themselves (or at least understanding this chapter's four-ingredient
version deeply) buys full visibility into every failure mode — when
something breaks, they're debugging their own code, not framework
internals. A framework buys velocity on standard patterns (state
persistence, multi-agent handoffs, built-in retries) once the team
already understands what those patterns are doing underneath, which is
exactly why this course teaches the from-scratch version first. The
real anti-pattern is reaching for a framework *before* understanding
the loop it's implementing — that's how "the framework did something
weird" becomes undebuggable.

**Red flag:** Gives a one-word answer ("always frameworks" or "never
frameworks") without connecting it to what the team actually needs to
debug or extend later.

**Follow-up:** "What's one thing a framework like LangGraph gives you
that would be genuinely painful to hand-roll at scale?"

**What this proves:** Can reason about a real build-vs-adopt trade-off
instead of having a fixed opinion, and ties the decision back to this
chapter's own pedagogical choice.
