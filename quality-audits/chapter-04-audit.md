# Chapter 4 Quality Audit: Memory and State

Session date: 2026-09-28. This session built Chapter 4 in full, cold,
from `PROJECT_STATE.md`'s "Next Recommended Task" brief: `lesson.html`,
`quiz.html`, `interview-questions.html` + `.md`, the full `exercises/`
and `practice/` sets, the entire `project/` folder (this chapter's
**L2 Assisted** project, per the curriculum map's project ladder), this
audit, wiring `assets/chapters-data.js` and `docs/curriculum/index.html`,
updating root `index.html`'s hero stats, and rewriting
`PROJECT_STATE.md`'s "Next Recommended Task" for Chapter 5. The build
was interrupted once by the parent session ending before a commit
landed; it was resumed in a second pass that verified every file
already on disk (rather than rewriting anything already complete and
correct) and built only what was still missing (`practice/index.html`,
`practice/ai-paired.html`, and the entire `project/` HTML/Markdown set
— `starter.py`/`solution.py` for the project already existed and were
re-verified, not rebuilt).

## Honest self-critique

**What's strong:**
- Unlike Chapter 3, **this session's live Ollama calls actually
  succeeded** — the model was explicitly pre-warmed
  (`keep_alive: "120m"`) before any lesson code was written, and every
  live call in the lesson (Section 2's sanity check, Section 6's
  promote-worthy classification, Section 8's grounded-vs-ungrounded
  reply contrast, Section 12's summarization call) is a **real,
  captured transcript**, not a deterministic stand-in disclosed as a
  fallback. Section 8 in particular is a genuinely useful real result:
  the identical prompt, with and without persisted facts injected as
  context, produces two materially different real model outputs,
  proving the personalization comes from the memory mechanism and not
  from the model itself.
- The lesson goes deep on exactly what the brief specified: the
  short-term/long-term split (Sections 1, 3-5), what to promote vs.
  forget (Section 6, live-tested), token-budget pressure and pruning
  (Sections 11-12), and — beyond the brief's minimum — a genuine
  read-modify-write bug (Section 9) caught by testing, a stale-snapshot
  bug caught in the finished agent (Section 15), and a corrections/
  supersede treatment (Section 10) the brief didn't explicitly ask for
  but that fell out naturally from testing the read-modify-write fix
  against a realistic "the injury is resolved now" case.
- Every single code example in the lesson was actually run before
  being written into `lesson.html` — see "Code tested before writing"
  below for the full list of scratch files executed, including the two
  process-separated files (`session1.py`, `session2.py`) run as two
  genuinely separate `python3` invocations to prove real
  cross-process persistence, not just a variable surviving inside one
  script.
- A real bug was caught and fixed during testing, not manufactured:
  a first draft of `remember_preference` built a brand-new facts dict
  from scratch instead of loading the member's existing facts first,
  silently deleting an already-persisted injury note the moment a
  second fact was promoted for the same member. The fix (Section 10,
  read-modify-write) is the same "an unscripted failure surfaced by
  testing became the lesson's own honest example" pattern Chapter 1's
  Cedar Hollow bug and Chapter 3's retry-timeout bug both used. A
  second, related bug (a stale-snapshot variable used to decide
  Session 1's own reply) was caught the same way while building
  Section 15's finished agent.
- Lesson density: 62 lines match `<pre\|<code` via
  `grep -c '<pre\|<code' lesson.html` (above the 60+ requirement, and
  close to Chapter 1's 61), or 114 total tag occurrences via
  `grep -oE '<pre|<code' | wc -l`.
- This session verified every `solution.py` across `exercises/`,
  `practice/`, and `project/` scores a perfect total, and every
  corresponding `starter.py` fails cleanly (low score, no crash) with
  its `TODO`s unfilled — all six files actually executed this session,
  not assumed, both in the original pass and re-verified after the
  session resumed from an interruption.
- **This chapter's `project/` folder is explicitly the course's
  numbered L2 Assisted project**, not a chapter mini-project — the
  curriculum map's own wording for Chapter 4 ("ships after Ch. 4,
  extended through Ch. 5-6's reflection/guardrail material") is
  different from Chapters 2-3's wording, and this session read that
  distinction before building rather than defaulting to the
  mini-project pattern silently. The reflection half of the L2
  description is a clearly labeled no-op passthrough
  (`reflect_on_response()`), wired into the call path exactly where
  Chapter 5 will replace its body — documented explicitly in
  `project/README.md`'s own "What Chapter 5 will do with this file"
  section, which is the concrete answer to the brief's requirement to
  state which of the two options (real scaffold vs. mini-project) was
  chosen and why.

**Honest gaps:**
- This chapter's own live-model success does not mean the sandbox's
  documented intermittent hang is resolved — it means this session's
  specific pre-warm discipline worked this specific time. Future
  chapters should still budget up to 450 seconds per call and disclose
  honestly if a hang recurs, exactly as Chapter 3 did.
- Only `llama3.2:latest` was ever targeted (the one model available in
  this sandbox), consistent with Chapters 1-3 — no claim is made that
  any described model behavior (including the promote-worthy
  classification or the grounded-reply contrast) generalizes beyond
  what was actually, live-demonstrated.
- The persisted-memory store's correction/supersede handling (Section
  10) is deliberately kept simple (a `RESOLVED:` string prefix, not a
  structured status field) — the lesson says explicitly this is a
  choice not to over-engineer a subproblem outside this chapter's own
  scope, not a claim that it's production-ready as shown.
- Exercises/practice/project scoring for free-text-style answers still
  relies on exact-string or keyword matching rather than fully semantic
  grading — the same necessary, disclosed limitation as every prior
  chapter's own exercise harness.
- The project's grading (7 structural self-checks against deterministic
  fixtures, no live model call) is a design choice for gradability, the
  same disclosed approach every prior chapter's project used, not a
  claim that it exercises a live model's actual non-determinism.
  `project/README.md` gives the live-Ollama swap pattern explicitly,
  pointing to the lesson's own Section 8 as the exact working pattern.
- This session was interrupted once (the parent session ended before a
  commit landed) and resumed cold in a second pass. The resumed pass
  verified `lesson.html`'s well-formedness (balanced `<section>`/`<div>`
  tags, ends in `</html>`) and re-ran every solution/starter pair before
  trusting any of it, rather than assuming the prior pass's work was
  correct — this is disclosed here rather than silently treated as a
  non-event.

## Fictional-org exclusion check

Extending, not restarting, the list from `chapter-03-audit.md` (12
orgs: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol,
Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty Group,
Thistlewood Veterinary Group, Cobblestone Courier Co., Palisade
Broadband, Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel
Appliance Service).

**4 new fictional orgs used in this chapter, all checked clean against
the full running list and against each other:**

- **Larkspur Fitness Studio** (lesson hook; product: CoachBot)
- **Driftwood Legal Clinic** (exercises; product: IntakeBot)
- **Saltmarsh Language Academy** (exercises `ai-paired.html`; product:
  TutorBot)
- **Hollowridge Wellness Clinic** (project; product: CareBot)

**MemoBot's productivity app** (practice `ai-paired.html`) is left
unnamed/generic on purpose, the same convention Chapter 3's HandoffBot
scenario (and Chapter 1's ConciergeBot, Chapter 2's EscalationBot)
used — a small, two-or-three-fact scenario doesn't need an invented
company name.

Every distinctive root word above (Larkspur, Driftwood, Saltmarsh,
Hollowridge) was checked for zero overlap against both this chapter's
own four named scenarios and the full 12-org Chapter 1-3 list
(Northbeam, Summit Gear, Fernbrook, Wavecrest, Alderleaf, Pinehurst,
Thistlewood, Cobblestone, Palisade, Thornbury, Wrenhollow, Kestrel).
The running exclusion list for future chapters is now: Northbeam
Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol, Wavecrest Marina,
Alderleaf Research Group, Pinehurst Realty Group, Thistlewood
Veterinary Group, Cobblestone Courier Co., Palisade Broadband,
Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel Appliance
Service, Larkspur Fitness Studio, Driftwood Legal Clinic, Saltmarsh
Language Academy, Hollowridge Wellness Clinic. Future chapters should
extend this list, not restart it.

## Source verification, done honestly

Like Chapters 1-3, this is a from-scratch code walkthrough, not a
claims-and-citations chapter — no external papers or docs required
WebFetch verification. This chapter's one general-convention claim
(characters-divided-by-4 as a rough token estimate, Section 11) is
presented explicitly as a common approximation, not a precise
tokenizer claim, and the lesson says directly that exact tokenizer
accounting is Chapter 8's subject, not asserted as a sourced external
fact here. No other external source claims are made this chapter.

## Ollama check, done fresh this session

Unlike Chapter 3, this session's live calls succeeded. The model was
explicitly pre-warmed before any lesson code was written:

```
$ curl -s localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"","keep_alive":"120m"}'
{"model":"llama3.2","created_at":"2026-09-28T11:47:49Z","response":"","done":true,"done_reason":"load"}

$ python3 check_ollama.py   # plain "Say OK" sanity check
elapsed: 2.226099
OK. Is there something I can help you with?
```

Every subsequent live call in the lesson (Sections 6, 8, 12) carried
`extra_body={"keep_alive": "120m"}` and completed well inside this
course's documented 450-second ceiling (the slowest single call,
Section 12's summarization, took 23.19 seconds; a cold-load outlier
during the promote-worthy classification took 9.51 seconds on its
first call). On resuming this session after an interruption, Ollama
was re-warmed again with the same command before re-verifying any
Python files, per this course's reliability policy of never assuming a
prior session's warm state persists.

## Code tested before writing

Every Python file this session wrote was actually run, in a scratch
directory, before its content was transcribed into `lesson.html`:

```
$ python3 tools.py                -> CoachBot's three tools verified against real fixtures
$ python3 memory_store.py         -> load/save/remember_injury round trip verified
$ python3 session1.py             -> run as a real, separate python3 process
$ python3 session2.py             -> run as a SECOND real, separate python3 process,
                                      after session1.py fully exited, proving genuine
                                      cross-process persistence
$ python3 naive_no_memory.py      -> the no-persisted-store failure baseline verified
$ python3 promote_check.py        -> live Ollama classification, 4/4 correct, captured
$ python3 token_pressure.py       -> running token-estimate growth over 12 real turns
$ python3 prune_summarize.py      -> live Ollama summarization call, captured, and the
                                      real detail-loss observation that became Section 14
$ python3 overwrite_bug.py        -> the blind-overwrite bug reproduced for real
$ python3 overwrite_fix.py        -> the read-modify-write fix verified, plus the
                                      no-prior-file edge case
$ python3 correction.py           -> the append-only correction failure and the
                                      resolve_injury fix, both verified
$ python3 extra_sections.py       -> PR tracking, key-lookup isolation across two real
                                      members, the prune-safety guard, and a second live
                                      Ollama call (the memory-grounded reply) all verified
$ python3 coachbot_agent.py       -> the finished agent, both sessions verified end to
                                      end -- this file's first version used a stale
                                      `facts` snapshot for Session 1's own reply, caught
                                      and fixed (re-fetch after write) before being
                                      written into the lesson
```

Then, in the actual chapter directory, after every file was written
(re-verified again after this session's own interruption and resume):

```
$ python3 exercises/solution.py   -> TOTAL: 16/16
$ python3 exercises/starter.py    -> TOTAL: 3/16, no crash
$ python3 practice/solution.py    -> TOTAL: 8/8
$ python3 practice/starter.py     -> TOTAL: 0/8, no crash
$ python3 project/solution.py     -> 7/7 checks passed
$ python3 project/starter.py      -> 2/7 checks passed, no crash
```

No stray JSON files were left behind in the chapter directory by any
of the `exercises/`, `practice/`, or `project/` runs (each script
cleans up its own test fixtures on exit).

## Local check

`scripts/local_check.sh` was run for the whole repo after all Chapter
4 files were in place — see `PROJECT_STATE.md`'s Session 4 entry for
the result captured this session.
