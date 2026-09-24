# Maintenance Guide (Solo-Maintained Project)

This repo is maintained solely by its owner — it is **not open to
external contributions**. Issues and pull requests from outside
contributors are not reviewed or merged. If you found this repo
useful, feel free to fork it for your own use per the license
(`LICENSE` for code, `LICENSE-CONTENT` for lesson content), but please
don't open issues or PRs here.

This doc is a working reference for how content gets added or updated,
so nothing drifts from the repo's conventions as it grows.

## The non-negotiable rule: test before you write

Inherited directly from `ai-engineering-for-everyone`,
`llm-evaluation-for-everyone`, and every course before it, where it
caught real, non-obvious bugs repeatedly. Every code example in every
chapter — every agent loop, planner, tool-calling harness, memory
store, reflection loop, guardrail check, evaluation script, or
multi-agent orchestrator — must be installed and run for real (against
the real `openai` client pointed at a real local Ollama server with a
real model pulled, where applicable) before being written into a
lesson — never written from memory or copied from older tutorials.
**Do not relax this for any edit, however small it seems.** A claimed
agent trace, tool-call result, or reliability number that wasn't
actually produced is worse than useless — it's the exact "it looked
good in the demo" failure mode this course exists to prevent.

```bash
python3 -m venv /tmp/aafe-test-env
/tmp/aafe-test-env/bin/pip install openai
# ollama pull <model>  -- see PROJECT_STATE.md for the current
# recommended model; requires a running local Ollama server
# (https://ollama.com), no API key or account needed.
# The openai client points at it via base_url="http://localhost:11434/v1".
/tmp/aafe-test-env/bin/python your_new_example.py
```

Only write the example into the lesson once you've seen its real
output. If a live model call genuinely can't be captured this session
(Ollama hangs — see `PROJECT_STATE.md`'s disclosure, including the
documented 432s intermittent-hang case), say so explicitly in the
lesson text itself — never claim a live transcript that wasn't
observed. Treat live calls as illustrative, not gate-load-bearing:
budget up to 450s and prefer showing captured output over
idle-blocking a session.

## Adding or updating a chapter

1. Follow the rich per-chapter file pattern from Chapter 1 (this
   course's default from the start): `lesson.html`, `quiz.html`,
   `interview-questions.html` + `interview-questions.md`,
   `exercises/{index.html,starter.py,solution.py,README.md,ai-paired.html}`,
   `practice/{index.html,starter.py,solution.py,README.md,ai-paired.html}`,
   `project/{index.html,starter.py,solution.py,README.md,ai-paired.html}`
   (+ `RUBRIC.md` where the chapter has a graded project).
2. Test every code sample per the rule above before writing it into
   the lesson.
3. Wire the chapter into `assets/chapters-data.js` — give it a `path`
   only once its `lesson.html` actually exists (see that file's header
   comment for why a premature `path` breaks the site).
4. Update `docs/curriculum/index.html` (the styled roadmap) and the
   root `index.html`'s chapter/module counts in `hero-stats`.
5. Write a quality audit at `quality-audits/chapter-0N-audit.md`
   including a live-tested-vs-logical-only disclosure section.
6. Run the local checks below before pushing.

## Local checks before pushing

```bash
bash scripts/local_check.sh < /dev/null
```

Use `< /dev/null` if any chapter's code calls `input()` for a live
interactive demo. This runs the same checks CI runs: folder structure,
placeholder-text scan, Python syntax + actual execution of every
`solution.py` (exercises, practice, and project), JS syntax, chapter-path
validation against `chapters-data.js`, and a secret scan. If it fails,
CI will fail too — fix locally first.

## File naming convention

```text
chapters/chapter-NN-kebab-slug/lesson.html
chapters/chapter-NN-kebab-slug/quiz.html
chapters/chapter-NN-kebab-slug/interview-questions.html
chapters/chapter-NN-kebab-slug/interview-questions.md
chapters/chapter-NN-kebab-slug/exercises/{index.html,starter.py,solution.py,README.md,ai-paired.html}
chapters/chapter-NN-kebab-slug/practice/{index.html,starter.py,solution.py,README.md,ai-paired.html}
chapters/chapter-NN-kebab-slug/project/{index.html,starter.py,solution.py,README.md,ai-paired.html}
assessments/written-exams/module-N-exam.html (+ .md as raw/portable source)
quality-audits/chapter-0N-audit.md
```

- Chapter numbers are two-digit, zero-padded: `chapter-01`,
  `chapter-02`, ... `chapter-13`.
- Slugs are lowercase, hyphenated, no special characters.

## Content standards

- **No placeholder text** in anything merged to `main` — no `[insert
  X]`, no Lorem ipsum. CI blocks these. (Bare `TODO 1:`, `TODO 2:` etc.
  inside `exercises/starter.py` and `project/starter.py` are
  intentional learner tasks, not placeholders — CI does not flag
  those.)
- **No API keys or secrets** committed anywhere, ever. CI scans for
  common secret patterns.
- **Cross-chapter Python imports** must use
  `importlib.util.spec_from_file_location`, never a `sys.path.insert`
  + `import solution` trick — multiple files across chapters share the
  name `solution.py`, and the naive approach breaks depending on
  invocation method.
- **Every file with a top-level `asyncio.run(main())`** must guard it
  with `if __name__ == "__main__":`.
- **Long-running or live-server-dependent solution.py files** need a
  `# CI: LONG_RUNNING_SERVER` or `# CI: NEEDS_LIVE_SERVER=<path>`
  marker comment (see `ci.yml`'s comments).
- **Chapters that call the model via Ollama** must check for a running
  local Ollama server and skip/degrade gracefully with a clear message
  if it's absent, rather than crashing — CI runners don't have Ollama
  running or a model pulled.
- **Written exams render as styled HTML**, not raw `.md`.
- **No hard dependency on a paid API anywhere.** Hands-on code runs
  against local Ollama via the plain `openai` client by default, with a
  documented option to swap in a hosted provider. No heavy agent
  framework (LangChain, LangGraph, CrewAI, AutoGen, etc.) as a required
  dependency — concepts are taught with minimal, readable code;
  frameworks may be mentioned as an optional "how this maps to X" note,
  never required to complete a chapter.
- **Every chapter needs**: a hook grounded in a real agent failure mode
  (a loop that never terminates, a tool call with the wrong arguments,
  a plan that silently drops a step, an agent that can't tell it
  failed), tested code (not illustrative pseudocode) with real captured
  output, a production scenario, an explicit statement of what the
  chapter is *not* re-teaching from `ai-coding-agents-for-everyone`,
  `mcp-for-everyone`, `ai-engineering-for-everyone`,
  `llm-evaluation-for-everyone`, or `context-engineering-for-everyone`
  wherever relevant, a builder thought-process box, 8+ exercises (5+
  production-gear), 8+ practice scenarios, 8+ interview questions
  across all 4 levels, and a project where the curriculum map assigns
  one.

## Code-density bar (hard requirement)

This ecosystem has twice shipped a chapter that was structurally
complete (right files, right sections) but too thin — a conceptual
essay with occasional illustrative snippets instead of an
incrementally-built, actually-run, output-shown code walkthrough
(`ai-coding-agents-for-everyone` and `context-engineering-for-everyone`
both needed a later retrofit pass, "deepen lesson code density," to fix
this after the fact). Do not repeat it. Every `lesson.html` needs
**60+** real `<pre>`/`<code>` blocks — err toward the denser end, built
as one incrementally-extended, actually-run agent, not a pile of
disconnected snippets. Verify against
`python-for-everyone/chapters/chapter-01-first-program/lesson.html` and
`chapter-02-variables-data-types/lesson.html` (this ecosystem's deepest
reference, 56 and 62 blocks respectively) before calling a chapter
done.
