# Chapter 3 Exercises: Tool Use and Function Calling

These exercises use a second scenario, deliberately different from the
lesson's Palisade Broadband/NetBot hook: **Thornbury Insurance Group**,
a fictional auto insurer. Its agent, **ClaimBot**, has four tools that
plausibly overlap in what they could explain about a slow claim — a
lapsed policy, a repair-shop delay, or missing adjuster notes — and one
tool (`send_status_update`) that always "succeeds" without that meaning
the claim is actually resolved. Applying this chapter's tool-use
concepts to a fresh scenario is the point — recalling the lesson's
answers by heart won't get you through these.

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

1. **Map facts to tool-failure concepts** — assign the correct concept
   (wrong-tool-choice, argument-formatting drift, timeout failure,
   malformed-output failure, succeeds-but-wrong-answer failure) to five
   ClaimBot facts.
2. **Dependency reasoning** — decide whether always picking the
   topically-closest-sounding tool, instead of the cheapest decisive
   signal, makes a wrong-tool-choice failure more or less likely.
3. **(Production-gear) Normalize a policy ID** — tolerate four real
   argument-formatting variations, not just one.
4. **(Production-gear) Implement a tool-selection function** — check
   the cheapest, most decisive signal before the topically-tempting
   one.
5. **(Production-gear) Implement a timeout-retry policy** — recover
   from a transient hang without retrying forever.
6. **(Production-gear) Diagnose a failure type** — read a real trace
   and correctly name a malformed-output failure.
7. **(Production-gear) Implement an outcome-check function** — catch a
   tool that always "succeeds" but doesn't mean the problem is solved.
8. **Completeness check** — confirm all five tool-failure concepts were
   actually used.

## Files

- `starter.py` — the scaffold with 11 `# TODO`s and the score report.
- `solution.py` — the fully filled-in reference; scores 16/16.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-diagnosis-then-critique exercise using a
  third scenario.
