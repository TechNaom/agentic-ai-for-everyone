# Chapter 10 Exercises: Multi-Agent Coordination and Communication

These exercises use a second scenario, deliberately different from the
lesson's Harrowgate Logistics Exchange/DockScout-YardScout hook:
**Bellcrest Freelance Guild**, a fictional freelance-coordination
cooperative. Its two PEER agents, **DesignScout** and **DevScout**,
must claim tasks from a shared project backlog by exchanging messages
directly — no supervisor routes work between them. Applying this
chapter's peer-to-peer coordination concepts to a fresh scenario is the
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

It prints a score report. Fill in each `# TODO`, re-run, and watch
your score climb toward the total (19 points across 7 tasks).

## The seven tasks

1. **Map facts to multi-agent communication concepts** — assign the
   correct concept (miscommunication, duplicated work, deadlock,
   fail-closed validation, consensus/tie-breaking) to five Bellcrest
   facts.
2. **Message-validation reasoning** — decide whether a receiving agent
   should guess an unrecognized field name maps to a known one.
3. **(Production-gear) `parse_message_safely`** — normalize safe
   whitespace issues, fail closed on a missing or renamed field.
4. **(Production-gear) `coordinated_claim`** — a shared, locked
   claim-check preventing duplicated work between two peers.
5. **(Production-gear) `which_agent_caused_miscommunication`** —
   message-level cross-agent attribution, extending Chapter 9's
   dispatch-level version.
6. **(Production-gear) `classify_communication_gap`** — classify a
   peer-to-peer setup's biggest blind spot from a capability dict.
7. **(Production-gear) `resolve_conflicting_claims`** — consensus
   voting with fail-closed tie handling.

## Files

- `starter.py` — the scaffold with 11 `# TODO`s and the score report.
- `solution.py` — the fully filled-in reference; scores 19/19.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a third
  scenario.
