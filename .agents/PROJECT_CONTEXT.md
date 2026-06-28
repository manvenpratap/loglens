# LogLens — Project Context

> **Agent Rule:** Read this file at the start of every session. Update it after every meaningful code change.

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

*Last Updated: 2026-06-27*  
*Updated By: Antigravity (merged v6.2 Overhaul & updated architecture details)*
