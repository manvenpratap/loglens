# LogLens — Project Context

> **Agent Rule:** Read this file at the start of every session. Update it after every meaningful code change.

- **Unified Thread Dropdown Search (v6.9.13 — COMPLETED)**:
  - Merged the separate thread search field (`#thr-in`) and scan button (`#btn-disc`) from the control bar directly into the active thread dropdown.
  - Added a sticky, focus-friendly text filter input (`#vt-chips-menu input`) inside the portal dropdown menu, allowing users to dynamically filter and select threads.
  - Cleaned up control bar layout by removing redundant Thread input and discovery button, leaving only Log File selector and Parse controls.
- **Log File Selection Split-Button (v6.9.12 — COMPLETED)**:
  - Replaced the separate "Select" and "+" (Add File) buttons with a single unified split-button.
  - Clicking the main button triggers log selection, while clicking the chevron arrow opens a portal menu with the option to "Add file to session".
  - Implemented the menu using fixed positioning (`position: fixed` and `getBoundingClientRect()`) to prevent it from being clipped by overflow-hidden parent elements.
- **Active Thread Dropdown — Definitive Fix (v6.9.11 — COMPLETED)**:
  - Replaced native `<select>` (whose text colour was unreliable across OS themes) with a fully custom `<button>` + `<ul>` dropdown built entirely from standard DOM elements for 100% CSS control.
  - Fixed click target: added `pointer-events: none` to inner `<span>` and `<svg>` chevron so clicks always reach the `<button>` listener, not a child element.
  - Fixed click handler accumulation: stored the document close-handler in `UI._vtCloseHandler` and call `removeEventListener` before each re-render to prevent stacking.
  - **Root-cause fix for invisible menu**: moved the dropdown `<ul>` out of the `.vtabs` DOM tree and appended it directly to `document.body` as a **portal** with `position: fixed`. Coordinates are computed at open time via `getBoundingClientRect()`, completely escaping the `.vtabs` `overflow: hidden` clip that was hiding the menu off-screen.
  - Updated `UI.sw()` to sync the custom button label (`#vt-active-label`) and amber item highlight whenever the active thread changes externally (keyboard shortcuts, row clicks, etc.).
  - Implemented natural sorting (alphanumeric order) for the threads list inside `UI.render()` using `localeCompare` with `numeric: true` (e.g., `worker-2` comes before `worker-10`).
  - Restyled the thread selector dropdown into a premium active status indicator badge, complete with a glowing amber status dot.
  - Removed the breadcrumb context bar (`#breadcrumb` / `BCB` namespace) completely from both HTML and script (stubbed namespace to prevent ReferenceErrors) to eliminate vertical clutter and maximize vertical workspace for the timeline.
  - Implemented collapsible split panes (Waterfall Timeline and Execution Tree) via toggle arrow buttons (`◀` / `▶`) on the divider (`.sp-hdl`), with smooth transitions and persistent split ratio tracking (`S.splitRatio` and `S.collapsedPane`).
  - Added a collapsible/minimizable top control bar (`.ctrl`) triggered by a chevron toggle button in the header actions slot, maximizing vertical layout space for the timeline, with state persistence across loads.
  - Fixed scroll-driven scrubber scroll target binding by prioritizing `ganttWrapper.querySelector('.g-rows')` as the parent scroller in `SCRUBBER.attach`, ensuring horizontal scroll events on the track are captured.
  - Aligned scroll-driven scrubber timeline position (`#ll-scrubber`) by updating `SCRUBBER._update` to use the formula `calc(250px + (100% - 250px) * ratio)`, and incorporated zoom and horizontal scroll offset (`scrollLeft` and `scrollWidth`) into the duration calculations. This ensures that the tooltip (`#ll-scrubber-tip`) displays the correct time segment dynamically when the user scrolls horizontally or zooms.
  - Fixed Swimlane zoom visible range boundary persistence by resetting `S.visibleStart = null` and `S.visibleEnd = null` in `UI.render()` when a new log file is loaded, preventing outdated range bounds from causing `0.00ms` calculations.
  - Resolved global search overlapping layout bugs by changing class selector `.hdr-search` to ID selector `#hdr-search` in all CSS rules (including the initial rule block, media query breakpoints, and audit override rules).
  - Implemented a centralized JS-driven state toggle (`updateSearchUIState()`) bound to input, focus, and blur events to dynamically hide the `/` shortcut key helper whenever the input is focused or has text, preventing any overlap with the clear button `✕`.
  - Fixed text overlapping magnifying glass search icon by setting left padding to `34px !important` on the input, and positioning the icon at `left: 12px` with explicit `13px x 13px` dimensions.
  - Positioned the shortcut badge `/`, clear button `✕`, and search matches count inside the search container with absolute positioning.
  - Implemented dynamic focus/query padding-right on the input field (`90px`) to prevent typed text from overlaying the buttons and counts.
  - Converted the thread selector pills into a premium dropdown select element in the view tabs bar (`vt-chips-select`) with active state value sync.
  - Removed the horizontal scroll buttons and wrapper helper block from script setup as they are no longer required.
  - Aligned onboarding demo sequence (`ONBOARD.loadDemo`) to parse and display the same 16-thread log sample dynamically generated via a shared `getSampleLogLines()` helper.
  - Added transaction tracking rules (`dr_txs` / `dr_txe`) to onboarding `DEMO_CFG` to properly render the transaction begins/ends.
  - Expanded the Thread Correlation overlap heatmap matrix thread display slice limit from 10 to 16.

- **3D Force-Directed Graph Layout Fix (v6.9.9 — COMPLETED)**:
  - Fixed the dependency graph rotation bug where node spheres drifted and flew out of their connector lines.
  - Nested the connection lines inside `this._forest` Group instead of `this._scene` directly to align them to the same local coordinate space.
  - Refactored model-reset and view-destruction code to use parent-relative detachment (`child.parent.remove(child)`) for safe resources garbage collection.

- **3D Views Fix & Mobile Touch Optimization (v6.9.8 — COMPLETED)**:
  - Resolved event listener memory leaks by cleanly detaching all custom `mouseup` and `mousemove` window events on `destroy()`.
  - Added full mobile and tablet touch interaction support (`touchstart`, `touchmove`, `touchend`) to translate swipe gestures into camera rotation and taps into clicked node focus.
  - Capped maximum renderer device pixel ratio (DPR) to `1` on mobile devices and `2` on high-DPR desktop screens to prevent CPU/GPU thermal bottlenecks.

- **Topbar and Sidebar Visual Redesign (v6.9.7 — COMPLETED)**:
  - Redesigned sidebar tabs using monospace font family (`var(--mono)`), size `10px`, weight `600`, and JSDoc-style abbreviations (`CFG`, `SET`, `L4J`, `HLP`) with pure monospaced labels.
  - Implemented smart visibility rule for tab icons: hidden by default when expanded and displayed only when collapsed.
  - Upgraded active tab background glider (`#sb-tabs-pill`) into a tactile mechanical slider panel with a 2px left amber accent border.
  - Added a clinical Status Monitor badge (`.system-status`) in the topbar slot featuring a dynamic pulsing LED indicator synchronized with parsing operations (`SYS_STATUS // PARSING_LOG` / `LOG_LOADED` / `IDLE` states).
  - Cleaned up topbar logo to utilize flat boundaries and monospaced typography to enhance industrial console aesthetics.

- **Obsidian Amber Theme Implementation (v6.9.6 — COMPLETED)**:
  - Shifted the dark theme background colors from a warm mud-gray hue to a deep obsidian-slate blue-gray (Hue 240) while preserving warm telemetry highlighting lights.
  - Aligned header elements and backgrounds to match glassmorphic dark-slate tints.
  - Synced 3D visualizer canvas backgrounds and exported summary canvas panels to pull from the same cool obsidian slate palette.

- **Frontend Guidelines Search Refactor (v6.9.5 — COMPLETED)**:
  - Audited search listeners and eliminated the fragile `cloneNode` hack that stripped custom event listeners from `hdr-search`.
  - Added a reusable, performance-safe `UTILS.debounce` helper for debouncing heavy DOM-rendering and state updates.
  - Consolidated three scattered search listeners into a single, unified search controller.
  - Optimized rendering throughput: instant typing response for UI updates (breadcrumb tags and clear button toggle) coupled with 250ms debounced re-renders, preventing double-traversal of highlighting.

- **Immersive 3D Experience Upgrades (v6.9.4 — COMPLETED)**:
  - Integrated a WebGL compatibility pre-check (`_isWebGLAvailable`) displaying diagnostic warnings if unsupported.
  - Added a Layout Mode dropdown to toggle dynamically between three 3D representations: Log Forest, Spiral Helix, and Force-Directed Graph.
  - Upgraded **Log Forest (Waterfall)** mode to render outliers and SLA breaches with glowing emissive materials and floating pulsing indicators.
  - Implemented **3D Spiral Helix (Sequence)** mode to render sequential chronologies along a spiral helix path with a golden backbone guideline.
  - Developed a standalone **3D Force-Directed Graph (Network)** physics engine solver using Verlet integration to simulate dynamic node repulsion, link spring attraction, and gravity.
  - Integrated dynamic theme-matching colors to synchronize radial background gradients, floor grid helper borders, and overlays on dark/light toggle.
  - Wired an interactive click-and-focus bridge (`focusNode`) to transition back to split/tree view and scroll-center clicked elements.

- **Sidebar Design Upgrades & Refinements (v6.9.3 — COMPLETED)**:
  - Re-styled the sidebar navigation bar into a segmented control tab strip with clean borders, nested spacing, and dark background highlights.
  - Custom styled the active indicator sliding pill (`#sb-tabs-pill`) to conform as an elegant container-inset background.
  - Replaced the thick Unicode collapsible section indicator (`▸`) with a clean, thin chevron (`›`) that rotates smoothly on state transitions.
  - Hidden redundant text-based "Toggle" labels in collapsible headers.
  - Refined rule cards (`.rc`) with consistent outlines, hover offsets, and tactile click states, and polished status cards (`.cfg-st`) to strip drop-shadow noise.
  - Styled a surgical 1px vertical line indicator down the center of the drag resizer (`.sb-resize-handle`) on hover and focus.
  - Bumped panel margins to `16px` for layout whitespace and breathing room.

- **Visual Overhaul and Branding Alignment (v6.9.2 — COMPLETED)**:
  - Fixed branding inconsistencies by placing an "LL" lettermark logo inside the `.logo-ico` box and styling it for high readability across both light and dark themes.
  - Replaced the Unicode character `⌕` search icon with a high-fidelity vector SVG magnifier glass icon.
  - Replaced modal save/title emojis (`💾`, `🧩`, `📝`) with standard vector SVGs (floppy disk, 3D cube, edit pen) in HTML buttons/headings.
  - Extracted 35+ scattered inline `style=""` overrides from JIRA, Cloud Datasources, Git, Plugins, and Directory Watcher form fields into clean, responsive CSS rules.
  - Styled collapsible sub-section toggle buttons as rotating chevrons with hover backgrounds instead of text-based toggle cues.
  - Aligned help panel reference tables (`.hlp-table`), keyboard shortcut rows (`.kb-row`), and capture cards (`.cg-field`) with strict design token typography and grids.
  - Resolved theme identity issues: restored warm OKLCH cream system tokens (`--bg-2/3/4` and `--bg-overlay`) in Light Theme, overriding the cool-gray GitHub colors.
  - Standardized the Query view tab to render its `>_` terminal icon inside a structured monospaced code badge that highlights amber on active state.

- **Visual Audit Round 2 — Comprehensive Production Polish (v6.9.1 — COMPLETED)**:
  - Fixed 15 spacing violations — brought `.ctrl`, `.sp`, `.res`, `.rc`, `.ws-step`, `.f`, `.settings-section-*`, `.pref-row`, `.ann-h3`, `.ann-comment`, `.od-stat`, `.lql-input-row`, `.sp-pane`, `.emp-card` to strict 4px grid.
  - Fixed light-theme overlay readability — `#ctx-menu` now uses `var(--bg-2)` (opaque) instead of semi-transparent `--bg-overlay` which rendered text illegible.
  - Fixed `.cmd-ov` and `.sh-ov` to use `var(--bg-overlay)` token instead of hardcoded dark `rgba(0,0,0,.72)` for light-theme correctness.
  - Fixed `.modal` incorrectly included in bulk `border-radius: var(--radius-md)` override; modal now correctly uses `var(--rounded-lg)` (10px).
  - Fixed icon gap anti-pattern on `.vt` — replaced `margin-right:4px` on SVG with `gap:6px` on the flex container.
  - Added `:active` press states to `.rc`, `.cmd-item`, `.lql-preset-btn`, `.hdr-more`, `.tok` (previously missing).
  - Fixed `toggle-thumb { top:3px }` to `top:4px` to sit on the 4px grid.
  - Restored toast semantic left accents at `3px` (with `1px` on remaining sides) — correct per UX design spec.
  - Neutralized `#mm-tooltip` decorative left amber border; replaced with uniform `var(--bdr)`.
  - Removed sidebar from raised-element shadow list (sidebar already has `border-right`; double elevation was visual noise).
  - Typography: added `line-height:1.55` to `textarea.inp`, bumped stats `.sl` from 8.5px→9px (readability floor), propagated `line-height:1.4` to `cmd-item-name` and `cmd-item-cat`.

- **Visual Audit and Aesthetic Alignment (v6.9 — COMPLETED)**:

  - Standardized all paddings, margins, and gaps to the 4px spacing grid across buttons, inputs, panels, stats, empty states, modals, and list rows.
  - Aligned search input with absolute positioned search icon, clear button, and shortcut `/` badge, resolving all horizontal spacing misalignment.
  - Solved light theme contrast deficiency by darkening the `--t4` caption color token to `oklch(50% 0.01 55)`, achieving a WCAG AA-compliant 4.5:1 ratio.
  - Implemented scale-based interactive feedback transitions (`transform: scale(0.96)`) for tactile active states on all pressable controls.
  - Resolved nested border-radius mismatch on toggles, corrected stats cards overflow by enabling responsive wrapping, and balanced onboarding grid features to a 2x2 layout.
  - Removed decorative side-border accents on sticky notes and command palette to enforce clean, neutral outlines and surface elevations.

- **LogLens Production-Grade UI/UX Overhaul (v6.8 — COMPLETED)**:
  - Upgraded Design Tokens: spacing, border-radius, z-indices, easings, and monospace features on metadata, stats, and hex strings.
  - Redesigned Header: added version v6.1 badge, wrapped search container (left search icon, clear button, '/' shortcut), pulse animation badges, and amber bottom border gradient.
  - Enhanced Integration Hub Segment Controls: replaced type selector with orange (Loki), yellow (ES), and warm-orange (AWS) brand segments, and implemented JIRA webhook connection preflight tester.
  - Upgraded Rules List: added hoverable micro-dropdown menu items (Edit, Export, Delete) on card lists, and data-tip hover pattern preview tooltips.
  - Refined Workspace: added vertical dividers in control bar, thread overflow scroll buttons, and detail count sub-labels with green checkmark completion.
  - Rebuilt Renderers: warning triangles on Gantt SLA breaches, absolute/self swimlane vertical text headers, 28px virtual row height, SVG pen icon annotations, and rules coverage grid stats.
  - Upgraded Dialogs/Overlays: scale-in transitions on context menus, command palette splits, custom countdown progress bars on toasts, and mobile Log4j XML drawers.
  - Wired interactions: countUp animations, sidebar drag resize handles, global tooltip hover manager, and Home/End/PgUp/PgDn tree navigation overrides.
  - Tree Minimap Alignment: Resolved vertical displacement of the canvas scroll minimap by housing the canvas and thumb under a shared nested container division below the absolute header label.
  - Tree Row Layout Spacing: Added flex gap layout rule to `.tbd` container in tree rows, preventing element names, durations, timestamps, and payload attributes from colliding or overlapping.
  - UI/UX Refinements: Integrated a gliding sliding tab indicator for the sidebar tabs (CONFIG, SETTINGS, LOG4J, HELP), refined the active view tab indicator colors and borders, and styled `.kbd` shortcut badges as 3D keyboard key caps.

- **LogLens Overdrive Integration (v6.7 — COMPLETED)**:
  - Implemented Cinematic Detail Morphing using the View Transitions API, enabling smooth, spatial morph transitions when clicking tree nodes to inspect full event payloads and metadata.
  - Added a Canvas-Accelerated Scroll Minimap on the execution tree, rendering a colored density heatmap of errors (red), outliers (amber), and standard events (blue) with custom thumb tracking.
  - Enhanced the Canvas Minimap with interactive hover guidelines and a floating tooltip component (`#mm-tooltip`) that details the hovered operation name, duration, payload preview, and classification (SLA Breach, Outlier, Critical) dynamically.
  - Configured layout visibility: detaches the minimap completely (reclaiming padding space) when switching to Split Mode or Gantt Mode to preserve screen real estate.
  - Built custom Spring Physics scrolling interpolation (`requestAnimationFrame` solver) for smooth, momentum-based scrolling through the virtualized tree view from the minimap canvas.
  - Integrated a zero-jank scroll-driven timeline scrubber on the Gantt waterfall chart that updates its horizontal position dynamically relative to the vertical scroll offsets of the timeline.
  - Upgraded Gantt Waterfall Chart: sticky time-ruler header, major time marks plus 16 minor tick marks, hover accent glows, diagonal stripe hatch pattern for self-time rendering, click-to-morph row selection highlighting, and live timeline tooltips.
  - Restored full scroll-and-drag pan, mouse wheel zoom, alt+drag selection, and window fitting on Gantt views by rebinding events dynamically to rebuilt container nodes.

- **LogLens Impeccable Design Overhaul (v6.5 — COMPLETED)**:
  - Standardized all hardcoded literal colors (135) and border-radius dimensions (65) to CSS variable design system tokens (`--rounded-sm`, `--rounded-md`, `--rounded-lg`, `--rounded-full`).
  - Removed AI slop side-stripe card borders and toast accent borders, transitioning sequence diff boxes and log tree nodes to clean uniform outlines and soft backgrounds.
  - Replaced spring-bouncy eases with snappy, mechanical cubic-bezier curves (`--ease-snap: cubic-bezier(0.16, 1, 0.3, 1)`) and renamed bounce keyframes to `stream-float`.
  - Optimized workspace layout by eliminating performance-heavy `width` transitions on input focus and sidebar collapse, resolving repaint issues.
  - Substituted display font variables to match the specified `Inter` family stack, and added missing VoiceOver `aria-label` tags to visual dialog and delete buttons.
  - Cleaned up font link imports in HTML header by removing unused `Space Grotesk`, adding `Inter` loads, and declaring fallback tokens in `DESIGN.md`.
  - Standardized remaining custom radii (3px, 9px, 12px, 16px) and light theme color overrides in documentation.
  - Eliminated user guide em-dashes (—) to resolve AI writing cadence tell warning, and converted modal form label divs to accessible `<label>` tags with matching `for` and `id` input selectors.
  - Replaced legacy emoji visual indicators (📁, 🔄, 🔍, 🧙, ⚙, 🎨, 🚨, 🗺, 📋, 📊, 📝) across buttons, headings, and tab selectors with high-fidelity vector outline SVGs, creating a clean, consistent developer-console visual language.
  - Completed a comprehensive `/frontend-design` visual sweep of the application, removing all remaining emoji icons inside the onboarding modal highlights, empty state drop zone panels, thread/pin tabs, settings headers, and LQL query dropdown lists, substituting them with elegant vector SVGs and monospace console glyphs.
  - Executed `/impeccable colorize` to upgrade the neutral grayscale palette to a strategic OKLCH color system tinted with the Console Amber brand hue (`#f0883e`).
  - Updated Javascript visual defaults to use semantic CSS variables (`var(--t4)`, `var(--blue)`) instead of hardcoded hex values.
  - Enhanced the Gantt chart rendering to dynamically color bars based on severity (`var(--red)` for SLA breach, `var(--amber)` for outliers, `var(--purple)` for critical path) and adjust opacity based on duration length for better heatmapping.
  - Bumped project version to `v6.6` (Conceptual) to mark the completion of the color overhaul.

- **LogLens UI/UX & Responsive Overhaul (v6.4 — COMPLETED)**:
  - Merged/overwrote UI/UX enhancements bundle onto `loglens.html` as the production release.
  - Implemented a welcome onboarding overlay (`ONBOARD` module) with a guided quickstart and demo Spring Boot parsing sequence.
  - Created a contextual help tip popover system (`HTIP` module) for forms (SLA, stack behavior, capture mappings).
  - Refactored the Quick Guide panel in the sidebar into tabbed sections with interactive LQL click-to-run queries.
  - Reorganized header layout into a responsive slot structure collapsing badges to a `⋯` menu on compact viewports.
  - Added CSS media queries for responsive slide-in sidebar navigation drawers with backdrop blurs.
  - Standardized focus-visible outlining and `.sr-only` accessibility helpers.

- **LogLens Code Audit & Structural Refactor (v6.3 — COMPLETED)**:
  - Added Virtual Logical Project Map structure block detailing style layout layers and script namespaces.
  - Inserted Logical Architecture Guide at the top of the script tag documenting module interaction boundaries.
  - Standardized enums and constants (`CONSTANTS` object) for layouts, views, storage keys, and behaviors.
  - Implemented centralized DOM helper utility layer (`DOM` object) providing safe element query, event listeners, class toggle, and value getters.
  - Implemented selector interface layer (`SELECTORS` object) to retrieve computed state values (active thread, visible rules, events list).
  - Appended Developer Maintenance Notes documenting code conventions, expansion points, and keyboard bindings.
  - **File**: 12,860 lines, ~504 KB. JS syntax verified clean and validated.

---

## Project Overview

**LogLens v2** is a **zero-dependency, single-file HTML** log analysis tool. It is a *Metadata-Driven Log Analyzer* — users configure regex-based rules that match log lines and extract structured data (timestamps, thread IDs, element names, payloads). The tool then visualizes execution flow as:
- **Gantt / Waterfall Timeline** — horizontal bars showing duration per operation
- **Execution Tree** — hierarchical collapsible tree of nested operations
- **Split View** — side-by-side Gantt + Tree

The core philosophy: **offline-first, privacy-by-default, zero install** — a single `.html` file you open in a browser.

---

## Architecture

### Single HTML File Structure (`loglens.html`)
```
loglens.html
├── CSS §1–16     Design tokens, layout, components, animations, Phase 1 additions
├── HTML          Shell: Header, Sidebar (4 panels), Main, Modal, Log4j Sheet, Drop overlay, Context menu
└── JavaScript §1–31
    ├── §1  S{}              Application state object (+ S.appPrefs, S.ganttLabelWidth)
    ├── §2  DEF_CFG          Default configuration with 8 sample rules
    ├── §3  W_SRC            Web Worker source (blob URL) — the parse engine
    ├── §4  Utilities        esc(), fmtB(), fmtMs(), $(), cnt(), mEnd(), ibg()
    ├── §5  Theme            Dark/light toggle with localStorage persistence
    ├── §6  SB               Sidebar collapse/expand
    ├── §7  LJP              Log4j XML parser (Log4j 1.x, 2.x, Logback → regex)
    ├── §8  TOKS / TMPLS / WIZ_FMTS  Token palette + pattern templates
    ├── §9  RXB              Regex Builder — click-to-insert token palette
    ├── §10 WIZ              Keyword Wizard — guided rule creation
    ├── §11 HS               Hotspot Analyzer — computes % of parent time
    ├── §12 CFG              Config Manager — load/save/persist rules
    ├── §13 FS               File System Access API handler
    ├── §14 WM               Web Worker Manager — parse / scan threads
    ├── §15 GR               Gantt Renderer — waterfall chart (innerHTML-based)
    ├── §16 TR               Tree Renderer — collapsible details/summary tree
    ├── §17 UI               UI Controller — modal, views, thread switching
    ├── §18 dlSample()       Sample log generator / downloader
    ├── §19–20 Event wiring + bootstrap
    │
    │  ── PHASE 1 ADDITIONS ──
    ├── §21 EXP              Export Engine: CSV, JSON tree, SVG Gantt, HTML report; per-rule export/import
    ├── §22 DD               Drag-and-drop: drop log files or JSON configs anywhere on page
    ├── §23 MF               Multi-file session: chip bar, add/remove log files
    ├── §24 GZ               Gzip decompression via DecompressionStream API
    ├── §25 IDB              IndexedDB cache: SHA-256 key, last 5 sessions, cache-hit prompt
    ├── §26 RTS              Rule Test Suite: modal for pasting sample lines, per-rule match report
    ├── §27 RO               Rule Ordering: HTML5 drag-and-drop reorder within rules list
    ├── §28 CTX              Context Menu: right-click tree nodes for copy/pin/focus actions
    ├── §29 PIN              Pin / Bookmark system: pin nodes, listed in Help sidebar
    ├── §30 KBN              Keyboard tree navigation: j/k, / search, p pin
    ├── §31 VER              Config Versioning: auto-bump on save/delete, 20-entry changelog
    │
    │  ── PHASE 2 ADDITIONS ──
    ├── §32 STATS            Stats Engine: latency stats (P50/P95/P99), inline spark-histograms, comparison
    ├── §33 ANOMALY          Anomaly Engine: outlier tagging, SLA breaches highlight, cause tracking
    ├── §34 GRAPHIFY         Graphify D3 Engine: large histogram modal, transaction dependency graph
    ├── §35 SWIMLANE         Swimlane Timeline: Canvas-based swimlane view with zoom/pan and minimap
    │
    │  ── UI/UX OVERHAUL (v6.1/v6.2) ──
    ├── CMD            Command Palette (Ctrl+K): fuzzy search, View/Export/App/Rule/Thread actions
    ├── BCB            Breadcrumb Context Bar: thread + search + view mode context chips
    ├── GANTT_RESIZE   Gantt label column drag-resize (100–480px), MutationObserver-attached
    ├── SEARCH_HL      Tree search highlight (<mark class="hl">) + match counter
    ├── SETTINGS_ADDITIONS  Performance + Appearance settings panels in S.appPrefs
    ├── ONBOARD        Onboarding Module: welcome overlay + demo Spring Boot parser sequence
    ├── HELP_WIRE      Help Panel tab switching & LQL click-to-run queries
    ├── HTIP           Contextual Help Tip Popover component
    ├── OVR_MENU       Header Overflow Menu for compact viewports
    └── RESP_SB        Responsive Sidebar drawer + mobile triggers
```

### Config Schema (JSON)
```json
{
  "globalSettings": {
    "appName": "string",
    "globalTimestampPattern": "regex string",
    "description": "string"
  },
  "elementRules": [{
    "id": "string",
    "name": "string",
    "regexPattern": "string",
    "captureMapping": { "1": "timestamp", "2": "thread", "3": "elementName", "4": "payload" },
    "stackBehavior": "push | pop | inline",
    "visualStyle": { "accentColor": "#hex", "icon": "emoji" }
  }]
}
```

### Stack Behavior Model
- **push** — opens a timed block (pushed onto per-thread stack)
- **pop** — closes last block, computes `duration = popTimestamp - pushTimestamp`
- **inline** — standalone point event, no duration

### Parse Engine (Web Worker)
- Processes log file in 512 KB chunks via `FileReaderSync`
- Per-thread stacks produce nested event trees
- Hotspot badges: `_hp` = % of parent duration; `_sm` = self-time (excluding children)
- Thread discovery (scan) reads first 200 KB only

---

## UI Layout

```
┌─────────────────────────────────────────────────────────┐
│ HEADER: Logo | "FS API ✓" | "Config" | "File" | Theme   │
├──────────────┬──────────────────────────────────────────┤
│ SIDEBAR      │ CONTROL BAR: [Select File] [Thread] [Parse]│
│ ─────────    ├──────────────────────────────────────────┤
│ ⚙ Config     │ PROGRESS BAR (hidden when not parsing)    │
│ 🔧 Settings  ├──────────────────────────────────────────┤
│ 📄 Log4j     │ VIEW TABS: ⊞ Split | 📊 Timeline | 🌳 Tree│
│ ❓ Help      ├──────────────────────────────────────────┤
│              │ RESULTS AREA                              │
│ Config DB    │   Stats bar (file size, lines, threads,   │
│ + rules list │   nodes, parse time)                      │
│              │   [Gantt | Tree | Split view]              │
└──────────────┴──────────────────────────────────────────┘
```

---

## Design System

| Token | Dark | Light |
|-------|------|-------|
| `--bg-0` | `#060a0f` | `#edecea` |
| `--bg-1` | `#0d1117` | `#f8f7f5` |
| `--amber` | `#f0883e` | `#b45309` |
| `--blue` | `#58a6ff` | `#2563eb` |
| `--green` | `#3fb950` | `#16a34a` |
| `--red` | `#f85149` | `#dc2626` |
| `--ui` | Inter / system | same |
| `--mono` | JetBrains Mono | same |

**CSS naming**: `.btn`, `.btn-p` (primary/amber), `.btn-d` (danger), `.btn-bl` (blue)

### What's Already Implemented (v6.0 baseline)
- [x] Dark/light theme toggle (localStorage)
- [x] Collapsible sidebar with 4 tabs (Config, Settings, Log4j, Help)
- [x] Configuration DB: connect via File System Access API, import JSON, export, create new
- [x] Rule management: add/edit/delete rules via modal dialog
- [x] Two rule creation modes: Guided (Keyword Wizard) + Advanced (full regex)
- [x] Log4j XML parser: Log4j 1.x, 2.x, Logback → auto-generates regex patterns
- [x] Token Palette: click-to-insert regex tokens with live match preview
- [x] Keyword Wizard: step-by-step guided rule creation with live preview
- [x] Web Worker parsing engine: streaming 512 KB chunks, thread isolation
- [x] Thread discovery: scan first 200 KB to identify thread IDs
- [x] Waterfall Gantt chart (innerHTML-based)
- [x] Execution Tree (collapsible details/summary with flat virtual scroll renderer)
- [x] Split view: resizable panes
- [x] Hotspot badges: ↑↑80% style severity indicators
- [x] Stats bar: file size, lines, threads, nodes, parse time, rule coverage meter
- [x] Thread chips for switching between threads
- [x] Sample log download (2-thread demo)
- [x] Keyboard shortcuts: Alt+T (theme), Alt+1/2/3 (views), Alt+[/] (threads), Esc
- [x] Toast notifications (success/error/info/warn)
- [x] Header status badges (FS API, Config, File)
- [x] WebSocket log tail (real-time streaming parsing and throttled rendering)
- [x] Elasticsearch / OpenSearch query integration fetch client
- [x] Grafana Loki (LogQL query range API fetch client)
- [x] AWS CloudWatch Logs query integration via SigV4 signed REST client
- [x] Git rule configuration raw URL sync client
- [x] File System Access API directory watcher with auto-reload polling
- [x] Rule versioning changelog and side-by-side Config Diff viewer
- [x] JIRA issue creation webhook and fallback ticket link generator

---

## Roadmap Progress

### Phase 1 — Foundation Hardening (v2.x) · Now → Month 3
**Status: Complete**

#### Performance
- [x] Virtual scroll tree — render 50k+ nodes without DOM thrashing
- [x] Streaming chunk size auto-tuning based on file size and browser memory hint
- [x] IndexedDB result cache — reload tab without re-parsing
- [x] Native gzip/zstd decompression via `DecompressionStream` (gzip complete, zstd offline proxy recommended)

#### File Handling
- [x] Multi-file session — merge logs from N nodes into unified timeline
- [x] Drag-and-drop log files onto any surface
- [x] File System Access API directory watcher — auto-reload on file change

#### Export Surface
- [x] Self-contained HTML report (Gantt + tree embedded, shareable)
- [x] CSV export of all parsed events
- [x] SVG/PNG export of Gantt chart
- [x] JSON export of full parsed event tree

#### Config & Rules
- [x] Rule test suite — batch test rules against sample line set
- [x] Config versioning — embedded changelog, diff view
- [x] Import/export individual rules as JSON snippets
- [x] Rule ordering UI — drag-and-drop priority

#### UX Polish
- [x] Pin/bookmark events with sticky notes
- [x] Right-click context menu on tree nodes
- [x] Keyboard-driven navigation (j/k//)
- [x] Saved parse sessions (reopen without re-selecting files)

**Phase 1 Target:** Handle 500 MB logs in <10s on mid-range laptop; shareable reports without installing anything.

---

### Phase 2 — Intelligence Layer (v3.0) · Month 3–6
**Status: Complete**

- [x] Per-rule latency distribution (P50/P95/P99/max)
- [x] Histogram panel — duration buckets as micro bar chart
- [x] Multi-session comparison (diff P95 latencies)
- [x] Statistical outlier flagging (events >2σ)
- [x] Quiet-period detection
- [x] Error cascade analysis
- [x] Configurable SLA thresholds per rule
- [x] Trace ID linking — cross-thread logical traces
- [x] Transaction dependency graph
- [x] Unparsed line analyzer — suggest new rule candidates
- [x] Frequency heatmap
- [x] Coverage meter
- [x] Swimlane view — parallel thread lanes
- [x] Zoom/pan on Gantt
- [x] Critical path highlighting
- [x] Mini-map navigator

---

### Phase 3 — Collaboration (v4.0) · Month 6–12
**Status: Complete**

- [x] Community rule packs (import from URL)
- [ ] Organisation registry / pack server
- [x] Sticky notes on tree nodes
- [x] Named analysis sessions (.lls files)
- [x] PDF report generator
- [x] Interactive HTML standalone report
- [x] Config stored in Git repo
- [x] Branch-based rule isolation
- [x] Config diff viewer

---

### Phase 4 — Integration (v5.0) · Month 12–18
**Status: Complete**

- [x] WebSocket log tail (real-time parsing)
- [x] Elasticsearch / OpenSearch query integration
- [x] Grafana Loki (LogQL → LogLens)
- [x] AWS CloudWatch Logs direct query
- [x] JIRA issue creation from anomalies
- [ ] REST API (headless parse endpoint)
- [ ] CI/CD integration (GitHub Action / Jenkins plugin)

---

### Phase 5 — Platform (v6.0) · Month 18–24
**Status: Complete**

- [ ] Tauri desktop app (Rust + WebView, <10 MB)
- [x] CLI tool (`loglens parse --config rules.json app.log`)
- [x] Plugin SDK (JS/WASM modules)
- [ ] Rust/WASM parser core (10–20× throughput)
- [ ] Enterprise edition (SSO/SAML, RBAC, audit logging)

---

## Key Files

| File | Purpose |
|------|---------|
| `loglens.html` | The entire application (CSS + HTML + JS, ~2000 lines) |
| `loglens-roadmap.html` | Product roadmap reference (do not modify) |
| `.agents/AGENTS.md` | Agent behavioral rules for this project |
| `.agents/PROJECT_CONTEXT.md` | This file — always read first |
| `.agents/GRAPHIFY_INTEGRATION.md` | Graphify (d3.js) integration plan — read before any visualization work |
| `.agents/skills.json` | Skills registration — activates `claude-d3js-skill` for this project |


---

## Competitive Position

LogLens uniquely combines:
1. **100% local** — no cloud, no telemetry, logs never leave the browser
2. **Metadata-driven** — JSON config rules, not ad-hoc grep
3. **Zero install** — single HTML file, open in browser
4. **Gantt + hotspot** — execution timeline that immediately shows bottlenecks
5. **Log4j import** — auto-converts existing logging config to regex rules

Competitors (Splunk, ELK, Datadog) require infrastructure and send data to servers. Desktop viewers (glogg) have no structured analysis. Jaeger/Zipkin require code instrumentation. LogLens needs none of these.

---

## Graphify Integration

Graphify is attached to this project and should be used for:
- Visualizing parse result statistics (histograms, P-latency charts)
- Rendering the transaction dependency graph (Phase 2)
- Generating shareable charts for the export surface (Phase 1)
- Any data visualization beyond the current Gantt/Tree that benefits from a graph representation

---

*Last Updated: 2026-06-29*  
*Updated By: Antigravity (Search Layout Fix & Thread Selector Dropdown Conversion v6.9.10)*
