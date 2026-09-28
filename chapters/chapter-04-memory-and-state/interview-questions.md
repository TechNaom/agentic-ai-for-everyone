# Chapter 4 Interview Questions: Memory and State

Grouped by level — beginner, intermediate, senior, architect. Each
includes a strong answer, a red flag, a follow-up, and what the
question actually proves.

## Beginner

### 1. What's the difference between working memory and persisted memory?

**Strong answer:** Working memory is the message list (conversation
history, tool results) that lives inside one run of the agent loop —
exactly what Chapters 1-3's `messages` list already was. It exists only
as long as the process is alive and is gone the moment it exits.
Persisted memory is a deliberately small set of facts written to
storage (a file, a database) that survives past process exit and can
be correctly loaded back into a completely separate, later run.

**Red flag:** Describes persisted memory as "just a bigger working
memory" or conflates the two, missing that they have fundamentally
different lifetimes and different content (persisted memory should
hold far less than a full transcript).

**Follow-up:** "If an agent only has working memory and no persisted
store, what specifically breaks?"

**What this proves:** Understands the core lifetime distinction this
chapter's entire architecture is built on.

### 2. Why does this chapter's persisted store use a plain JSON file instead of a vector database?

**Strong answer:** The architectural problem this chapter solves —
does a fact survive past this process, and does writing it correctly
merge with what's already there — has nothing to do with retrieval
quality or semantic search. A plain key-value lookup, keyed on a user
ID, is the entire mechanism needed. Vector databases and embeddings
solve a different problem (finding semantically similar content across
a large, unstructured corpus), which this course explicitly defers to
`context-engineering-for-everyone`.

**Red flag:** Assumes any "memory" system automatically needs
embeddings or a vector store, without being able to say what problem
those specifically solve that a key lookup doesn't.

**Follow-up:** "At what point would this system's needs outgrow a
plain key-value store?"

**What this proves:** Doesn't reach for a more complex tool than the
actual problem requires.

### 3. What is a "promote-worthy" fact, and why doesn't every message qualify?

**Strong answer:** A promote-worthy fact is something that should
change future behavior — an injury, a lasting preference, a schedule
constraint. Most messages (routine questions, acknowledgments, small
talk) don't qualify. Persisting everything would work mechanically but
fills the long-term store with noise that dilutes the facts that
actually matter, and makes future retrieval less useful, not more.

**Red flag:** Argues it's simpler and safer to just persist every
message "in case it's needed later," without weighing the real cost
of a noisy, undifferentiated store.

**Follow-up:** "What would you check to decide if a given message is
promote-worthy?"

**What this proves:** Recognizes that memory design includes a
filtering decision, not just a storage mechanism.

## Intermediate

### 4. Walk through the "blind overwrite" bug this chapter's own testing caught. Why did it happen, and what specifically fixed it?

**Strong answer:** A first draft of a fact-promotion function built a
brand-new facts dict from scratch on every call (`{"injuries": [],
"preferences": [pref_text], ...}`) instead of loading the member's
existing facts first. The bug was invisible on a member's very first
promoted fact, and only appeared the second time a fact was promoted
for the same member — the new write silently erased everything
persisted before it. The fix is read-modify-write: load existing
facts, merge the new one in, then save.

**Red flag:** Describes the bug only as "forgetting to save," rather
than correctly identifying that data was actively destroyed by a
write that never read first.

**Follow-up:** "Why would this bug pass a demo that only tests one
fact being persisted, but fail in real repeat usage?"

**What this proves:** Can trace a subtle persistence bug to its exact
mechanical cause, not just its symptom.

### 5. Why is summarization not a substitute for persisting a fact, even though both seem to "preserve information"?

**Strong answer:** They solve different problems with different
failure modes. Summarization keeps a working-memory buffer under a
token budget while staying coherent for recent turns — but the
summarizer has no way to know which specific detail a future,
separate system actually needs to keep forever, so it can (and, in
this chapter's own real test, did) drop something important.
Persisting is a deliberate, specific choice to keep one fact correct
and available indefinitely. Relying on summarization alone to
preserve a durable fact means that fact's survival depends on the
summarizer's judgment on every single pass, forever.

**Red flag:** Treats summarization as a reliable way to "compress but
keep everything important," without acknowledging it can silently
drop specific details.

**Follow-up:** "What ordering rule prevents this specific failure?"

**What this proves:** Distinguishes two memory mechanisms that look
similar on the surface but serve genuinely different purposes.

### 6. What ordering rule connects promotion (deciding what to persist) and pruning (shrinking working memory)?

**Strong answer:** Promote-worthy facts must be written to the
persisted store *before* the working-memory turns that stated them
are ever pruned or summarized away. If pruning happens first, and the
fact was never promoted, it's lost permanently the moment those turns
are dropped or summarized — this chapter's practice bank calls this
"prune-before-promote," and it's a real, demonstrable risk, not a
hypothetical one.

**Red flag:** Doesn't see a dependency between the two mechanisms at
all, treating promotion and pruning as unrelated, independently
schedulable steps.

**Follow-up:** "How would you enforce this ordering in code, rather
than just documenting it as a rule?"

**What this proves:** Sees the dependency between two mechanisms that
are easy to design independently and get subtly wrong together.

## Senior

### 7. Design the data model for a persisted memory store for a new domain you haven't seen before. What would you actually decide?

**Strong answer:** First, what's the natural key (a user/account/
member ID) that guarantees isolation between different users' facts —
this chapter proved that isolation directly with two real members on
file at once. Second, what categories of fact this domain actually
needs (this chapter used injuries, preferences, and PRs; a different
domain would need its own categories) rather than one undifferentiated
list. Third, for each write path, confirm it loads existing state
before writing (read-modify-write), or a second write for the same
user will silently destroy the first. Fourth, decide explicitly
whether facts can be superseded/corrected, not just appended to
indefinitely — an injury that gets resolved needs a different handling
path than one that's still active.

**Red flag:** Jumps straight to schema/table design without addressing
the isolation, categorization, and read-before-write questions first.

**Follow-up:** "How would corrections/contradictions to an existing
fact be handled in your design?"

**What this proves:** Can generalize this chapter's specific mechanisms
into a reusable design process for memory in an unfamiliar domain.

### 8. A teammate proposes persisting the entire conversation transcript of every session, "just in case." What's the actual cost of this, beyond storage size?

**Strong answer:** Beyond raw storage growth, the real cost is at
retrieval time: every future session that loads this member's memory
now has to sift a growing, mostly-irrelevant transcript to find the
few facts that actually matter, defeating the purpose of a fast,
reliable working-context merge (this chapter's Section 5/15 pattern).
It also makes the promote-worthy filter pointless, since the filter
exists specifically to keep the store small and high-signal. A full
transcript archive might be a legitimate *separate* system (for
compliance or analytics), but it's the wrong shape for the memory this
chapter's agent actually needs to load and act on every session.

**Red flag:** Only raises storage cost as the concern, missing the
retrieval-quality and context-merge cost, which matters more for an
agent's actual behavior.

**Follow-up:** "If full-transcript archival is genuinely needed for
compliance, how would you keep it separate from the fast-path memory
store this chapter built?"

**What this proves:** Distinguishes storage cost from retrieval/design
cost, and can propose keeping two systems' concerns properly separated.

### 9. How would you detect, in a production trace, that an agent's memory system has a "stale snapshot" bug like the one this chapter's own finished agent first had?

**Strong answer:** Look for a session where a promote-worthy fact was
stated and correctly written to the persisted store, but the agent's
*own reply, in that same turn*, doesn't reflect it — while a
*following* session correctly does. That split (wrong within-session
behavior, correct next-session behavior) is the signature: it proves
the write succeeded (next session sees it) but something mid-session
used a variable captured before the write instead of re-checking the
store after it.

**Red flag:** Looks only for missing writes to the store, missing that
this specific bug is about *reading* stale local state, not about
persistence failing.

**Follow-up:** "Why does this bug specifically NOT show up if you only
test across separate sessions, and only appears if you test within
one session that both learns and acts on a fact?"

**What this proves:** Can reason about a subtle class of bug from its
observable symptom pattern, not just its code-level cause.

## Architect

### 10. Design a standard your team could require of every new agent's memory system before it ships.

**Strong answer:** Every new memory system must state, in the same
review: (1) what qualifies as promote-worthy for this domain, with a
named filter (live-tested or deterministic) rather than "persist
everything" or an undocumented ad hoc judgment call; (2) confirmation
every write path is read-modify-write, with a test that specifically
exercises a *second* write for the same key, since the blind-overwrite
bug is invisible on a first write; (3) an explicit ordering guarantee
that promotion happens before any pruning/summarization that could
discard the same content, with a test that would fail if that ordering
were reversed; (4) a stated policy for corrections/contradictions to
existing facts (supersede vs. append), since this chapter showed
appending alone silently produces a store where the current state of
the world isn't the same as what's recorded; (5) explicit key-based
isolation between users, with a test proving one user's facts never
appear in another's retrieved context.

**Red flag:** Proposes a single "make sure memory works" checkbox
review, collapsing five genuinely distinct, independently-failing
concerns back into one undifferentiated concern.

**Follow-up:** "Which of these five would you automate as a CI check,
versus leave as a design-review question, and why?"

**What this proves:** Can turn this chapter's five worked mechanisms
(promotion filtering, read-modify-write, promote-before-prune
ordering, corrections, key isolation) into an enforceable, reusable
engineering standard, not just five separate worked examples.
