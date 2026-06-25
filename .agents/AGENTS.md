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
