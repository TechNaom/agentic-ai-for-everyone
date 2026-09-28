# Chapter 4 Exercises: Memory and State

These exercises use a second scenario, deliberately different from the
lesson's Larkspur Fitness Studio/CoachBot hook: **Driftwood Legal
Clinic**, a fictional legal-aid clinic. Its intake agent, **IntakeBot**,
handles a separate phone/chat session for each client visit, and needs
to remember accessibility accommodations and scheduling preferences a
client states in ONE visit so a receptionist booking a follow-up
hearing weeks later automatically gets it right — without a vector
database or embedding framework, per this chapter's own scope.
Applying this chapter's memory concepts to a fresh scenario is the
point — recalling the lesson's answers by heart won't get you through
these.

## How to run

You'll need Python 3 installed. Check with:

```bash
python3 --version
```

Then run the starter file:

```bash
python3 starter.py
```

It prints a score report. Fill in each `# TODO`, re-run, and watch your
score climb toward the total (16 points across 8 tasks).

## The eight tasks

1. **Map facts to memory concepts** — assign the correct concept
   (short-term working memory, long-term persisted memory, token-budget
   pruning, promote-worthy fact detection, read-modify-write merge bug)
   to five IntakeBot facts.
2. **Dependency reasoning** — decide whether pruning working memory
   before a fact is ever persisted makes permanently losing that fact
   more or less likely.
3. **(Production-gear) Promote-worthy classifier** — distinguish an
   accessibility accommodation or scheduling preference from routine
   chat.
4. **(Production-gear) Read-modify-write add function** — fix the
   blind-overwrite bug, don't repeat it.
5. **(Production-gear) Merge into a fresh working context** — retrieve
   persisted facts and correctly inject them as context.
6. **(Production-gear) Diagnose a failure type** — read a real trace
   and correctly name a read-modify-write merge bug.
7. **(Production-gear) Promote-before-prune** — ensure a promote-worthy
   fact survives even after the working-memory turns that stated it are
   gone.
8. **Completeness check** — confirm all five memory concepts were
   actually used.

## Files

- `starter.py` — the scaffold with 11 `# TODO`s and the score report.
- `solution.py` — the fully filled-in reference; scores 16/16.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-diagnosis-then-critique exercise using a
  third scenario.
