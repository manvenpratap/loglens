# LogLens Agent Rules

## Mandatory Context Reading
- **ALWAYS** read `/Volumes/Study/Projects/loglens/.agents/PROJECT_CONTEXT.md` at the start of every session before writing any code.
- **ALWAYS** read the current `implementation_plan.md` artifact to understand what phase you are in.

## Project Context Maintenance
- After every meaningful change to `loglens.html` (new feature, refactor, bug fix), update the **Current Status** and **Implemented Features** sections in `PROJECT_CONTEXT.md`.
- If new roadmap items are completed, mark them as done in `PROJECT_CONTEXT.md` under "Roadmap Progress".
- If the architecture changes (new modules, major restructuring), update the **Architecture** section accordingly.

## Core Constraints (Never Break These)
1. **Single-file HTML** — the primary artifact is always `loglens.html`. Do NOT split into separate JS/CSS files unless explicitly asked.
2. **Zero dependencies** — no npm, no external JS libraries at runtime. No CDN imports unless instructed.
3. **Privacy-first** — all log parsing happens in-browser (Web Worker). Never send log data to any server.
4. **Vanilla CSS + JS** — no React, Vue, Angular, Tailwind, or any other framework.

## Code Style
- Use the existing section comment pattern: `/* ================================================================ §JS-N SECTION NAME ================================================================ */`
- Follow the existing naming: `S` for global state, module objects (`CFG`, `UI`, `WM`, etc.) for encapsulation.
- Use `const $=id=>document.getElementById(id)` for DOM lookups.
- Toast notifications via `toast(msg, type)` for user feedback.
- Always use the `esc()` utility for HTML-encoding user/log data before injecting into innerHTML.

## Testing Approach
- After implementing any parsing feature, verify with the built-in sample log (click "Download Sample Log" in Help tab).
- Confirm no JS console errors after changes.
- Test both dark and light themes after visual changes.

## Graphify Integration
- Graphify is **formally attached** to this project via `/Volumes/Study/Projects/loglens/.agents/GRAPHIFY_INTEGRATION.md`.
- **Always read `GRAPHIFY_INTEGRATION.md`** before implementing any chart, graph, or visualization feature.
- D3.js (`claude-d3js-skill`) is the visualization engine. Read the SKILL.md before writing any d3 code.
- D3 must be **lazy-loaded** via dynamic `import()` — never bundled at startup.
- Canvas 2D for interactive charts (performance); SVG for exports (quality).
- All Graphify code goes in `§JS-22 GRAPHIFY ENGINE` in `loglens.html`.
- If D3 fails to load (offline), fall back gracefully and toast a warning.

## Git Version Control Rule
- **ALWAYS** perform a `git add`, `git commit` (with a descriptive message), and `git push` command after every major change or milestone is successfully finished and verified.

## Regression Test Suite Rules (MANDATORY)
The project maintains a formal regression test package at `tests/`. All agents MUST follow these rules:

1. **Read** `tests/README.md` before adding or modifying any test.
2. **Run tests before committing**: After implementing any feature or fixing any bug, run:
   ```bash
   ./run_tests.sh tests/test_NN_<feature>.py   # New/changed module only
   ./run_tests.sh                               # Full suite — no regressions
   ```
3. **Write a test for every feature**: Every new feature added to `loglens.html` must have a corresponding test file in `tests/`. File naming: `test_NN_<feature_name>.py` where NN is sequential.
4. **Never delete tests**: If a feature changes, update the existing test file rather than deleting it. Deleted tests = silent regressions.
5. **Use shared fixtures**: Always use `page_with_data` (data loaded) or `blank_page` (empty state) from `conftest.py`. Never copy-paste browser setup code.
6. **Keep tests independent**: Each test function must be self-contained — use the fixture's fresh browser instance.
7. **Add `assert_no_critical_errors(page)`** at the end of any test that exercises JS module behaviour.
8. **Update `tests/README.md` Coverage Map** when a new test file is added.
9. **`pytest.ini` stays at project root** — do not move it.
10. **`run_tests.sh` is the canonical runner** — document all test run invocations using it.
