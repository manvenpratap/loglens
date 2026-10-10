# LogLens — Project Context

> **Agent Rule:** Read this file at the start of every session. Update it after every meaningful code change.


- **Impeccable Design System Consistency & Zero-Antipattern Polish (v6.9.99 — COMPLETED)**:
  - **Zero Radius Token Drift (`design-system-radius: 0`)**: Normalized all off-ramp radii (2px, 3px, 4px, 5px, 16px, 20px, and `calc(var(--rounded-md) - 2px)`) across all CSS rules, dynamic elements, and JavaScript string templates (`rg-hover-hl`, unparsed mark backdrops, `stream-prog-card`, `vtabs-pill`, `.rules-count-badge`, `.rule-toggle-track`) to semantic design tokens (`--rounded-sm: 6px`, `--rounded-md: 8px`, `--rounded-full: 99px`).
  - **Eliminated AI-Slop Visual Antipatterns**:
    - **`side-tab: 0`**: Replaced 2px side-border tab accents (`border-left: 2px`) on sidebar tabs (`.sb .stab`) and command items (`.cmd-item`) with native macOS-style background highlights (`var(--amber-d)`) and rounded pill indicators.
    - **`pulsing-dot: 0`**: Removed infinite looping pulse keyframes on `.hdr-live .dot` and `#hdr-live-badge span.dot`, converting live status dots to calm, solid telemetry indicators.
    - **`dark-glow: 0`**: Eliminated colored neon blur box-shadows across timeline bars (`.g-bar.g-outlier`, `.g-bar.g-sla-breach`, `.g-bar.g-critical`), config dots (`.cfg-dot.live`, `.cfg-dot.imp`), token hovers (`.tok:hover`), scrubber guides, and minimap thumbs (`#ll-minimap-thumb`), restoring clean developer console elevation.
  - **Badges & Color Normalization**: Replaced 6 hardcoded RGBA badge borders with a single semantic `border: 1px solid color-mix(in srgb, currentColor 28%, transparent)` on `.badge`, and normalized `--red` lightness in `:root` to 63.5% for WCAG AA compliance (≥4.5:1).
  - **Full Regression Test Suite Passed**: All 111 tests passing across dark and light/ivory themes with zero regressions.

- **Split View Baseline Alignment, Zero-Overflow Toolbar & Apple Chevrons (v6.9.98 — COMPLETED)**:
  - **Symmetric Full-Height Card Geometry**: Converted `.gw` (Waterfall container) and `.tw` (Execution Tree container) into `display: flex; flex-direction: column; height: 100%; min-height: 0; box-sizing: border-box;` and `.gw .g-rows` to `flex: 1; min-height: 0; max-height: none;`. Eliminated the 259px vertical empty-space mismatch where `.gw` stopped prematurely at 342px while `.tw` filled 601px.
  - **Exact 38px Baseline Toolbar Alignment**: Aligned `.pt.g-toolbar` (Waterfall) and `.tw .pt` (Execution Tree) to exactly 38px height (`min-height: 38px !important; height: 38px !important; box-sizing: border-box !important; padding: 6px 12px !important; background: var(--bg-2); border-bottom: 1px solid var(--bdr); font-size: 12px; font-weight: 600; font-family: var(--ui)`), eliminating the previous 18px toolbar height disparity.
  - **Eliminated Horizontal Toolbar Overflow**: Condensed toolbar controls in `.pt.g-toolbar` (`Waterfall`, `Swimlane`, unified badge `${fmtMs(rd)} · ${rows.length} spans`, `✦ Critical`, compact zoom slider and icon, `Fit`, `Reset`), bringing total toolbar width from 803px down to 670px, completely eliminating line wrapping and clipped buttons in 50% split view (`clientW: 670, scrollW: 670`).
  - **Native Apple SVG Divider Chevrons**: Replaced raw unicode text (`◀` and `▶`) on `#sp-hdl` collapse buttons with inline vector SVG chevrons (`M5 1L1 5l4 4` and `M1 1l4 4-4 4`). Upgraded `.sp-hdl-btn` to 18px width, 28px height, `var(--rounded-md)` border radius, smooth hover scale (`scale(1.08)`), and active press state (`scale(0.92)`).
  - **Calibrated Button Hover & Caption Contrast**: Refined `.btn-d:hover` to `oklch(50% 0.20 25)` / `oklch(46% 0.20 25)` and `.btn-bl:hover` to `color: var(--bg-0)` in dark themes and `oklch(46% 0.18 250)` with `#fff` in light themes. Lifted secondary text token `--t4` to `oklch(62% 0.012 55)` in `:root` and `oklch(44% 0.01 55)` in light/ivory themes, achieving WCAG AA (≥4.5:1) compliance across all themes.
  - **Full Regression Test Suite Passed**: All 111 regression tests passing with 0 errors across dark and light/ivory themes.

- **Stats View Top Header Bar Squashing & Text Truncation Fix (v6.9.97 — COMPLETED)**:
  - **Eliminated Flex-Shrink Squashing on `#stats-bar`**: Fixed root cause where `#stats-bar` defaulted to `flex-shrink: 1` inside flex container `#res`. When the Stats view child height exceeded viewport height (e.g., 1860px), flexbox squashed `#stats-bar` down to 26px and `overflow: hidden` clipped all metric values and labels, rendering a half-visible empty bar with only vertical dividers. Added `flex-shrink: 0 !important;` to `.stats` and `.res-summary-cards`.
  - **Pristine Grouped Card Cell Padding**: Removed outer padding (`padding: 0 !important;`) on `.stats` and styled `.sc` cells with `padding: 10px 14px !important; gap: 4px !important;`, allowing vertical dividers to extend seamlessly from top to bottom border in true Apple grouped style.
  - **Full Regression Test Suite Passed**: All 111 regression tests passing across both dark and light/ivory themes with zero regressions.

- **Summary Stat Cards Real-Estate Optimization (v6.9.96 — COMPLETED)**:
  - **Restricted Summary Cards to Stats View**: Restricted `#res-summary-cards` ("Slowest Operation", "Rules Coverage", "Active Threads") exclusively to the dedicated Stats dashboard (`S.viewMode === 'stats'`).
  - **Reclaimed 130px+ Vertical Real Estate**: In Split View (`split`), Gantt/Timeline (`gantt`), and Tree (`tree`), the 3 bulky summary stat cards are automatically removed, restoring full viewport height to the execution tree, waterfall lanes, and zoom timeline without vertical crowding.
  - **Uncompromised Quick Metrics**: Kept `#stats-bar` parse metric strip (File Size, Lines, Coverage, Threads, Nodes, Outliers, Parse Time) intact across analytical views for baseline performance metrics.
  - **Full Regression Test Suite Passed**: All 111 tests passing across both dark and light/ivory themes with zero regressions.

- **Apple Human Interface Guidelines (HIG) Polish across All Views, Modals & Spotlight (v6.9.95 — COMPLETED)**:
  - **Apple Sheet Elevation & Double-Layer Shadows**: Upgraded `.modal` and `.cmd-box` with double-layer macOS sheet depth (`box-shadow: 0 0 0 1px rgba(255,255,255,.07), 0 24px 64px -12px rgba(0,0,0,.55), 0 12px 28px -6px rgba(0,0,0,.35)`) and smooth Apple spring entrance animation (`cubic-bezier(0.16, 1, 0.3, 1)`). Added calibrated light-mode perimeter shadows (`0 0 0 1px rgba(0,0,0,.08)`) with soft diffusion.
  - **Frosted Translucent Backdrops**: Applied macOS frosted backdrop blur (`backdrop-filter: blur(14px) saturate(160%)`) to all modal overlays (`.mm`, `.sh-ov`, `.cmd-ov`), floating HUD toolbars (`.graph-hud-toolbar > div`, `#graph-hover-card`, `#ld3-overlay`), and popovers (`.quick-edit-pop`).
  - **Apple Circular 26px Close Buttons**: Unified all dialog close buttons (`#btn-mx`, `#btn-shc`, `#btn-ann-close`, `#btn-ins-close`, `#od-close`, `#htip-pop-close`, and dynamic dialog close buttons) into 26px circular buttons with centered `✕`, subtle borders, smooth hover scale (`transform: scale(1.06)`), and active press state (`scale(0.94)`).
  - **San Francisco Native Typography Stack**: Unified `--ui`, `--display`, and `--mono` tokens across `:root` and all 6 themes to prioritize `-apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "SF Pro", "SF Mono"`, delivering native Apple typography with zero runtime font downloads.
  - **Spotlight Command Palette Overhaul**: Upgraded `#cmd-palette` to 620px width, 16px search input with seamless outline-free active row, 8px rounded item highlights, and keyboard hint pills (`.cmd-kbd`).
  - **macOS System Settings Grouped Cards**: Styled `.dashboard-card` with 14px border radius (`var(--rounded-lg)`), hairline borders, subtle double depth, and clean 13px semi-bold headers.
  - **Native macOS Segmented Controls & Toggles**: Transformed Help view tabs (`.hlp-tabs`) and modal toggles (`.m-tog`) into macOS segmented controls with 8px pill wrappers and smooth active states. Enhanced toggle switches (`.toggle-sw`) with 14px white drop-shadowed thumbs and Apple spring easing.
  - **Trace Explorer & Event Inspector Drawer**: Polished Trace Explorer KPI cards, rounded list rows, and pill thread badges. Refined Event Inspector drawer (`#event-inspector`) with elevation shadow, hairline border, and clean metadata cards.
  - **Full Regression Test Suite Passed**: All 111 tests passing across both dark and light/ivory themes with zero regressions.

- **Timeline & Observability UI-UX Overhaul (v6.9.94 — COMPLETED)**:
  - **Eliminated Corrupted Vertical Swimlane Text**: Fixed root cause in `.swim-lane-hdr` where `writing-mode: vertical-rl;` rotated labels 90° vertically, causing characters to overflow into neighbor rows and create garbled illegible text (`:RNKKRRNKKR...`). Replaced with `writing-mode: horizontal-tb !important;`, flex spacing, font-size 11px, `trunc` title wrapper, and right-aligned pill badges (`.badge b-gray`).
  - **Consolidated Dual Toolbars into Unified Single Row**: Merged redundant 72px dual-row toolbars (`#g-zoom-ctrl-row` and `.pt`) into a single compact 38px `.pt.g-toolbar` across both Waterfall and Swimlane views. Restored 34px+ of vertical timeline real estate while retaining all controls: view mode toggle, thread/span count badges, Group by Rule checkbox, Lane Height slider, Critical Path checkbox, Time Zoom slider with direct readout, and Fit/Reset actions.
  - **Replaced Static Stuck Scrubber with Interactive Crosshair Guide**: Replaced the static 250px vertical line and colliding `0.00ms` ruler badge (which was inappropriately bound to vertical scroll) with an on-demand hover crosshair that cleanly tracks mouse movements across tracks with precise millisecond tooltips and vanishes when idle.
  - **Fixed 99% Stuck Progress Bar**: Ensured `UI.hprog` reliably sets `$('prog-p').textContent = '100%'` upon completion, shortened dismiss timeout to 400ms, and eliminated hanging progress states.
  - **KPI Summary Card Visual Symmetry**: Added matching progress track (`.summary-card-progress-wrap` with `background-color: var(--amber)`) to Card 3 ("Active Threads"), aligning height and aesthetic structure with Cards 1 & 2.
  - **Toast Queue Management & Dismissal**: Capped maximum stacked toasts in `#toast-r` to 2, enabled click-to-dismiss (`cursor: pointer;`), and added `pointer-events: none` on `#toast-r` container with `pointer-events: auto` on `.toast` to prevent dead click zones.
  - **Full Regression Test Suite Passed**: 111 passed / 111 total across both dark and light/ivory themes with zero regressions.

- **Graphify Dependency Graph Legibility & Pipeline Architecture Layout (v6.9.93 — COMPLETED)**:
  - **Overcame Visual Overlap & Knot Topology**: Solved dense clustering, label collision, and tangled cross-links in the transaction dependency graph. Transformed chaotic force distribution into an intuitive, high-clarity distributed service architecture layout.
  - **Hierarchical Microservice Pipeline (`assignClusterAnchors`)**: Structured primary business flows into distinct, readable service swimlane columns:
    - *Order Service (`worker-1`)* on the Left (`ProcessOrder/42` → `/api/checkout` → `auth.lookup`).
    - *Payment & Refund Service (`worker-2`)* in the Center (split streams for Checkout Payment and Refund `order.lock`).
    - *Inventory Service (`worker-3`)* on the Right (split streams for Inventory Reservation and Reconcile scan).
    - Cross-thread links (red dashed lines) flow strictly left-to-right (`auth.lookup` → `ProcessPayment/8921` and `/api/payment/charge` → `ReserveInventory/8921`).
  - **Dedicated Background Worker Shelf**: Positioned isolated batch tasks (`worker-4` through `worker-16`) along an organized bottom rack with alternating row elevations, ensuring all 13 worker pairs (`TaskRun/N` → `task.process.N`) have zero link crossings and unobstructed labels.
  - **General-Purpose Layered Fallback**: Built a Sugiyama/layered topological BFS layout for arbitrary user logs, grouping nodes by root distance (`rank`) and thread lanes.
  - **Physics Relaxation & Spring Bug Resolution (`drawNativeGraph`)**:
    - Fixed inverted spring velocity signs (`a.vx += fx`, `b.vx -= fx`) that previously acted as explosive catapults throwing linked nodes to canvas boundaries `(50, 50)` and `(W - 50, H - 50)`.
    - Replaced unstable Coulomb $1/r^2$ repulsion with soft linear repulsion (`dist < 85`), ensuring stable convergence without numerical jitter.
  - **Cross-Thread Ancestor Resolution (`buildGraph`)**: Enhanced correlation link tracking to traverse parent hierarchies (`_parent`) when linking non-push events (e.g. `CACHE-HIT` stripe idempotency events), resolving real microservice call endpoints without orphan link origins.
  - **Automatic Viewport Centering & Framing (`fitView`)**: Added automatic bounding-box scaling and centering on initial load across both D3 and native engines, preventing edge cropping and manual zoom requirements.
  - **SVG Text Halo & Interactive HUD Controls**: Added SVG text halo casing (`stroke: var(--bg-1); stroke-width: 4px; paint-order: stroke fill;`) across all labels, live node search filtering, zoom buttons, interactive 1st-degree neighborhood focus dimming, and an interactive category-grouped legend.
  - **Full Regression Test Suite (111 tests passing)**: Verified with full automated test suite (`./run_tests.sh`) with 0 regressions and 0 console errors.

- **Zero-Dependency Native Graphify Offline Fallback Engine (v6.9.92 — COMPLETED)**:
  - **Graceful Offline Degradation**: Eliminated fatal `TypeError: Failed to fetch dynamically imported module` errors, unhandled exceptions, and dead states (`⚠ Graphify unavailable offline.`) when LogLens runs offline or in air-gapped / CDN-restricted enterprise environments without internet access to `cdn.jsdelivr.net`.
  - **Native SVG Dependency Graph (`drawNativeGraph`)**: Built a zero-dependency SVG transaction dependency graph with deterministic physics relaxation (80 iterations), directional arrows, cross-thread dashed links (`var(--red)`), dynamic self-time circle radius scaling with metadata tooltips, labels, interactive pan (`isPanning`), SVG matrix-inverse coordinate drag-and-drop (`pt.matrixTransform(mainG.getScreenCTM().inverse())`), and wheel zoom (0.2x to 5x).
  - **Native Latency Histogram (`drawNativeHist`)**: Built a zero-dependency SVG latency histogram computing 20 linear duration bins with coordinate axes, bar rects, and tooltips, supporting 1-click SVG export without requiring D3.
  - **Native Temporal Density Heatmap (`drawNativeHeatmap`)**: Built a zero-dependency SVG heatmap grid over 10 temporal buckets with dynamic opacity ramps and time-offset labels.
  - **Silent Network Fallback**: Cleanly catches D3 network import failures without emitting console errors, automatically and seamlessly rendering native visualizations across Graph, Latency Histogram modals, and Heatmaps.
  - **Full Regression Test Suite (111 tests passing)**: Added `test_graphify_offline_fallback` in `tests/test_20_demo_showcase.py` simulating air-gapped environments by aborting CDN requests, asserting native SVG graph node rendering, histogram modal rendering, and 0 console/runtime errors. Full suite of 111 tests passing with 0 regressions.

- **Comprehensive Demo Showcase across All Features (v6.9.91 — COMPLETED)**:
  - **Full-Spectrum Demo Log & Configuration Overhaul**: Enhanced the built-in demo (`ONBOARD.loadDemo()`, "Load Demo Log", "Try Demo", and `dlSample()`) to comprehensively showcase every primary capability of LogLens with realistic multi-service distributed transactions.
  - **Distributed Tracing & Trace Explorer Integration**: Configured `DEMO_CFG` to capture group 4 as `correlationId` across all element rules (`(?:\s+\[(?:traceId=)?([^\]]+)\])?`), generating multi-thread distributed transactions (`trace-ord-8921` spanning `worker-1`, `worker-2`, and `worker-3`, `trace-pay-3310`, `trace-inv-4091`). Trace Explorer displays active trace rows, span counts, inter-thread links, and duration metrics.
  - **Graphify Dependency Graph Activation**: Connected cross-thread `correlationId` links automatically generate service dependency arrows in the `Graph` tab, visualizing communication topology from API Gateway to Payment and Inventory services.
  - **Multiline Block Payloads**: Injected rich real-world payloads with preserved formatting and indentation:
    1. Printed class payload: `class OrderCheckoutRequest { customerId: "cust-9481", items: [...], paymentMethod: "CREDIT_CARD" }` on `/api/checkout`.
    2. Formatted JSON webhook: `{ "event": "charge.initiated", "gateway": "stripe", "amount": 11948 }` on `/api/payment/charge`.
    3. Multiline SQL exception stack trace: `java.sql.SQLException: Deadlock detected in InnoDB lock table` with preserved `Caused by: com.mysql.cj.exceptions.DeadlockException` chain on the `OrderService` error.
  - **SLA Thresholds & Breach Detection**: Configured `slaThresholdMs: 250` on HTTP requests and `slaThresholdMs: 150` on DB queries in `DEMO_CFG`. Automatically populates `#hdr-sla` badge (`4 SLA`), renders `SLA BREACH` badges in the tree, and highlights breaches in the Event Inspector.
  - **Latency Outlier & Anomaly Detection**: Configured realistic duration spikes (850ms database lock contention and 1400ms inventory reconciliation), activating `ANOMALY.analyze()` IQR detection to light up `#hdr-outliers` (`2 Outliers`) and AI Insights outlier inspection cards in Stats.
  - **Pre-Seeded Sticky Notes / Annotations**: Pre-seeded markdown annotations (`S.annotations`) with author metadata on the critical error node and slow query node, immediately displaying the `📝` note badge in Tree view and sticky note cards in Event Inspector.
  - **Multi-Thread & 3D Landscape Terrain**: Generates 16 concurrent threads (`worker-1` through `worker-16`), producing rich swimlanes in Gantt and multi-level latency topology in the 3D Landscape view.
  - **Full Regression Test Suite (110 tests passing)**: Created `tests/test_20_demo_showcase.py` containing 6 automated E2E tests validating multi-thread tree loading, distributed traces, multiline block payloads, SLA and outlier badges, pre-seeded annotations, and all-view navigation. Full suite of 110 tests passing with 0 regressions.

- **Event Inspector Context-Aware Auto-Close (v6.9.90 — COMPLETED)**:
  - **Auto-Close on Irrelevant Views**: Eliminated persistent drawer obstruction when switching away from log exploration. In `INSPECTOR.syncVisibility(vm, thread)` and `UI.svm(vm)`, the drawer automatically closes when navigating to non-event views (`Settings / cfg`, `Help / hlp`, `Stats / stats`, `Graph / graph`, `3D / 3d`, `Query / query`, `Diff / diff`) or when in empty state (`!S.trees || S.activeThr === null`).
  - **Thread-Aware Auto-Dismissal**: In `UI.sw(tid)`, if the active inspected event belongs to a different thread (`_activeNode.thread !== tid`), the inspector closes automatically so stale events from inactive threads do not persist into the newly selected thread view.
  - **Blank Space / Canvas Deselect**: Clicking empty space in the Tree container (`#tree-vscroll`) or Timeline rows (`.g-rows`) automatically deselects the active row and hides the inspector drawer, clearing `.kb-focus` and `.g-selected` highlights.
  - **New Parse & Reset Dismissal**: When new log data is parsed or loaded via `UI.render(...)`, or when resetting configuration, previously open event inspectors are closed immediately.
  - **Extended Regression Suite (104 tests passing)**: Added 3 new automated Playwright tests to `tests/test_05_event_inspector.py` asserting auto-close across view switches (Settings, Help, Stats), thread transitions, and empty background clicks. Full suite of 104 tests passing with 0 regressions.

- **Multiline Block & Class Payload Parsing (v6.9.89 — COMPLETED)**:
  - **Single Payload Identification for Multiline Blocks**: Enabled automatic block accumulation in Web Worker parser (`W_SRC`) and streaming parser (`STREAM_PARSER`). When log files contain multiline blocks (e.g., printed Java/Python classes, object dumps, multiline formatted JSON/XML payloads, exception stack traces with `Caused by` chains), non-header continuation lines are identified and accumulated into the parent event's `payload` property as a single formatted unit.
  - **Intelligent Header Discrimination Algorithm (`isLogHeader`)**: Built timestamp and log-prefix detection (`DEF_TS_RX`) that accurately separates true log event boundaries from continuation lines containing internal dates (e.g. `createdAt: 2026-10-09`), preventing false block truncation.
  - **Accurate Line Accounting & Adaptive Rescue Shield**: Continuation lines belonging to an active block are counted towards `matchedLines` and excluded from `unparsedSample`, eliminating false-positive Adaptive Rescue warnings on logs containing large class dumps.
  - **Memory-Safe Streaming**: Preserves line indentation and line breaks with an automatic 64KB safety cap per payload block to prevent worker OOM on malformed logs.
  - **UI & Formatting Preservation**: Added `white-space: pre-wrap;` to `.tpy` (Tree view), `.ins-payload-pre` (Event Inspector), and `.od-payload` (Overlay detail view) ensuring indentation and newlines are rendered verbatim without collapsing.
  - **Configurable Global Setting**: Added `multilinePayloads: true` to `globalSettings` with a toggle in Card 3 (Global Settings) UI (`#gs-multiline`) allowing zero-overhead opt-out.
  - **Full Regression Test Suite (101 tests passing)**: Created `tests/test_19_multiline_block_payload.py` with 6 automated E2E tests validating printed class payload capture, exception stack trace aggregation, multiline JSON blocks, opt-out setting toggles, DOM whitespace styling, and clean interleaved multi-thread boundaries. Full suite of 101 tests passing with 0 regressions.

- **Custom Log Pattern Journey & Defect Elimination (v6.9.88 — COMPLETED)**:
  - **Zero-Friction Custom Pattern Rule Setup**: Streamlined the user journey for parsing custom lines of logs across 3 distinct workflows:
    1. *Empty-State Discovery*: Added prominent `[+ Custom Rule Builder]` button directly on `#emp` empty-state cards (both initial static load and dynamic `UI.svm` navigation), allowing immediate 1-click rule authoring without needing to search Settings.
    2. *Interactive Regex Builder (`RG` & `RXB`)*: Cleaned recognizer patterns (`Thread name`, `Request ID`, `key=value`, `Hashtag`, `Hour`, `Minute`, `Day`, `Month`, `Square brackets`, `Parentheses`, `Curly braces`) to use non-capturing groups `(?:...)` and unescaped brackets, fixing nested capture group numbering and restoring exact 1:1 token-to-capture-mapping alignment (`#cm-ts`, `#cm-th`, `#cm-lv`).
    3. *Live Visual Feedback & Badging*: Synchronized `RG.buildRegex()` with `RXB.update()` to instantly update live match highlighting (`#rx-pre`) and Visual Group Mapping Guide pills (`#cap-diagram-pills`). Added `badge b-amber` (`Format: Custom Pattern`) badge recognition for non-standard log lines.
    4. *Rule Test Suite (`RTS`)*: Enabled `#btn-rule-test` dynamically when rules exist, allowing users to test multi-line custom snippets with safe per-rule evaluation before running on large files.
    5. *Preserved Utility Panels in DOM*: Fixed critical root cause where `UI.svm()` transitioning to empty state destroyed `#p-cfg` and `#rules-list` from `innerHTML = ''`, causing subsequent rule creation and `CFG.rl()` calls to crash with `Cannot set properties of null`.
  - **Comprehensive Regression Suite (95 tests passing)**: Created `tests/test_18_custom_log_pattern_journey.py` covering empty-state discovery, token selection, group mapping, Rule Test Suite execution, custom file parsing, and adaptive rescue workflow. Full suite of 95 tests passing with 0 regressions.

- **File-Based Rule Retention & Live File Sync (v6.9.87 — COMPLETED)**:
  - **Replaced `localStorage` with Direct File Persistence**: Eliminated origin-bound `localStorage` rule retention in favor of dedicated File System persistence. Active rules, capture mappings, and synthesized patterns are saved directly to `.json` configuration files on disk with real-time live sync.
  - **Explicit Save to File Action**: Added `[Save to File]` in Settings Card 2 and `CFG.saveToFile()`, leveraging native File System Access API (`showSaveFilePicker`) to create and connect files on disk, or exporting directly via clean download fallback.
  - **Live File Sync via `S.cfgHandle`**: Connected files automatically receive every rule update, addition, deletion, and auto-learned rescue rule via `createWritable()` without manual export steps.
  - **Adaptive Rescue Save-to-File Integration**: Updated rescue banner action to `[+ Auto-Add Rule & Save to File]`, writing new learned pattern rules straight into the connected file on disk.
  - **Regression Test Coverage**: Updated `tests/test_17_auto_detect_and_retention.py` to assert file handle writing, live sync, and file picker fallbacks. Full suite of 90 tests passing.

- **Auto-Pattern Sniffer & Adaptive Rescue (v6.9.86 — COMPLETED)**:
  - **Zero-Config Pre-Flight Sniffer (`SNIFFER`)**: Automatically samples dropped or selected log files (up to 50 lines), detects format signatures (`spring`, `java_std`, `log4j2_t`, `json`, `csv`, or generic timestamps), synthesizes complete baseline parsing rules (Transaction Start/Push, Transaction End/Pop, Error/Inline, Event/Inline), and automatically begins parsing with zero configuration required.
  - **Inline Adaptive Rescue Banner**: Detects when unparsed log lines exceed 15% during parsing, mounting a top rescue dock (`#res-top-dock` / `.rescue-card`) displaying the dominant unmatched signature with 1-click `[+ Auto-Add Rule & Save to File]` (instant rule learning and immediate re-parse) or `[Custom Regex]` (pre-populates Rule Creator modal).
  - **Settings Reset Control**: Added `[Reset Defaults]` in Settings Card 2 to safely reset the workspace to factory defaults.

- **Developer Console Aesthetic & Glassmorphism Elimination (v6.9.85 — COMPLETED)**:
  - **Eliminated Heavy Glassmorphism & Backdrop Filters**: Removed all `backdrop-filter: blur(...)` across the entire application — including header (`.hdr`), modal overlays (`.mm`, `.sh-ov`, `.cmd-ov`), contextual dropdown menus (`#ctx-menu`), drag-and-drop overlays (`#drop-ov`, `#drop-ov-inner`), timeline mini-maps (`#ll-minimap-wrap`), and 3D visual landscape controls/tooltips.
  - **Solid Developer Console Header**: Replaced translucent glassmorphism in `.hdr` across all 6 themes (Dark, Light, Ivory, Aurora, Midnight, Forest, Crimson) with a solid surface (`background: var(--bg-1); border-bottom: 1px solid var(--bdr); box-shadow: none;`), removing distracting bottom center amber gradient glowing accent lines (`.hdr::after`).
  - **Crisp Buttons & Solid Accents**: Replaced gradient fills and neon blur glows on primary action buttons (`.btn-p`), danger hover states (`.btn-d:hover`), and blue outlines (`.btn-bl:hover`) with solid tokens, crisp 1px borders, and subtle 1px/2px drop shadows. Updated Ivory theme primary button to solid amber with crisp dark/light contrast.
  - **Refined Selection & Row Highlights**: Replaced heavy 2px/3px colored left borders with crisp 1px outlines (`outline: 1px solid var(--amber-g); outline-offset: -1px; background: var(--amber-d)`) for selected Gantt timeline rows (`.g-row.g-selected`) and Trace Explorer active rows (`.trace-row-item.active-trace`).
  - **Restrained Progress Indicators**: Replaced animated gradient shimmer sweeps on `.prog-f` with clean, solid progress fills.
  - **Full Regression Suite Passed**: All 85 Playwright E2E tests verified and passing (0 regressions).


- **Impeccable Action 1: Typography & Shape Standardization across Themes (v6.9.84 — COMPLETED)**:
  - **Eliminated Font Family Drift**: Replaced theme font overrides (`Georgia, serif` in Light/Ivory, `Century Gothic` in Aurora, `Impact` in Midnight) with a unified high-clarity sans stack (`Inter, Geist, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`) for UI and display, and `JetBrains Mono / Consolas` for log data across ALL 6 themes.
  - **Eliminated Hardcoded Font Names in Views**: Replaced inline `'Space Grotesk'` and `'Geist'` references with semantic CSS custom properties (`var(--display)`, `var(--ui)`, `var(--mono)`).
  - **Standardized Border-Radius Tokens**: Unified component border-radius across all themes to `sm: 6px`, `md: 8px`, `lg: 10px`, `full: 99px`, removing brutalist `0px` in Light theme and extreme `20px` in Forest/Midnight.
  - **Detector Validation**: Completely eliminated all `overused-font` and `design-system-font` detector warnings.


- **Project Folder Cleanup & Documentation Assets Reorganization (v6.9.83 — COMPLETED)**:
  - **Removed Scratch & Junk Files**: Removed obsolete `scratch.js` (unreferenced test scratchpad), `.DS_Store` metadata files, and temporary test cache directories (`tests/__pycache__`, `.pytest_cache`, `.impeccable/critique`).
  - **Reorganized Loose Screenshots**: Moved all 9 unreferenced root screenshots (`header_vtabs_active.png`, `layout_with_footer.png`, and 7 `theme_*.png` files) into `docs/screenshots/` to keep root pristine.
  - **Reorganized Sample Files**: Relocated `log4j.xml` from the project root into `docs/samples/log4j.xml`.
  - **Full Regression Suite Passed**: All 85 Playwright E2E tests verified and passing.


- **Active Log & Parse Actions Control Well Redesign & Spacing Polish (v6.9.82 — COMPLETED)**:
  - **Recessed Control Well**: Redesigned `.cfg-action-dock` from an unstyled container with conflicting inline styles into an intentional, rounded control well with `border-radius: var(--rounded-md)`, `padding: 16px 20px`, `background: var(--bg-0)` in Ivory theme (`var(--bg-2)` in dark themes), and `border: 1px solid var(--bdr)`.
  - **Removed Conflicting Inner Drop Shadow**: Removed `.cfg-action-dock` from the global raised surfaces selector (`box-shadow: var(--shd) !important`), enforcing `box-shadow: none !important` to prevent unnatural dark drop shadows inside the parent card.
  - **Action Button Proportions & Alignment**: Removed the full-width stretch class (`wf`) from `#btn-parse` and standardized it with balanced proportions (`min-width: 140px; height: 36px; padding: 0 24px; font-weight: 700;`). Aligned `#btn-abort` to an identical 36px height, placing them side-by-side with a 12px gap.
  - **Keyboard Shortcut Affordance**: Added `(Ctrl+Enter)` shortcut indicator alongside parse buttons for keyboard accessibility.
  - **Eliminated Phantom Horizontal Line**: Removed default bottom border on `#file-chips` and added `#file-chips:empty { display: none !important; }`, preventing empty file-chip containers from rendering artifact lines across the dock.
  - **Split Button & Filename Polish**: Styled the Select File split button (`#btn-sel-wrap`) with a crisp white surface in Ivory theme and refined filename label typography.
  - **Full Regression Suite Passed**: All 85 Playwright E2E tests verified and passing.


- **Top Bar & Settings Menu Visual Polish & Ivory Theme Overhaul (v6.9.81 — COMPLETED)**:
  - **Top Bar View Tabs Uncapped**: Removed arbitrary `max-width: 50%` constraint from `.hdr .vtabs`, allowing all 10 navigation tabs (`Split`, `Timeline`, `Tree`, `Traces`, `Query`, `Stats`, `Graph`, `3D View`, `Settings`, `Help`) to render cleanly on desktop viewports without truncating `Settings` or hiding `Help`.
  - **Clean Active Tab Indicator**: Removed duplicate `border-bottom` on `.hdr .vt.active` and added `position: relative; z-index: 1;` so the sliding rounded `vtabs-pill` acts as the sole, crisp indicator without bottom border artifact lines.
  - **Ivory Theme Contrast & Depth Overhaul**: Rebalanced the Ivory palette (`--bg-0: 94.5%`, `--bg-1: 99%`, `--bdr: 75%`, rounded corners `4px`/`6px`/`8px`/`9999px`) to eliminate washed-out flat appearance and restore visual hierarchy.
  - **Settings Menu Inputs & Buttons Polish**: In Ivory theme, inputs and textareas now render in crisp white (`#ffffff`) with subtle inset shadows and clean borders instead of muddy dark grey slabs. Secondary buttons are styled as clean, tactile card buttons with hover elevation.
  - **Parse & Abort Button Height & State Alignment**: Standardized button heights in the Action Dock (32px), aligned `btn-abort` vertically, and replaced muddy disabled orange bar with a subtle, light-neutral disabled state.
  - **Segmented Datasource Controls**: Added CSS for `.ds-type-segmented` and `.ds-segment-btn` to turn raw browser buttons into modern segmented pill controls across all themes.
  - **Directory Watcher Checkbox Alignment**: Corrected `flex-direction: row` to ensure checkbox and label sit side-by-side horizontally instead of stacking awkwardly.
  - **Toast Notifications Polish**: Added solid card background with colored left border for toasts in Ivory theme, ensuring high-contrast readability.
  - **Full Regression Suite Passed**: All 85 Playwright E2E tests verified and passing.

- **Interactive Visual Match Badges Alignment & Hover Details Overlay (v6.9.80 — COMPLETED)**:
  - **Perfect Character Alignment**: Positioned visual match badges using parent wrapper `div` blocks (`.rg-match-badge-wrap`) styled in `ch` units inheriting the text container's 15px monospace font size, keeping them aligned with the sample log line.
  - **Overlapping Matches Merged**: Grouped matches by unique range `(start, end)`, assigning tracks to grouped blocks to eliminate redundant rows and visual badge overlapping.
  - **Premium Hover Options Overlay**: Added a CSS-driven popover panel (`.rg-match-details-overlay`) inside the badge wrappers. Hovering a badge displays all overlapping pattern choices for that segment (color-coded, with pattern name, regex string, and matched text preview), allowing users to toggle selections directly from the overlay.
  - **Olaf Naming Restored**: Standardized names to match Olaf Neumann's exact patterns (`Date`, `Time`, `ISO8601`, `DateTime`, `Log level`), ensuring test runner compatibility.
  - **E2E Test Success**: All 85 verification checks passed.

- **Olaf Neumann Recognizer Registry Rewrite (v6.9.79 — COMPLETED)**:
  - **Full 40-Recognizer Registry**: Completely rewrote `RG.findMatches()` to use a structured `RECOGNIZERS` array mirroring Olaf Neumann's `regex-generator.olafneumann.org` engine. Registry is lazy-built once via `_buildRecognizers()`.
  - **7-Tier Priority System**: Tier 0 (Log Semantics: ISO8601, space-sep timestamps, Log Level, Dotted Class Name, Thread Name in brackets, Method Signature, File Path, HTTP Status/Method, Request ID, key=value, Quoted Strings) → Tier 1 (UUID, IPv4, Email, Hashtag, URL-encoded, Hex Color) → Tier 2 (Date, Time components) → Tier 3 (Brackets, Strings) → Tier 4 (Numeric) → Tier 5 (Text) → Tier 6 (Character-level).
  - **Eliminated literal-per-word badges**: Generic Alphanumeric/Multiple chars patterns replace the old one-badge-per-word approach.
  - **Correct track sort**: Start-position ascending, span-length descending for ties (matches Olaf's layout exactly).
  - **Auto-map label expansion**: `buildRegex()` capture-mapping heuristics updated for new label names.

- **Interactive Selection Suggestions & Auto-Mapping (v6.9.78 — COMPLETED)**:
  - **Arbitrary Selection Scans**: Integrated text selection listeners on the sample log input (`#e-tl`). Highlighting any section immediately queries the `TOKS` dictionary for matches, offering matching presets and a literal escaping generator.
  - **Capture Map Auto-Population**: Tied selections directly to Step 2 (Custom Mappings). Adding an interactive pattern (e.g. Timestamp, Level, Thread) automatically writes the capture group index into the corresponding configuration field (`cm-ts`, `cm-lv`, `cm-th`, etc.), eliminating manual group mapping.
  - **Robust E2E Validation**: Extended the E2E test file to select ranges, click suggestions, check panel dismissals, and verify mapped values.

- **Interactive Regex Builder Stacked Gantt Layout (v6.9.77 — COMPLETED)**:
  - **Stacked Color-Coded Matches**: Redesigned the visual builder to parse all possible matching patterns across the log line simultaneously and map them to vertical rows (tracks). Represented options as color-coded horizontal bars aligned to the log line characters using monospace `ch` units.
  - **Dynamic State Overlapping**: Handled active highlights for selected options and automatically disabled overlapping tracks with a lower-opacity warning state to guide the user.
  - **Updated E2E Test Suite**: Updated `tests/test_16_interactive_regex_builder.py` to cover the badge layout clicking and toggle state selections.

- **Interactive Regex Builder (v6.9.76 — COMPLETED)**:
  - **Olaf Neumann Style Replication**: Built an interactive builder (`RG` module) where a sample log line is split into words, numbers, delimiters, and spaces. Clicking segments displays floating option dialogs showing matching regex patterns (e.g. Log Level, Date, Time, Number, IP Address, literals).
  - **Dynamic Composition Engine**: Real-time regex generation stitching selected tokens with capture groups and escaping unselected segments dynamically.
  - **E2E Validation Suite**: Created E2E test file `tests/test_16_interactive_regex_builder.py` to assert correct token highlighting, dropdown clicks, selection badges, and output regex matches.

- **Unparsed Regex Index-Based Handlers Fix (v6.9.75 — COMPLETED)**:
  - **Memory-Based Index Referencing**: Added `UNPARSED.currentClusters` and `UNPARSED.createRuleFromIndex()` to hold cluster references in memory and pass clean indices in the HTML `onclick` handlers, eliminating JavaScript evaluation corruption of regex backslashes.
  - **Ellipsis Truncation Guard**: Handled ellipsis `…` termination inside signature conversions, safely replacing them with `.*` to guarantee valid, compileable regular expressions.

- **Unparsed Analyzer Representative Pre-population Fix (v6.9.74 — COMPLETED)**:
  - **Sample Line Tracking**: Modified `UNPARSED.cluster()` to track and store a representative raw `sampleLine` for each structural cluster.
  - **Modal Pre-population**: Updated `UNPARSED.createRuleFromPattern()` to populate `#e-tl` with the representative log line and dispatch the input event, enabling automatic match highlighting in Step 1 of the Rule Creator modal instantly.
  - **E2E Test Assertion**: Added an assertion in `tests/test_14_unparsed_analyzer.py` verifying that `#e-tl` contains the correct sample log line when "+ Create Rule" is clicked.

- **Regex Editor Undo-Redo Option (v6.9.73 — COMPLETED)**:
  - **Undo/Redo History Stack**: Added a new global module `RX_HIST` to manage a history state stack specifically for the `#e-rx` regex pattern input field. Redefined its property descriptor to automatically capture programmatic assignments alongside standard user keyboard input.
  - **Interactive Controls & Shortcuts**: Added Undo (`↶ Undo`) and Redo (`↷ Redo`) action buttons with custom SVG icons in the Rule Creator modal. Enabled standard keybindings (`Ctrl+Z`, `Ctrl+Y`, `Cmd+Z`, `Cmd+Shift+Z`) scoped to the regex textarea.
  - **E2E Test Validation**: Added a new regression test `tests/test_15_regex_undo_redo.py` asserting history states, visual button visibility/disabled states, value restorations, and zero runtime script errors.

- **Unparsed Analyzer Create Rule Button Fix (v6.9.72 — COMPLETED)**:
  - **Fixed Undefined Handlers**: Replaced obsolete `CFG.openM` inline click handler with a new robust helper `UNPARSED.createRuleFromPattern(pattern)` to open the rule creator modal, check the customize regex pattern checkbox, call `UI.syncCustomRxUI()`, expand the advanced accordion, populate `e-rx` with the generated regex, and trigger a regex explanation.
  - **Auto-Suggest Wire Fix**: Replaced obsolete `UI.setMM` references inside the auto-suggest try and cluster-add click listeners with calls to the new helper `UNPARSED.createRuleFromPattern`.
  - **E2E Validation Suite**: Created a new Playwright E2E test file `tests/test_14_unparsed_analyzer.py` to verify the "Create Rule" flow from the Unparsed Analyzer. Updated the Coverage Map in `tests/README.md`.

- **Equal Height Settings Cards Layout Alignment (v6.9.71 — COMPLETED)**:
  - **Equal-Height Dashboard Grid**: Changed `align-items: start !important;` to `align-items: stretch !important;` in the `#res .dashboard-grid` selector class definitions. This forces all dashboard configuration settings cards (e.g. System & Aesthetics, Log Sources, Parse Rules, Sessions) within the same row of the responsive CSS grid to stretch to equal heights, eliminating jagged border lines and organizing the dashboard.

- **Rule Icon Dropdown & Semantic Auto-Suggestion (v6.9.70 — COMPLETED)**:
  - **Dropdown Selection**: Replaced the text input for `#e-ico` with a styled `<select>` element populated with standard log emojis and symbols (Bullet, Play/Start, Network/API, Database/SQL, Service/System, Warning/Alert, Error/Failure, Info, Latency, Auth, Queue, Ingress/Request, Egress/Response, Test/Debug).
  - **Dynamic Rule Name suggestions**: Added an `input` event listener to `#e-name` that monitors the Rule Name in real-time. If the current icon is the default bullet `•`, it automatically suggests and selects a matching semantic icon based on keyword matching (e.g., `query` -> `🗄`, `api` -> `🌐`, `error` -> `✕`, `warn` -> `⚠`, `auth` -> `🔒`, `latency` -> `🕒`, `queue` -> `📨`).
  - **Custom Value Safety**: Enhanced `UI.openM()` to check if a rule's saved icon is in the list of select options. If not, it dynamically creates a `(Custom)` option to preserve the icon selection gracefully without losing data.
  - **E2E Assertions**: Created `test_rule_creator_icon_dropdown_and_auto_suggestion` in `tests/test_13_rule_creator.py` validating select element visibility, default states, and real-time semantic name suggests.

- **Elements Rule Creator Modal Simplification (v6.9.69 — COMPLETED)**:
  - **Prioritized Auto-Detection Flow**: Moved the sample log line input (`#e-tl`) and live highlighted match preview (`#rx-pre`) to Step 1 at the top of the modal. Added a dynamic format status badge (`#preview-format-badge`) to visually display the current auto-detected preset layout (e.g., Spring Boot, Java Standard) or custom state.
  - **Manual Override Accordion**: Grouped manual format selectors (`#wf-sel`) and keyword marking parameters (`#kw-inp` chip builder, match modes, capture options) inside a collapsible accordion section (`#ovr-hdr` / `#ovr-body`) that starts collapsed by default.
  - **Appearance & SLA Settings Accordion**: Moved visual styles (Accent Color `#e-col` / `#e-hex`, Emoji Icon `#e-ico`) and SLA Threshold settings (`#e-sla`) into a collapsible accordion section (`#vis-hdr` / `#vis-body`) that starts collapsed by default.
  - **Removed Minimize/Maximize Buttons**: Cleaned up the modal header by removing the `#btn-rule-min` and `#btn-rule-max` buttons, UI toggle methods, and event bindings, streamlining rule creation viewports.
  - **Accordion Visual Indicators (Plus/Minus Toggles)**: Replaced the confusing right-pointing chevrons (`›`) on the main accordion headers (`#ovr-hdr`, `#adv-hdr`, `#vis-hdr`) with explicit `+` (collapsed) and `−` (expanded) text indicators rendered dynamically via CSS `::after` pseudo-elements. This cleanly distinguishes collapsible layout sections from dropdown select indicators (downward arrows).
  - **Dynamic Visual Group Mapping Guide**: Modified the static "Visual Group Mapping Guide" legend diagram to compute and render color-coded capture group pill segments in real-time as users modify mappings or map fields using visual tokens.
  - **Collapsible Capture Group Mapping Section**: Wrapped the Capture Group → Field Mapping input fields inside a collapsible accordion container (`#map-hdr` / `#map-body`) with a monospace `+`/`−` toggle indicator, making it collapsible/minimizable. Fixed chevron rotation for the Pattern Token Builder header (`#rxb-hdr`) by applying the correct `.rxb-hdr` style class in the HTML.
  - **Pattern Token Builder Click Fix**: Fixed a bug where the Pattern Token Builder accordion header (`#rxb-hdr`) could not be clicked. Cleaned up the initialization flow by merging the Token Builder structure directly into the original `RXB.init` (avoiding duplicate binding/listener execution). Restricted `pointer-events: none` to the token grid container (`#rxb-bd`) rather than the entire token builder wrapper to ensure the header remains interactive at all times.
  - **Regression Test Updates**: Updated E2E validation test suites (`tests/test_13_rule_creator.py`) to align with restructured steps, verify accordion expand/collapse toggles (including mapping header `#map-hdr`), and ensure all 81 regression assertions pass successfully.

- **Rule Creator UI fixes and Javascript Initialization Robustness (v6.9.68 — COMPLETED)**:
  - **Javascript Startup Robustness**: Resolved a javascript `TypeError` at startup when trying to bind `WIZ.test` (which was undefined), ensuring sequential javascript initialization blocks (such as `RXB.init()`, regex explainer color-coding, and custom overlays) execute successfully without crashing.
  - **Visual Group Mapping Restoration**: Fixed visual group mapping context menu activation inside `RXB.init` by calling `originalRxbInit` to register core change and input listeners correctly, resolving a regression where mapping fields did not auto-refresh preview layout.
  - **Add Rule Bootstrapping & Tests**: Aligned the Add Rule modal triggers and XML import tests (`test_12_log4j_import.py` and `test_13_rule_creator.py`) to properly verify modal maximize/minimize toggles and blank page bootstrapping workflows.

- **Unified Elements Rule Creator & Detailed Helper Tooltips (v6.9.67 — COMPLETED)**:
  - **Single-View Merger**: Eliminated the Guided and Advanced tabs (`#mb-g`, `#mb-a`, `.m-tog`) in the Elements Rule Creator modal (`#mm`). Replaced them with a unified view containing preset selection, keyword chips tagging, match options, and a single live match preview input (`#e-tl` / `#rx-pre`) with click-to-map group features.
  - **Customize Regex Pattern Accordion**: Grouped all custom regex fields, pattern template selector, token builder, and capture mappings under an expandable/collapsible advanced section accordion (`#adv-hdr` and `#adv-body`) with rotating chevrons.
  - **Regex-Free Checkbox Guard**: Added a "Customize Regex Pattern (Advanced)" checkbox (`#e-use-custom-rx`). When unchecked, advanced fields are read-only and display the auto-generated regex and capture mappings live as keywords are typed/deleted. Checking it enables editing to let advanced users tweak the auto-generated baseline.
  - **Contextual Help Popovers**: Extended the `HTIP` module's `TIPS` dictionary with detailed help descriptions for `format` (presets details), `keywords` (OR/AND match modes, next word/rest of line capture), and `custom_regex` (advanced editing instructions). Added interactive `?` help buttons to log format selector, keywords, and custom regex checkboxes.
  - **Regression Test Coverage**: Created `tests/test_13_rule_creator.py` containing Playwright assertions for tab-less modal checks, tooltip popovers rendering, custom regex enabling, and match previews highlighting. Updated coverage map in `tests/README.md`. All 78 tests pass successfully.

- **Log4j Config XML Import Alignment & Fix (v6.9.66 — COMPLETED)**:
  - **Inline Result Container**: Relocated the `#lj-res` element (which displays the appender count and the "Preview & Import" action button) from below Section 05 at the bottom of the Settings view, to sit inline directly inside Section 03 (Rule Generators) dashboard card under the "Import XML Config File" button (`#btn-lj-imp`). This places preview actions in the correct context for a seamless workflow.
  - **Empty Configuration Initialization Guard**: Fixed a bug where clicking "Import Selected" on the preview modal did nothing when the app was in an empty/fresh state (`S.cfg === null`). Updated `UI.impSheet()` to check for a null configuration and automatically load default rules from `DEF_CFG` (mimicking "New Config" button behavior) before adding the imported appender rules and enabling configuration operations.
  - **E2E Validation Suite**: Created a new Playwright E2E test file `tests/test_12_log4j_import.py` to verify the inline result container placement, correct class toggle transitions of `#sh-ov` modal, empty config fallback initialization, and overall rule count validation. Updated the Coverage Map in `tests/README.md`. All 74 tests pass.

- **CSS background-clip Compatibility Fixes (v6.9.65 — COMPLETED)**:
  - Fixed stylesheet warnings by explicitly adding the standard `background-clip: text` CSS property alongside the existing vendor-prefixed `-webkit-background-clip: text` rules for both the primary header logo mark (`.logo .acc`) and the onboarding welcome panel branding wordmark (`.ob-wordmark .acc`).

- **AI Insights, Focus Mode, First-Run UX & A11y Polish (v6.9.64 — COMPLETED)**:
  - **Phase 8 — AI Insights Engine** (`§JS-42`): Zero-dependency heuristic analysis of `S.trees`. Produces 2–5 insight cards per session covering: slowest thread (avg + max duration), error hotspot (top rule by error count), SLA breach list (worst offender highlighted), statistical duration outliers (2.5σ above mean), and multi-thread parallelism summary. Cards rendered as `role="region"` in Stats view with amber/red/green/blue severity badges.
  - **Phase 9 — Focus Mode** (`§JS-43`): `FOCUS_MODE` module toggled via the `F` key. Adds `body.focus-mode` CSS class to hide header, sidebar, action bar, and timeline mini-map — maximising the timeline viewport. Amber pill toast confirms state change. State persisted in `sessionStorage`. CSS `§31` controls all hide rules.
  - **Phase 10 — First-Run Experience** (`§JS-44`): Patches `UI.svm()` to detect the empty `#emp` card and inject a 3-step getting-started guide (Configure Rules → Load Log → Explore & Analyse) plus a keyboard shortcut strip (`Alt+1`, `Ctrl+K`, `F`, `/`). Drag-over highlight added to drop zone.
  - **Phase 11 — Accessibility Polish** (`§JS-45`): Skip-to-content link injected as first body element; focus traps applied to 5 modal dialogs (`#mm`, `#ann-modal`, `#cmd-palette`, `#ob-ov`, `#od-overlay`); `aria-live="polite"` on `#toast`; `role=status` on focus-mode toast; `role=switch` + `aria-checked` on all TIMELINE_NAV overlay chips (set at mount time).
  - **CSS** `§30 · AI INSIGHTS CARD`, `§31 · FOCUS MODE`, `§32 · ACCESSIBILITY POLISH` added.
  - **Phase 12 — Verification**: All 23 Playwright assertions in `test_phases_8_11.py` pass; JS syntax check clean.

- **Timeline Navigator mini-map panel (v6.9.63 — COMPLETED)**:
  - Added new `TIMELINE_NAV` IIFE module (`§JS-41`) providing a mini-map panel mounted at the bottom of Gantt waterfall and Swimlane views.
  - The mini-map renders per-bucket density histograms using Canvas 2D for four overlay layers: **Activity** (blue), **Errors** (red), **SLA breaches** (amber), and **Duration intensity** (green). Each layer is toggled independently via colour-coded pill chips.
  - An amber **viewport indicator** rectangle shows the current horizontal scroll position relative to the full timeline. The indicator is draggable left/right to pan the main scroll container, and clicking anywhere on the canvas jumps to that point in the timeline.
  - A **zoom presets strip** provides one-click buttons for 0.5×, 1×, 2×, 4×, 8× and Fit, wired to `GANTT_ZOOM_PAN.applyZoom()` / `fitWindow()`.
  - A **position label** in the zoom strip shows the current scroll percentage.
  - All internals resize correctly on window/panel resize via `ResizeObserver` and scale to device pixel ratio.
  - Wired `TIMELINE_NAV.mount()` into both `GR.render` override and `SWIMLANE.init` so the panel appears automatically in standard Gantt and multi-thread Swimlane view modes.
  - Added CSS `§29 · TIMELINE NAVIGATOR` with variables-driven theming compatible with all 6 existing colour themes.
  - Wrote Playwright E2E verification suite `test_timeline_nav.py` — all 15 assertions pass successfully.

- **Trace Explorer view panel integration (v6.9.62 — COMPLETED)**:
  - Built the `TRACE_EXPLORER` namespace to scan parsed trees for correlation IDs, aggregate trace statistics (total unique traces, tracked events, SLA breaches, thread span list), and render the new full-screen Traces tab interface.
  - Linked trace row selection click events to filter all telemetry views to that specific trace ID, automatically opening and selecting the trace's slowest event in the right-side Event Inspector panel.
  - Added full search and filtering input bar to search for specific trace IDs or spanning threads.
  - Added Alt+7 hotkey support to switch view modes to Traces explorer.
  - Wrote Playwright E2E verification suite `test_trace_explorer.py` and confirmed all assertions pass successfully.

- **Command Palette & Event Inspector Drawer Feature Overhaul (v6.9.61 — COMPLETED)**:
  - Injected persistent right-side Event Inspector Drawer (`#event-inspector`) side-by-side with `<main class="main">` in the workspace flex grid.
  - Implemented the `INSPECTOR` namespace to populate details, copy raw payload, and edit comments on selection.
  - Wired tree rows, Gantt rows, Swimlane bars, and Stats cards clicks to open the inspector with selected event telemetry details.
  - Refactored `CMD` Command Palette to support fuzzy matched command searches, Recent Actions history powered by localStorage, and dynamic Trace ID filters.
  - Resolved event conflict where the Overdrive modal dialog intercepted pointer events, by bypassing the full-screen modal on simple click.
  - Wrote Playwright E2E verification suites `test_command_palette.py` and `test_event_inspector.py` and confirmed both suites pass successfully.

- **App Preferences Visibility Conflict Fix (v6.9.60 — COMPLETED)**:
  - Fixed a CSS class collision where nested "Performance" and "Appearance" preference sub-sections (`#ss-perf-body` and `#ss-appear-body`) used the `.settings-section-body` class name.
  - This class name matched the main settings section transition rules setting `max-height: 0` and `opacity: 0` by default. Because the nested sections are not direct children of `.settings-section-wrap`, they never matched the main open override selector, leaving them collapsed/empty even when toggled open.
  - Resolved this by renaming the nested sections' body class name to `.settings-sub-body` in both stylesheet rules and Javascript template builders.

- **Dedicated Web Worker Plugins Sandbox, Scoped MutationObserver, and Offline Fonts (v6.9.59 — COMPLETED)**:
  - Replaced the high-risk `iframe` sandbox execution system with a custom Blob URL-based dedicated Web Worker runner.
  - Implemented a message validation gate (`MSG_VALIDATOR`) checking types and structure of all postMessage communication.
  - Enforced a `3000ms` execution watchdog. If a plugin runs longer than 3 seconds, the worker is terminated and marked as timed out.
  - Implemented automatic recovery (workers respawn on next hook run) and a failure limit (plugins are disabled after 3 consecutive failures).
  - Added a new **Plugin Health Panel** showing live status badges (Active/Timeout/Error/Disabled), last run timestamps, execution times, and failure counters.
  - Cleaned up obsolete window-level event listeners and removed the `#plugin-sandbox` iframe.
  - Re-scoped `GANTT_RESIZE` MutationObserver to target only the `#res` container. Switched connection state dynamically: calls `connectObserver()` when switching to `gantt` or `split` view, and `disconnectObserver()` on all other views.
  - Implemented `UI.cleanupCurrentView()` called during view transitions to release resources.
  - Removed all Google Fonts preconnect and stylesheet link tags from the HTML header.
  - Switched default CSS variables (`--ui`, `--display`, `--mono`) and all 6 themes to use fast, native system font stacks.

- **ChatGPT Review Code Quality & Security Fixes (v6.9.58 — COMPLETED)**:
  - Standardized annotation comments lookup using a helper `getAnnotationText()` in `UTILS` object. Fixed tree details renderers, Gantt timeline labels, note MD exporters, and JIRA description formats to display comments correctly without crashes or rendering `[object Object]`.
  - Added robust initialization guards (e.g. `QUICK_EDIT._clickWired`) to prevent memory leaks from duplicate document event listeners on repeat renders.
  - Implemented keyboard accessibility & ARIA states for the Theme Picker Swatch Swapper (added `aria-selected` tracking, ArrowUp/ArrowDown selection navigation, Escape-key close triggers, and auto-focus coordinates target).
  - Hardened default rules configurations by deeply freezing `DEF_CFG` elements.

- **Enhanced Stack Behaviors: swap & popAll (v6.9.57 — COMPLETED)**:
  - Added support for two new stack behavior options: `swap` (closes current top stack node and opens a new one at the same level) and `popAll` (closes all open nodes on the stack and starts fresh at root).
  - Integrated the behaviors into all three parsing modules: Worker-based batch parser (`pl`), local stream parser (`STREAM_PARSER`), and WebSocket stream parser (`WS_STREAM_PARSER`).
  - Added dropdown selection elements to Rule Editor modal, and mapped badge styling (`b-amber` for swap, `b-red` for popAll) and visual labels (`⇆ swap`, `⤊ popAll`) inside Settings screen lists and Regex Test Wizard match indicators.
  - Documented new stack behaviors in the Help tooltip library (`HTIP.behavior`).
  - Added automated validation test suite `test_stack_behaviors.py` confirming parser stack node tree outputs.

- **Settings & Help Panel DOM Preservation Fix (v6.9.56 — COMPLETED)**:
  - Fixed a critical garbage-collection bug where `UI._showPanel()` used `removeChild()` to detach inactive utility panels from the DOM, causing them to be discarded by the browser. Solved this by parking inactive panels in `#hidden-panels-container` instead of detaching them.
  - Also resolved a bug in `UI.render()` where `#res.innerHTML = statsH` wiped out `p-cfg` or `p-hlp` if they were active during parsing. Added a panel preservation block at the start of `render()`.
  - Added a comprehensive Playwright automation test suite `test_settings.py` verifying full navigation transition flows.

- **Settings Panel DOM Reference Fix (v6.9.55 — COMPLETED)**:
  - Fixed an issue where the Settings or Help panel would fail to display because they were detached using `removeChild()` before `document.getElementById` was called to look them up.
  - Implemented pre-detached reference preservation inside `UI._showPanel()`.

- **Settings & Help Panel Staging Refactor (v6.9.54 — COMPLETED)**:
  - Completely removed the legacy `.sb-body` (sidebar) re-parking logic from `UI.rv()`. Since the sidebar is hidden, parking panels there caused rendering errors.
  - Rewrote `UI._showPanel()` to cleanly use `removeChild()` to detach panels from any parent, and set inline `display: flex` style override to guarantee visibility.

- **Settings/Help View Short-Circuiting (v6.9.53 — COMPLETED)**:
  - Bypassed the analytical view data-renderer `UI.rv()` in `UI.svm()` when navigating to utility views (`cfg`/`hlp`) by short-circuiting to the new `_showPanel` helper.

- **Active State Restoration Fix (v6.9.52 — COMPLETED)**:
  - Ensured `.active` class is reapplied to `p-cfg` and `p-hlp` when rendering them inside `#res`.

- **Null-Guard Fix for btn-parse/btn-abort (v6.9.51 — COMPLETED)**:
  - Fixed `Uncaught (in promise) TypeError: Cannot set properties of null (setting 'disabled')` thrown from `UI.ub()` during `ONBOARD.loadDemo()`.
  - Root cause: `btn-parse` can be temporarily absent from the DOM during async demo loading when the onboarding overlay is still visible and the parse dock hasn't mounted yet.
  - Applied defensive `if (btn)` guards across all six call sites: `UI.ub`, command palette parse/abort actions, incremental-parse catch/callback, `finally` block of main parse handler, and abort click listener.
  - Also guarded `btn-exp-menu` and `btn-abort` references in the same block.

- **Log Level Parsing & UI Visualization (v6.9.50 — COMPLETED)**:
  - Enabled logging level capturing across all three parsing entry points (Web Worker batch parser, client-side stream parser, and secondary live stream parser), populating a new `level` attribute on parsed telemetry nodes.
  - Implemented dynamic, color-coded level badges inside Tree View, Flat Row Timeline List View, and Diff Tree renderers using CSS swatches (`.b-red` for errors/fatal, `.b-amber` for warnings, `.b-blue` for info, and `.b-gray`/`.b-pur` for debug/trace).
  - Integrated the `level` attribute into the LQL (LogLens Query Language) runtime records mapping, allowing query statements like `WHERE level = "ERROR"`.
  - Documented `level` fields under the LQL Help reference table.
  - Updated both `DEF_CFG` and onboarding `DEMO_CFG` element rules regex patterns and capture mappings to extract log level fields, ensuring out-of-the-box level visualization support on built-in demo loads.

- **Defensive Button & Panel Checks (v6.9.49 — COMPLETED)**:
  - Added strict existence validation checks (`if (el) ...`) to all DOM appends of `p-cfg` and `p-hlp` inside both `UI.rv` and `UI.svm` navigation controllers.
  - Implemented safe element checks for `btn-parse` and `btn-abort` inside the `ONBOARD.loadDemo()` asynchronous workflow, preventing any uncaught promise rejections if the buttons are temporarily detached or unmounted during active rendering.

- **Panel Preservation & TypeError Fix (v6.9.48 — COMPLETED)**:
  - Resolved `Uncaught TypeError` when switching view modes where `p-cfg` or `p-hlp` would be destroyed by `.innerHTML = ''` or `.remove()`.
  - Added parent element preservation guards to both `UI.svm` and `UI.rv` which move `p-cfg` and `p-hlp` back to `.sb-body` (the sidebar container) before clearing `#res`.

- **Wider Rule Editor Modal Layout (v6.9.47 — COMPLETED)**:
  - Increased the default `.modal` width from `660px` to `920px` to leverage available workspace area on desktop displays.
  - Updated the token palette grid (`.tok-grid`) inside the Regex Builder accordion to use auto-fill (`repeat(auto-fill, minmax(130px, 1fr))`) instead of fixed 2 columns, letting the pattern token cards scale fluidly across the expanded modal layout.

- **Visual Group Mapping & Token Builder Search (v6.9.46 — COMPLETED)**:
  - Implemented a Visual Group Builder experience: highlighted regex capture groups in the live match preview can now be clicked directly to open an interactive mapping dropdown menu, setting the corresponding metadata field inputs dynamically.
  - Added a search input box at the top of the Pattern Token Builder accordion, filtering regex tokens and dynamically auto-expanding matching categories to improve builder navigation.
  - Expanded the token presets palette (`TOKS`) with trace/span IDs, generic JSON field capturing, and literal brace anchors.

- **CSV / Pipe-Delimited Template Alignment (v6.9.45 — COMPLETED)**:
  - Fixed an inconsistency where the "CSV / Pipe-delimited" preset was available in the Guided Rule Wizard but missing as a preset in the Advanced Mode template selection dropdown.
  - Added the CSV option to the `#tmpl-sel` HTML select dropdown and mapped its base regular expression template to the `TMPLS` pattern dictionary in JavaScript.

- **View Switcher Enabled Globally (v6.9.44 — COMPLETED)**:
  - Set the view tabs bar (`#vtabs`) display style to `flex` by default in CSS, rendering it visible at all times.
  - Rewrote the `UI.svm` navigation controller to support switching tabs cleanly when no logs are loaded yet: appends Settings (`cfg`) and Help (`hlp`) panels dynamically, and keeps the empty state card (`#emp`) correctly rendered across all analytical view modes.

- **Auto-Parse Empty Rule Check & Redirection (v6.9.43 — COMPLETED)**:
  - Added a validation guard to both the file-select helper (`UI.chooseAndParseLog()`) and the drag-and-drop listener to check for active rules (`S.cfg.elementRules.length`).
  - If no rules exist, a warning toast is shown and the user is automatically redirected to the Config screen to add or import rules first, preventing empty/useless parsing.

- **Auto-Parsing Workflow for Empty State and Drag-and-Drop (v6.9.42 — COMPLETED)**:
  - Added a `UI.chooseAndParseLog()` helper function that auto-triggers parsing once the user selects a log file via the empty state action button.
  - Enhanced the drag-and-drop listener to immediately parse log files upon being dropped onto the workspace if a config is already present, eliminating extra clicks in the new sidebarless UI.

- **Onboarding Hero Section Default Visibility Reversion (v6.9.41 — COMPLETED)**:
  - Reverted the default-hidden change on the onboarding welcome overlay (`#ob-ov`), ensuring the hero section starts visible by default on page load to guide new sessions.
  - Confirmed that this initial welcome screen serves as the core entry page when no log data exists.

- **Empty State Action Buttons Integration (v6.9.40 — COMPLETED)**:
  - Integrated primary action buttons directly inside the empty state card (`.emp-card`) for "Select Log File" and "Load Demo Log", resolving layout flow ambiguity when landing on the "Ready for telemetry" screen.
  - Replaced inline styles inside the empty state markup with clean, dedicated CSS classes (`.emp-title`, `.emp-desc`, `.emp-actions`).

- **Onboarding Skip Flow Persistence Fix (v6.9.39 — REVERTED)**:
  - Temporarily set onboarding overlay `#ob-ov` to start as hidden; reverted in v6.9.41 to keep the welcome screen as the default landing experience.

- **Frontend Design Audit & CSS Variable Fixes (v6.9.38 — COMPLETED)**:
  - Audited the entire stylesheet and resolved all undefined CSS variables (`--amber-dim`, `--sans`, `--text-sm`, `--text-xs`), preventing silent rendering failures in modern browsers.
  - Aligned `.ss-ord` badges background to use `--amber-g` and changed `.rules-hdr-btn` font-family to `--ui`.
  - Replaced the undefined `--sans` and inline template variable font sizes inside the Regex Builder Accordion with standard fixed font sizes (`11px` and `9.5px`).
  - Enforced the **Flat-First Rule** by removing drop-shadows on `.dashboard-card` elements at rest (`box-shadow: none`) and cleanly adding them on hover states only.

- **Global Summary Cards UI Styling (v6.9.37 — COMPLETED)**:
  - Implemented responsive, glassmorphic CSS styling for the global `#res-summary-cards` container and `.summary-card` children elements.
  - Added smooth grid-based layouts, micro-interaction scale transforms, rotating hover icons, and theme-synced progress bars to match the premium console aesthetic.
  - Resolved the unstyled vertical stacked layout bugs affecting the "Slowest Operation", "Rules Coverage", and "Active Threads" summary telemetry elements on analytical views.

- **Stats View UI Layout Fixes (v6.9.36 — COMPLETED)**:
  - Refactored the Stats panel structure by introducing a flex column `.stats-layout-wrapper` container with standard `16px` gaps.
  - Eliminated the double-border card nesting bug by wrapping only the Latency Statistics table inside `.tw`, making the main Latency panel, Pattern Anomalies, Thread Correlation, and Heatmap Calendar sibling cards.
  - Updated custom plugin SDK method `addStatsCard` to target the new `.stats-layout-wrapper` (with fallback to `.tw`), preventing plugin cards from being incorrectly nested inside the table borders.
  - Replaced the hardcoded hex color inside the Canvas Spark Histograms (`drawSpark`) with a dynamic `--amber` CSS theme-variable lookup for precise, responsive dark/light mode synchronization.

- **Tauri Desktop Application Setup (v6.9.35 — COMPLETED)**:
  - Initialized a Tauri v2 native desktop application wrapper inside the workspace root (`src-tauri` container).
  - Configured `tauri.conf.json` with the app bundle identifier `com.loglens.desktop` and custom high-density desktop dimensions (`1280` x `800`).
  - Added a root `package.json` to organize Tauri CLI dependency triggers (`npm run dev` / `npm run build`).
  - Implemented a cross-platform asset packaging node build script that copies the self-contained `loglens.html` into `dist/index.html` at run/build time.
  - Setup root level `.gitignore` rules to exclude package lock files, build artifacts (`dist/`), and dependencies (`node_modules/`).

- **Settings UI/UX Refinement & Data Portability (v6.9.34 — COMPLETED)**:
  - Redesigned all 4 settings sections into collapsible `.settings-section-wrap` containers with smooth `max-height` CSS transitions, rotating `›` chevron indicators, and monospace amber ordinal badges (`01`–`05`) for industrial wayfinding.
  - Scoped the inner App Preferences sub-section CSS selectors under `.settings-section >` parent to prevent style collision with the new top-level collapsible headers.
  - Added **Section 05: Data Portability** with three new cards:
    - **Export All Settings**: serializes `S.cfg`, `S.appPrefs`, theme, datasource fields, JIRA, Git, and WebSocket config into a single `.loglens-settings.json` file.
    - **Import Settings**: reads and validates a `.loglens-settings.json` file, hydrates all form fields, applies theme and preferences.
    - **Export Element Rules**: exports just `S.cfg.elementRules` as a standalone JSON file.
  - Created the `SETTINGS_IO` JavaScript module (`§JS-SETTINGS_IO`) with `exportAll()`, `importAll(file)`, and `exportRules()` methods.
  - Wired section collapse/expand via event delegation on `[data-collapse]` attribute click and keyboard events.
  - Updated responsive CSS overrides for the new collapsible section structure.
  - **Dropdown Stacking Fix**: Resolved rule action menus (`.rc-more-dropdown`) being clipped/occluded under subsequent element cards by using the CSS `:has()` selector to dynamically raise the active card's `z-index` to `50` when the dropdown is open, and `z-index: 2` on card hover.
  - **Enhanced Global Summary Cards**: Moved the three telemetry summary cards ("Slowest Operation", "Rules Coverage", "Active Threads") from being locally nested inside the Stats view into a global `#res-summary-cards` container right below the `#stats-bar`. Designed with a premium glassmorphic theme, micro-animation scale hover effect, rotating SVG icons, progress bars, and conditional display across all analytical result views (`split`, `gantt`, `tree`, `stats`) while hiding them on utility views like `cfg` and `hlp`.

- **Log4j Panel Merger into Settings (v6.9.33 — COMPLETED)**:
  - Merged the Log4j XML Importer and Real-Time Log Stream views into the unified Settings (`cfg`) panel.
  - Placed the Log4j import card and WebSocket stream card directly inside the dashboard-grid container of the Settings screen.
  - Relocated the pattern import result output container (`#lj-res`) below the grid but above the Element Rules section.
  - Removed the Log4j view (`lj`) tab switcher from both the header and hidden sidebar panel tabs.
  - Redirected the `Alt+9` keyboard shortcut to switch to the unified Settings view, and removed the Log4j option from the command palette.
  - Cleaned up obsolete CSS rules and references for the Log4j (`lj`) view mode.

- **Config & Setup Panel Merger (v6.9.32 — COMPLETED)**:
  - Merged Setup (`gs`) and Config (`cfg`) view modes into a single, unified "Settings" (`cfg`) view.
  - Relocated all setup cards (Global Settings, Cloud Datasources, JIRA Settings, Directory Watcher, Git Sync, Custom Plugins) directly into the Config dashboard card grid layout.
  - Restructured the DOM: closed the `.dashboard-grid` container to cleanly place the Element Rules section full-width below the settings cards.
  - Re-anchored settings dirty state tracking to listen to the new merged Settings tab (`cfg`) click events.
  - Removed all occurrences, routing switch statements, command palette registry items, and sidebar references to the old setup view (`gs`).
  - Redirected the `Alt+8` keyboard shortcut to launch the merged Settings (`cfg`) view mode.

- **UI/UX Pro Max Overhaul (v6.9.31 — COMPLETED)**:
  - Redesigned full-screen Config, Setup, and Log4j screens into modern dashboard layout card grids (`.dashboard-grid` and `.dashboard-card`) with glass hover animations, subtle shadows, and structured headers.
  - Refactored header view switcher tabs (`.hdr .vtabs`) to use flexible center alignment with automatic horizontal scrolling (`overflow-x: auto`) and hidden scrollbars, preventing visual collisions with logos and actions on narrow viewports.
  - Dynamically hide the workspace filter action bar (`#action-bar`) when switching to non-analytical screens (Config, Setup, Log4j, Help) to reclaim valuable vertical space for form views.
  - Optimized dashboard layout card accessibility, making forms and toggles visible by default in full screen while retaining manual toggle collapse controls.

- **Sidebar Options to Full-Fledged Screens (v6.9.30 — COMPLETED)**:
  - Relocated Config, Setup (Settings), Log4j, and Help sections from the narrow sidebar into full-screen main view modes.
  - Added "Config", "Setup", "Log4j", and "Help" view tabs to the header view switcher (`#vtabs`) with modern SVG icons.
  - Implemented dynamic panel recycling in `UI.rv()` to append/move panels between `#res` and a hidden container (`#hidden-panels-container`) when view modes change, preserving active states and DOM listeners.
  - Hidden the sidebar (`.sb`) and resizing handle (`.sb-resize-handle`) entirely, allowing all visualization views and setup screens to utilize 100% of the viewport width.
  - Updated default boot view mode to `'cfg'` for a clean setup start page.
  - Added keyboard shortcuts (`Alt+7` to `Alt+0`) and command palette view items.
  - Re-routed header click event listeners and overflow menu items to navigate to the new views via `UI.svm()`.

- **Keyboard Accessibility & Tooltip Viewport Guard (v6.9.29 — COMPLETED)**:
  - Added `tabindex="0"` focus markers to all collapsible sidebar headers (`#hdr-rules`, `#hdr-watch`, `#hdr-git`, `#hdr-plugins`, `#hdr-stream`, `#hdr-packs`).
  - Added a global `keydown` event listener to toggle collapsible section visibility when pressing `Enter` or `Space` while focused.
  - Extended the custom tooltip (`TIP` module) to listen for the document `mouseleave` event, ensuring the tooltip is immediately hidden if the cursor exits the browser viewport.

- **Element Rules Interactivity & 3-Dot Actions (v6.9.28 — COMPLETED)**:
  - Enabled section collapse/minimize functionality for the "Element Rules" sidebar header, ensuring click events trigger toggle states for `#rules-list` only when clicking outside the action buttons.
  - Implemented event delegation in JavaScript to capture clicks on each rule's 3-dot actions button (`.rc-more-btn`), dynamically showing/hiding options (Edit, Export, Delete) and auto-closing them when clicking outside.
  - Designed custom, premium CSS styling (`.rc-more-dropdown` and `.rc-dropdown-item`) supporting glass hover effects, card elevation, and responsive dark-mode variables.

- **Premium Tooltip System Integration (v6.9.27 — COMPLETED)**:
  - Designed and built a custom floating tooltip container (`#app-tooltip`) with theme-aware borders, elegant paddings, squircle corners, and smooth CSS transitions.
  - Refactored the core Javascript `TIP` controller to bind to the new HTML element, automatically capturing client coordinates and fading tooltips in and out on hover/focus actions.
  - Added descriptive `title` attributes (which dynamically map to tooltips) across view switchers, configuration database controls, file parse options, and rule manipulation elements.

- **Brand Logo & Wordmark Redesign (v6.9.26 — COMPLETED)**:
  - Designed a premium vector SVG logo emblem consisting of interlocking Squircle boundary, parallel data lines, and transparent magnifying focus lens elements with amber-to-orange gradients.
  - Upgraded font styling of "LogLens" branding across both header and onboarding overlay to use heavier font weights (`800`/`900`), modern display typefaces, and high-fidelity text-mask gradients.
  - Promoted overall layout prominence (increased logo icon bounds to 32px in header and 44px in onboarding).

- **Primary Action Bar Implementation (v6.9.25 — COMPLETED)**:
  - Introduced a primary action bar (`#action-bar`) nested inside the main content viewport so that it starts beyond (to the right of) the left sidebar, allowing the sidebar to extend directly to the top header.
  - Relocated the active thread selector (`#vt-chips`) to the left side of the action bar.
  - Relocated the global search filter (`#hdr-search-container`) to the right side of the action bar.
  - Hooked global search container visibility to display only when applicable for the selected view mode (e.g. hidden on Stats and 3D View).

- **View Switcher Relocation to Header (v6.9.24 — COMPLETED)**:
  - Moved the view switcher tabs (`#vtabs`) from the main content viewport directly into the center area of the header and centered it horizontally using absolute positioning.
  - Removed all inline styling from `#vtabs` HTML tag and structured styling rules purely inside the CSS stylesheet with responsive header overrides.
  - Handled the active indicator highlights using absolute bottom border lines that scale perfectly on theme transitions.

- **Footer Relocation of Status Indicators (v6.9.23 — COMPLETED)**:
  - Created a thin (26px) status footer at the very bottom of the application viewport.
  - Moved all system status metrics and indicators (`#sys-status`, `#hdr-fs`, `#hdr-cfg`, `#hdr-file`) from the header action grid to the new bottom footer.
  - Styled footer items with clean, flat transparent styling that changes cleanly across all 6 themes to preserve visual consistency.

- **5-Theme System Expansion (v6.9.22 — COMPLETED)**:
  - Added 4 brand-new themes: **Aurora** (cyan/deep-navy), **Midnight** (OLED-black/electric-purple), **Forest** (emerald-green/earthy), **Crimson** (dark-noir/crimson-red).
  - Added **Ivory** as an explicit `[data-theme=ivory]` alias for the former "light" theme.
  - Replaced the single moon/sun toggle button with a **theme swatch picker** dropdown in the header (shows all 6 themes as gradient preview cards — click to apply instantly).
  - Expanded the `Theme` JS object: `THEMES` metadata array, `apply()`, `renderPicker()`, `openPicker()`, `closePicker()` methods.
  - `Alt+T` keyboard shortcut now cycles through all 6 themes instead of toggling between 2.
  - Fixed all `isDark` checks to use `dataset.theme !== 'ivory'` so all 4 new dark-background themes work correctly with Graphify/canvas rendering.
  - Added per-theme header glassmorphism treatments (each theme has its own header tint and glow color).
  - Updated the report renderer theme select to offer all 6 themes.
  - **Different Fonts & UI Shapes per Theme**: Assigned custom typography (e.g., Playfair Display, Syne, Orbitron, Outfit, DM Serif Display) and distinct border-radius variables (`--rounded-*`) to each theme to completely alter the visual character (ranging from sharp retro-newsprint boxes to organic fluid pills).
  - **Architecture note**: All themes are pure CSS variable blocks (`[data-theme=X]`) — zero JS overhead, theme identity via `data-theme` HTML attribute.

- **System Emoji Elimination & Unicode Icon Upgrades (v6.9.21 — COMPLETED)**:
  - Swept the entire application codebase and programmatically replaced all remaining 65+ system-colored emojis with high-quality, flat monochrome Unicode glyphs.
  - Substituted rule icons (🌐, 🗄, 🪵, 🚨, 🍃, ☁️, ⚡) with professional developer glyphs (❖, ▤, ▪, ✕, ☘, ☁, 🗲).
  - Cleaned up category headers, option menus, stats tables, context menus, and empty state panels (replacing emojis like 🔍, 📈, 📉, 📊, 🏊‍♂️, 🕸, 📋, 📝, 📌, 🌲, 🧬, 🔌 with professional developer symbols).
  - Ensured all icons adapt dynamically to the active light/dark theme colors rather than rendering as colored system graphics.

- **Control Bar Elimination & Redirection (v6.9.20 — COMPLETED)**:
  - Eliminated the horizontal control bar (`.ctrl`) and its toggle button entirely, reclaiming ~45px of vertical screen space for the visualization canvas.
  - Redistributed its core components into a clean, sticky `#cfg-action-dock` at the top of the CFG sidebar panel:
    - Pinned the **Log File** select split-button, current filename display (`#lfname`), and multi-file session chips (`#file-chips`).
    - Pinned the **▶ Parse** and **■ Abort** primary actions directly below the file selector.
    - Integrated real-time stream controls (`#cg-stream-ctrl`) inline within the second row of the dock.
  - Moved the progress bar (`#prog`) into a dedicated slim strip above the view tabs layout inside the main panel, ensuring visual feedback is preserved during large parse cycles.

- **Help Panel Always-Visible Bug Fix (v6.9.19 — COMPLETED)**:
  - Root cause: `#p-hlp { display: flex !important }` CSS rule used an ID selector which has higher specificity than the `.sp { display: none }` class rule, causing the Help panel to render as visible (`display: flex`) at all times — even when it was not the active sidebar tab.
  - Fix: Removed `display: flex !important` from the bare `#p-hlp` rule and added it exclusively to `#p-hlp.active`, so the Help panel only becomes visible when the HLP tab is actually selected.
  - Result: Scrolling within CFG, SET, or L4J sidebar panels no longer reveals the Help content underneath.

- **No-Scroll Hero Page Optimization (v6.9.18 — COMPLETED)**:
  - Replaced the large 3-column quickstart card block (`.ob-steps`) with an elegant, ultra-slim inline progress bar (`.ob-quick-bar`), reducing its vertical footprint by over 110px.
  - Condensed margins, padding, and text/icon sizes on features, CTA, and logo headers.
  - Verified zero vertical scrollbars are needed on standard laptop (1366x768) and desktop screens.
- **Hero Layout Overflow Alignment Fix (v6.9.17 — COMPLETED)**:
  - Fixed a classic CSS flexbox overflow bug on the onboarding welcome screen overlay (`#ob-ov`): removed the absolute vertical centering (`align-items: center`) which pushed the top-level logo elements off-screen on shorter viewports.
  - Implemented standard container margin-collapsing (`margin: auto` on `.ob-wrap`) to center the content normally when shorter, and align safely to the top when taller than the viewport.
- **Onboarding Layout Compactness (v6.9.16 — COMPLETED)**:
  - Redesigned the onboarding feature highlights grid from a 2-column format into a balanced 3-column layout (`repeat(3, 1fr)`).
  - This reduces the vertical height from 3 rows to 2 rows, helping the hero overlay fit comfortably within standard viewport heights.
  - Maintains responsive collapse to a single column on small screen widths.
- **Tagline Placement Update (v6.9.15 — COMPLETED)**:
  - Removed "Metadata-Driven Log Analyzer" tagline and its vertical line divider from the main dashboard header to declutter the user interface.
  - Repositioned the tagline onto the onboarding/hero page underneath the main LogLens wordmark for branding consistency.
  - Cleaned up unused onboarding badge (`.ob-badge`) CSS rule.
- **Premium Logo Design & Version Removal (v6.9.14 — COMPLETED)**:
  - Replaced the simple "LL" text box with a premium custom inline SVG logo icon depicting structured log lines scanned by a glowing diagnostic lens with amber/orange gradients.
  - Removed the frontend version display badge (`.v-badge` showing `v6.1`) next to the wordmark to clean up the header layout.
  - Cleaned up unused `.v-badge` CSS rules to maintain stylesheet integrity.
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

- [x] Tauri desktop app (Rust + WebView, <10 MB)
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

*Last Updated: 2026-10-10*  
*Updated By: Antigravity (Stats View Header Bar Fix v6.9.97)*
