# LogLens — Roadmap Implementation Plan

## Goal
Execute the full 5-phase LogLens roadmap — from Foundation Hardening (Phase 1, v2.x) through Platform & Ecosystem (Phase 5, v6.0) — across 24 months of planned features. The implementation stays true to the core philosophy: single-file HTML, zero dependencies, offline-first, privacy-by-default.

## Implementation Strategy

Each phase builds on the previous. Phase 1 must be completed before Phase 2. Within a phase, feature groups can be tackled in parallel (performance, file handling, export, config, UX are independent from each other). The single HTML file is **always** maintained as the primary artifact — even as the architecture evolves.

---

## Phase 1 — Foundation Hardening (v2.x)

**Status: In Progress** · Target: 500 MB logs in <10s; shareable reports without install

> [!IMPORTANT]
> This phase is the current priority. All features below must be completed before Phase 2 begins.

### ⚡ Performance Group

#### Virtual Scroll Tree
Replace the current `details/summary` HTML tree with a virtual-scroll list that only renders visible nodes. Required for 50k+ nodes without DOM thrashing.

**Approach:**
- Track a flat, pre-ordered list of all nodes with depth metadata
- Maintain a `visibleStart` / `visibleEnd` window based on container scroll position + estimated row height
- Render only visible rows as absolutely positioned elements
- Collapse/expand operations simply mutate the flat list (insert/remove children)

#### Streaming Chunk Auto-Tuning
Currently uses a fixed 512 KB chunk. Add auto-tuning:
- Start with 256 KB
- Measure chunk-processing time; if <100ms, double the chunk size (max 4 MB)
- Report chunk size as a debug stat

#### IndexedDB Result Cache
After a successful parse, store the result trees + config hash in IndexedDB:
- Key: `SHA256(filename + file size + lastModified + configHash)`
- On file select: check IndexedDB for a matching key; if found, offer "Reload from cache" button
- Cache has a max of 5 sessions (LRU eviction)

#### Gzip/Zstd Decompression
Use the native `DecompressionStream` API to decompress `.log.gz` files before passing to the worker:
- Detect file extension `.gz` or MIME type
- Pipe through `DecompressionStream('gzip')` before slicing into chunks
- Show a "Decompressing…" progress phase before parsing begins

---

### 📁 File Handling Group

#### Multi-File Session
Allow selecting multiple log files from N nodes and merging into a unified timeline:
- New "Add Files" button in control bar (+ icon next to existing Select)
- Each file parsed independently in a worker; results merged by timestamp-sorting root events
- File selector chips shown below control bar (each removable)
- Header shows total file count badge

#### Drag-and-Drop
Listen for `dragover` / `drop` events on the entire app surface:
- Accept `.log`, `.txt`, `.out`, `.gz` files
- Accept `.json` files (treat as config import)
- Visual drop-zone overlay with amber border glow while dragging
- Works on: main result area, Gantt rows, control bar

#### Directory Watcher (Auto-Reload)
For browsers with File System Access API:
- After connecting a log file via FS API, offer "Watch for changes" toggle
- Poll file `lastModified` every 2 seconds (using `fileHandle.getFile()`)
- On change: auto re-parse with the same config and thread filter
- Show "Live" badge in header when watching

---

### 📤 Export Surface Group

#### Self-Contained HTML Report
Generate a standalone HTML file containing:
- Embedded Gantt SVG rendering of all threads
- Execution tree as static HTML
- Stats bar data
- Metadata (filename, config name, parse timestamp, rules used)
- No JS required to view (pure HTML/CSS)

**Implementation:**
- `function exportHtmlReport()` — serializes current parse results to self-contained HTML
- Uses `<details>/<summary>` for the tree (no JS needed)
- Gantt rendered as SVG via `serializer.serializeToString()` or reconstructed as `<rect>` elements

#### CSV Export
Export all parsed events as CSV:
- Columns: `thread, ruleName, elementName, behavior, timestamp, endTimestamp, duration_ms, payload, depth`
- Use `Blob` + `URL.createObjectURL` + `<a download>` pattern (same as sample log)
- Button: "📊 Export CSV" in a new "Export" section or header dropdown

#### SVG/PNG Gantt Export
- Render current Gantt view to SVG using the same layout math as `GR.render()`
- For PNG: draw to offscreen `<canvas>`, then `canvas.toBlob()`
- Offer format toggle in export modal

#### JSON Tree Export
Export the full parsed `S.trees` object as pretty-printed JSON:
- Includes all nodes, durations, timestamps, payloads
- Interoperable: can be imported into other tools

---

### ⚙ Config & Rules Group

#### Rule Test Suite
A "Test All Rules" panel that runs each rule against a user-provided set of sample lines:
- Input: textarea with sample log lines
- Output: table showing which rules matched which lines
- Warn on rules that match nothing across all samples
- Warning on ambiguous rules (two rules match the same line)

#### Config Versioning
Add a `_meta` key to the config JSON:
```json
"_meta": {
  "version": 3,
  "changelog": [
    {"v": 3, "date": "2026-06-25", "note": "Added HTTP-RESP rule"},
    {"v": 2, "date": "2026-06-20", "note": "Changed TX regex"}
  ]
}
```
- Auto-increment version on every save
- Diff view: side-by-side JSON comparison (previous vs current) in a modal

#### Individual Rule Import/Export
- "Share" button on each rule card → downloads a single-rule JSON file
- Import button in rule list → picks a single-rule JSON and appends it

#### Rule Ordering (Drag-and-Drop Priority)
Since the parser uses first-match-wins, rule order matters:
- Make rule cards in the sidebar draggable (HTML5 Drag API)
- Persist new order to `S.cfg.elementRules`
- Show order numbers (1, 2, 3…) on each card
- "Move to top" / "Move to bottom" buttons as alternatives

---

### 🎨 UX Polish Group

#### Pin/Bookmark Events with Sticky Notes
- Right-click (or long-press) on any tree node → "📌 Pin this event"
- Pinned events show a yellow star badge
- Sticky note textarea in a mini popover
- Pinned events panel in sidebar (new "📌 Pins" tab)
- Persisted to session storage (cleared on new parse)

#### Right-Click Context Menu
On tree nodes:
- Copy raw log line
- Copy element name
- Filter to this thread only
- Set as timeline focus (center Gantt on this event)
- Pin event / Add note
- Implemented as a custom `div` positioned at mouse coords

#### Keyboard Navigation (j/k//)
- `j` / `k` — move focus up/down in tree
- `/` — open search box to filter tree nodes by element name or rule name
- `Enter` — expand/collapse focused node
- Requires tracking a `focusedNode` index in state

#### Saved Parse Sessions
Store last 5 sessions in IndexedDB:
- Session = config + log file reference (FS API handle) + thread filter
- "Recent Sessions" section in Config panel
- Click to restore: re-opens handles if still granted, otherwise prompts re-select

---

## Phase 2 — Intelligence Layer (v3.0)

**Status: Planned** · Month 3–6

> [!NOTE]
> Begin after all Phase 1 items are complete. This phase introduces significant new JS modules within the single file.

### 📊 Statistical Engine

#### Per-Rule Latency Distribution
After parsing, compute for each rule with `stackBehavior='push'`:
- Collect all `duration` values across all threads and events
- Calculate P50, P95, P99, max
- Display in a new "Stats" view tab with a table

**New section:** `§JS-21 STATS ENGINE`

#### Histogram Panel
For each rule: render a micro histogram (Canvas 2D, ~120×40px) showing duration buckets.
Shown inline in the stats table row on expand.

#### Multi-Session Comparison
Allow parsing two log files and showing side-by-side P95 latency tables:
- "Compare" mode toggle in control bar
- Two file selectors (A/B)
- Diff table with green/red arrows indicating regression/improvement

### 🚨 Anomaly Detection

#### Statistical Outlier Flagging
For each event, flag if `duration > mean + 2*stddev` for its rule:
- Red border on outlier bars in Gantt
- `[OUTLIER]` badge in tree node
- Outlier count in stats bar

#### Configurable SLA Thresholds
Add `slaThresholdMs` to each rule's schema:
- Input field in rule editor modal
- During render: events exceeding SLA shown with red border + tooltip "SLA: 500ms"
- New "SLA Breaches" summary panel

#### Error Cascade Analysis
Identify the first ERROR/WARN inline event before each slow push/pop block:
- "Potential cause" annotation on slow blocks in tree view

### 🔗 Correlation Engine

#### Trace ID Linking
New capture mapping field: `correlationId`:
- If multiple rules capture `correlationId`, events with matching IDs are linked across threads
- New "Trace" view tab — shows all events for a given correlation ID across all threads

#### Transaction Dependency Graph
Canvas 2D interactive node-link diagram:
- Nodes = elementNames; edges = "B started after A completed" within same thread
- **This is where Graphify integration adds maximum value**

### 🗺 Enhanced Timeline

#### Swimlane View
New Gantt variant: all threads as parallel horizontal lanes with shared X axis:
- Each thread gets a row header on the left
- Events from all threads rendered with synchronized time axis
- Canvas 2D rendering (replaces innerHTML approach)

#### Zoom/Pan Gantt
Canvas 2D Gantt with:
- Mouse wheel zoom (time axis)
- Click-drag pan
- Pinch zoom on touch devices

#### Mini-map Navigator
Small thumbnail of full timeline beneath Gantt for navigation

---

## Phase 3 — Collaboration (v4.0)

**Status: Roadmap** · Month 6–12

> [!NOTE]
> Requires an optional lightweight Node.js companion server for team features. The core HTML file still works standalone.

### 📦 Rule Registry

#### Community Rule Packs
- "Import from URL" button in Config panel
- Fetches a JSON array of rules from a URL
- Preview before importing (table with rule names/behaviors)
- Curated packs: Spring Boot, Hibernate, Kafka, AWS SDK, Tomcat

#### Organisation Registry
- Config field: `registryUrl` pointing to an internal server
- LogLens fetches available packs from the registry on startup
- Version pinning: `@1.2.3` syntax

### 📝 Annotations

#### Sticky Notes on Tree Nodes
- Full sticky note modal with rich text (Markdown)
- Stored in `.lls` session file format

#### Named Analysis Sessions (.lls files)
New session file format (JSON):
```json
{
  "version": 1,
  "config": { ...configObject },
  "logFileName": "app.log",
  "parseResult": { ...trees },
  "annotations": { "nodeId": "note text" },
  "createdAt": "ISO timestamp"
}
```

### 📋 Report Generation

#### PDF Report Generator
Use browser Print API (`window.print()`) with print-specific CSS:
- Executive summary section
- Stats table
- Gantt as SVG
- Top anomalies table
- Controlled via a print-only stylesheet

#### Report Templates
Selectable: Executive Summary | Developer Deep-Dive | SLA Breach | Incident Post-Mortem

---

## Phase 4 — Ecosystem Integration (v5.0)

**Status: Roadmap** · Month 12–18

> [!NOTE]
> Connector plugin model — each connector is an optional JS module (ES module, importable via dynamic `import()`).

### 📡 Live Log Streams

#### WebSocket Log Tail
- New "Live" tab in control bar
- WebSocket URL input + Connect button
- Messages parsed in real-time using existing rule engine
- Rolling buffer of last N events (configurable)
- Animated live indicator

#### Server-Sent Events Consumer
Similar to WebSocket but for SSE endpoints.

### 🔌 Observability Backends

#### Elasticsearch / OpenSearch
- Query panel: index pattern + Lucene query + time range
- Fetches log lines via Search API
- Results fed into parse engine

#### Grafana Loki
- LogQL query input
- Converts Loki log stream entries to parseable lines

### 🎫 Ticketing

#### JIRA Issue Creation
- Right-click anomaly → "Create JIRA Issue"
- Pre-populated: summary, description with Gantt screenshot, labels
- Requires JIRA API token in Settings (stored in localStorage)

### 🔁 REST API Surface

#### Headless Parse Endpoint
A companion Deno/Bun script:
```bash
deno run loglens-server.js --port 3000
# POST /parse  body: { logContent, config }  → JSON tree
```

---

## Phase 5 — Platform & Ecosystem (v6.0)

**Status: Vision** · Month 18–24

> [!NOTE]
> Major architectural milestone: Tauri desktop app + Rust/WASM parser core + CLI.

### 🖥 Desktop App (Tauri)
- Tauri v2 (Rust + WebView2) — Windows/macOS/Linux
- Target binary size: <10 MB
- Native file associations (`.log`, `.lls`)
- System tray agent with live monitoring badge
- Auto-update channel (stable/beta)
- SQLite WASM for full-text session search

### ⌨ CLI Tool
```bash
loglens parse --config rules.json app.log > result.json
loglens report --format pdf --template exec --input result.json
loglens watch --config rules.json /var/log/app.log  # live tail
```

### 🧩 Plugin SDK
- Public JS API for plugins: `LogLens.registerRenderer()`, `LogLens.registerExporter()`, `LogLens.registerAnalyser()`
- CSP-enforced iframe sandboxing
- Official plugin store

### 🦀 Rust/WASM Parser Core
- Replace JS Web Worker parser with Rust compiled to WASM
- Target: 10–20× throughput vs JS worker
- SIMD-accelerated regex via Hyperscan compiled to WASM
- Incremental re-parse: only process changed lines since last parse

### 🏢 Enterprise Edition
- SSO / SAML 2.0 for optional team server
- RBAC: rule packs, reports, connectors scoped by role
- Audit logging: every config change, parse session, export
- Air-gap deployment: zero telemetry, on-prem pack registry

---

## Verification Plan

### Automated Tests (to be added in Phase 1)
The rule test suite (Phase 1) will serve as the regression suite:
- Each rule has sample lines that should match
- Run `loglens parse --self-test` (Phase 5 CLI) to verify all rules

### Manual Verification Per Feature
- **Performance:** Time parsing of 100 MB log, 500 MB log on mid-range hardware
- **Virtual scroll:** Navigate tree with 50k+ nodes; confirm no browser lag
- **Export:** Open exported HTML report in a different browser with no internet; confirm fully functional
- **Gzip:** Parse a `.log.gz` file; confirm identical results to uncompressed version
- **Drag-and-drop:** Drop a log file onto the Gantt area; confirm it is accepted and parsed

### Phase Milestones (Acceptance Criteria)
- **Phase 1:** 500 MB log parsed in <10s; shareable HTML report viewable without LogLens
- **Phase 2:** Top-3 latency culprits identified with P95 stats in <60s after opening a log
- **Phase 3:** Post-mortem PDF with annotated traces created in <10 minutes after incident
- **Phase 4:** LogLens connects to org observability stack in <15 minutes; JIRA ticket raised without leaving browser
- **Phase 5:** Signed desktop binary installable via `winget install LogLens`

---

## Open Questions

> [!IMPORTANT]
> **Graphify Integration Detail:** The user requested "attach graphify to the project". This has been noted in PROJECT_CONTEXT.md and AGENTS.md — Graphify will be used for data visualization (transaction graphs, histograms, dependency diagrams). If Graphify has a specific integration API or import format, please clarify.

> [!NOTE]
> **Phase Prioritization within Phase 1:** Should all feature groups in Phase 1 be treated as equal priority, or should Export Surface (shareable reports) be prioritized first since it provides immediate user value?

> [!NOTE]
> **Canvas 2D vs innerHTML Gantt:** The roadmap (Phase 2 architecture) calls for migrating the Gantt from innerHTML to Canvas 2D. Should this migration happen in Phase 1 as groundwork, or stay as Phase 2 work?
