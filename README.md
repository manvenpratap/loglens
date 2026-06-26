# 🔍 LogLens

**A browser-based, zero-install, privacy-first log analysis and visualization tool.**

LogLens transforms raw log files into interactive execution timelines, call trees, statistics dashboards, and graphs — all without uploading your data anywhere. Everything runs locally in your browser.

---

## ✨ Features at a Glance

| Category | Features |
|---|---|
| **Ingestion** | Local file select, drag-and-drop, multi-file sessions, `.gz` decompression, real-time log streaming |
| **Configuration** | JSON config, Log4j/Logback XML import, versioned config with changelog and diff |
| **Rule Authoring** | Guided wizard, advanced regex builder, token palette, live preview, community rule packs |
| **Parsing** | Multi-threaded log parsing, thread discovery scan, trace ID filtering, abort support |
| **Views** | Split, Timeline/Gantt, Execution Tree, Stats, Graph, 3D View, Query, Diff |
| **Annotations** | Per-node markdown notes with live preview |
| **Pins** | Bookmark important events, view them in the sidebar |
| **Exports** | CSV, JSON, SVG, PNG, interactive HTML report, `.lls` session file |
| **Integrations** | JIRA ticket creation, Git sync, cloud datasources, directory watcher, plugin sandbox |
| **Accessibility** | Full keyboard navigation, theme toggle (dark/light), command palette |

---

## 🚀 Quick Start

1. **Open** `loglens.html` in any modern browser (Chrome, Edge, Firefox, Safari).
2. **Load a config** — click the **Config** sidebar tab → **Import** an existing JSON config, or create a new one.
3. **Add rules** — click **+ Add Rule** to define patterns using the Guided Wizard or Advanced Regex Builder.
4. **Select a log file** — click **Select** (or drag and drop a `.log`, `.txt`, `.out`, or `.gz` file onto the page).
5. **Parse** — click the **Parse** button and watch progress in real time.
6. **Explore** — switch between **Split**, **Timeline**, **Tree**, **Stats**, **Graph**, and **3D View** tabs.

No installation. No server. No data leaves your machine.

---

## 📂 File Support

| Format | Notes |
|---|---|
| `.log` | Standard log text files |
| `.txt` | Plain text log output |
| `.out` | Process output files |
| `.gz` | Gzip-compressed logs — auto-decompressed in-browser |
| `.json` | Config import/export and session (`.lls`) files |
| `.xml` | Log4j / Logback / Log4j2 configuration import |

**Multi-file sessions** are supported — add multiple files with the **+** button and they are parsed together.

---

## 🧩 Core Concepts

### Config
A JSON object that defines your application's `globalSettings` and `elementRules`. It tells LogLens how to parse each line of your log file.

### Rules
Each rule is a regex pattern with:
- **Stack Behavior** — `push` (opens a timed block), `pop` (closes it and calculates duration), or `inline` (standalone point event).
- **Capture Mappings** — which regex capture group maps to `timestamp`, `thread`, `elementName`, `payload`, `correlationId`.
- **Visual Style** — custom accent color and icon for the rule.
- **SLA Threshold** — optional millisecond threshold; exceeded durations are flagged in red.

### Threads
LogLens automatically groups parsed events by thread ID. Use **Thread Discovery** (the scan button) to auto-detect all thread IDs from the first 200 KB of your log file.

### Sessions (`.lls`)
A session file saves the full parse result — config, trees, pins, annotations, and stats — so you can reload it later without re-parsing the original log file.

---

## 🖥️ Interface Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  Header: Logo | File badge | Status badge | Exports | Theme toggle  │
├──────────────┬──────────────────────────────────────────────────────┤
│              │  Controls: File select | Thread | Parse | Abort      │
│   Sidebar    ├──────────────────────────────────────────────────────┤
│              │  View tabs: Split | Timeline | Tree | Stats | Graph  │
│  ┌─────────┐ │              | 3D | Query | Diff                     │
│  │ Config  │ ├──────────────────────────────────────────────────────┤
│  │Settings │ │                                                      │
│  │ Log4j   │ │              Main Result Area                        │
│  │  Help   │ │   (empty state → parse results per active view)      │
│  └─────────┘ │                                                      │
└──────────────┴──────────────────────────────────────────────────────┘
```

---

## 📊 Analysis Views

### Split View
Side-by-side layout showing the Timeline (Gantt) and Tree simultaneously with a draggable divider.

### Timeline (Gantt)
Horizontal bar chart of all parsed events per thread, plotted on a shared time axis. Bars are color-coded by rule, and SLA violations are highlighted. Click any bar to focus the event in the Tree.

### Execution Tree
Hierarchical call tree of push/pop blocks and inline events. Supports:
- Expand / collapse all
- Keyboard navigation (`↑` `↓` `j` `k`, `/` to search, `P` to pin)
- Context menu (right-click) for copy, pin, annotate, focus in Timeline, create JIRA ticket
- Hotspot badges showing percentage of parent block time consumed
- Inline duration labels
- Annotation and pin indicators

### Stats
Dashboard cards showing:
- Total events, total duration, average duration, SLA violations
- Per-rule event counts and timing breakdowns
- Unparsed line count and percentage
- Thread distribution

### Graph
Force-directed graph of event relationships. Nodes represent unique element names; edges represent call frequency. Useful for identifying hotspots and dependency chains.

### 3D View
Three-dimensional visualization of the execution tree using WebGL. Rotate, pan, and zoom to explore deep call hierarchies spatially.

### Query View
Filter and search parsed events using structured query expressions.

### Diff View
Compare two config versions side-by-side to review rule additions, deletions, and modifications.

---

## ⚙️ Configuration Workflow

### Creating a New Config
1. Open the **Config** sidebar tab.
2. Click **New Config** and enter an app name.
3. Add rules using the **+ Add Rule** button.

### Importing from Log4j XML
1. Open the **Log4j** sidebar tab.
2. Click **Choose File** and select your `log4j.xml`, `logback.xml`, or `log4j2.xml`.
3. LogLens parses the appender conversion patterns and generates matching regex templates.
4. Select the patterns you want and click **Import Selected**.

### Config Versioning
Every time you save, LogLens automatically increments the config version and logs a changelog entry with a snapshot of the rules. Use the **Diff** view to compare any version against the current config.

---

## 🛠️ Rule Authoring

### Guided Wizard
1. Select a **Log Format** preset (Java Standard, Spring Boot, Log4j2, JSON, CSV, or Custom).
2. Enter **Keywords / Markers** — the exact strings that identify this event type (e.g., `TX-BEGIN`).
3. Choose **Match Mode** (Any / All keywords) and **Capture** (next word, rest of line, or nothing).
4. LogLens auto-generates the regex and shows a **Generated Pattern Preview**.
5. Enter a **Quick Test** sample line to verify the match.

### Advanced Regex Builder
Full manual regex control with:
- **Pattern Template** presets to start from
- **Token Builder** — click tokens to insert pre-built groups (timestamp, thread ID, UUID, duration, etc.) at the cursor position
- **Live Match Preview** — paste a sample line and see each capture group highlighted in a distinct color in real time
- **Explain Regex** — plain-English explanation of the current pattern
- **Capture Mappings** — assign capture group indices to semantic fields

### Rule Test Suite
Test all rules at once against a set of sample lines. Accessible via the Config panel footer. Reports which rules matched, which lines were matched, and total hit count.

### Community Rule Packs
Import pre-built rule packs for common frameworks:
- **Nginx** access logs
- **Log4j** standard
- **Spring Boot**
- **AWS CloudTrail**

Or supply a custom URL to fetch a pack from any CORS-enabled endpoint.

---

## 🔗 Integrations

### JIRA
Right-click any tree node → **Create JIRA Ticket**. Requires a JIRA base URL and webhook token configured in **Settings → Integrations**.

### Git Sync
Sync your config JSON to/from a Git repository. Configure a repository URL and personal access token in **Settings → Git Sync**.

### Cloud Datasources
Connect to remote log sources:
- **HTTP/REST** endpoints with bearer or basic auth
- **AWS CloudWatch Logs** — configure region, access key, secret, and log group
- **WebSocket** streams

Configure in **Settings → Cloud Datasource**. Use **Connect** to start streaming and **Disconnect** to stop.

### Real-Time Log Stream
Receive log lines via WebSocket in real time. Connect to a stream endpoint to continuously append events. Use **Pause** to hold the buffer and **Clear Log Stream** to reset.

### Directory Watcher
Point LogLens at a local directory path and enable **Auto Reload** to automatically re-parse when the watched file changes.

### Plugins
Load external JavaScript plugins into a sandboxed iframe. Plugins can extend parsing, add custom views, or integrate with external systems. Load via **Settings → Plugins**.

---

## 💾 Export Options

| Export | Format | Description |
|---|---|---|
| **CSV** | `.csv` | Flat tabular export of all parsed events |
| **JSON** | `.json` | Structured export of all event trees |
| **SVG** | `.svg` | Vector export of the current graph view |
| **PNG** | `.png` | Raster screenshot of the current view |
| **HTML Report** | `.html` | Fully self-contained interactive report — share with anyone, no LogLens required |
| **Session** | `.lls` | Full session snapshot — config + trees + pins + annotations, reloadable |
| **Rule Export** | `.json` | Export a single rule for sharing or backup |

Access all exports via the **Export** menu in the header or the keyboard shortcut.

---

## 📌 Pins & Annotations

### Pins
Bookmark any tree node by right-clicking → **Pin this event** or pressing `P` when a node is focused via keyboard. Pins appear in the **Help** sidebar tab with the node name, icon, and duration. Click the `×` to unpin.

### Annotations
Add a markdown note to any node by right-clicking → **Annotate event**. The annotation modal supports:
- Bold, italic, inline code
- Bullet lists and headers
- Hyperlinks
- Live markdown preview

Annotated nodes show a visual indicator in the Tree view.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Alt + T` | Toggle dark / light theme |
| `Alt + ←` / `Alt + →` | Previous / next thread |
| `Alt + 1` | Switch to Split view |
| `Alt + 2` | Switch to Timeline view |
| `Alt + 3` | Switch to Tree view |
| `↑` / `k` | Move up in Tree |
| `↓` / `j` | Move down in Tree |
| `/` | Search tree by element name |
| `P` | Pin focused tree node |
| `Esc` | Close modal / sheet / menu |
| `Ctrl + K` / `Cmd + K` | Open Command Palette |

### Command Palette
Press `Ctrl+K` (Windows/Linux) or `Cmd+K` (Mac) to open the command palette. Search for any view, export action, or command by name.

---

## 🗄️ Local Session Cache (IndexedDB)

LogLens automatically caches your last **5 parsed sessions** in the browser's IndexedDB. Each session is keyed by a SHA-256 hash of the file metadata and config, so the same file + config combination always resolves from cache. Cache is evicted on a least-recently-used basis when the limit is reached.

> **Note:** IndexedDB is local to the browser profile. Clearing browser data will clear the session cache.

---

## 🔒 Privacy

LogLens is **100% client-side**. Your log files and configs:
- Never leave your machine.
- Are never uploaded to any server.
- Are never sent to any analytics endpoint.

All processing happens in your browser tab using JavaScript Web Workers and IndexedDB.

---

## 🌐 Browser Requirements

| Browser | Minimum Version | Notes |
|---|---|---|
| Chrome / Edge | 89+ | Full support including gzip decompression |
| Firefox | 113+ | Full support |
| Safari | 16.4+ | Full support |

**Required browser features:** File API, IndexedDB, Web Workers, DecompressionStream (for `.gz`), WebGL (for 3D view), Clipboard API (for copy actions).

> If `DecompressionStream` is not available, `.gz` files will fail to decompress. Use an uncompressed log file in that case.

---

## 📁 Project Structure

LogLens ships as a **single self-contained HTML file**. Internally, it follows a logical modular architecture:

```
loglens.html
│
├── Styles (embedded)
│   ├── 01-tokens.css        Design tokens
│   ├── 02-base.css          Reset and base styles
│   ├── 03-layout.css        Page layout
│   ├── 04-components.css    UI components
│   ├── 05-views.css         Analysis view styles
│   ├── 06-utilities.css     Utility classes
│   ├── 07-states.css        State modifiers
│   ├── 08-responsive.css    Responsive breakpoints
│   └── 09-print.css         Print styles
│
└── Scripts (embedded)
    ├── 00-bootstrap.js      App initialization and event wiring
    ├── 01-constants.js      Enums and constants
    ├── 02-state.js          Application state (S)
    ├── 03-dom.js            DOM helpers (DOM)
    ├── 04-utils.js          Utility functions
    ├── 05-events.js         Event handling
    ├── 06-worker.js         Web Worker for parsing
    ├── 07-config.js         Config management (CFG)
    ├── 08-rules.js          Rule CRUD and ordering (RO)
    ├── 09-parser.js         Log parsing orchestration
    ├── 10-render-shell.js   Header, sidebar, controls
    ├── 11-render-gantt.js   Timeline / Gantt renderer
    ├── 12-render-tree.js    Execution tree renderer (TR)
    ├── 13-render-stats.js   Stats dashboard renderer
    ├── 14-render-graph.js   Graph renderer
    ├── 15-render-3d.js      3D view renderer
    ├── 16-annotations.js    Annotation system
    ├── 17-pins.js           Pin / bookmark system (PIN)
    ├── 18-exports.js        Export handlers (EXP)
    ├── 19-integrations.js   JIRA, Git, cloud datasources
    ├── 20-plugins.js        Plugin sandbox loader
    ├── 21-versioning.js     Config versioning and diff (VER)
    ├── 22-keyboard.js       Keyboard navigation (KBN)
    ├── 23-router-viewstate.js  View routing and state
    └── 24-app-init.js       Final app initialization
```

---

## 🧪 Rule Test Suite

Open the **Rule Test Suite** from the Config panel to validate all your rules at once:

1. Paste sample log lines (one per line) into the input area.
2. Click **Test All Rules**.
3. See per-rule match results — which lines each rule matched, and how many total hits were recorded.

This is useful for verifying rule coverage before running a full parse.

---

## 🧑‍💻 Contributing / Extending

LogLens is a single-file app. To extend it:

1. Locate the relevant logical module section in the `<script>` block (each module is clearly delimited by a `// JS-NN MODULE-NAME` comment).
2. Add constants in `JS-0 CONSTANTS`.
3. Add state shape in `JS-2 STATE`.
4. Implement the module logic in the appropriate section.
5. Wire events in `JS-0 BOOTSTRAP` / `JS-24 APP-INIT`.

For custom integrations or view extensions, consider writing a **Plugin** (see Integrations → Plugins above) to avoid modifying the core file.

---

## 📝 Sample Log Format

LogLens includes a **Download Sample Log** button in the Help panel. The sample log demonstrates:
- Transaction start/end markers (`push` / `pop` rules)
- Inline point events
- Multiple threads
- SLA-exceeding operations

Use it to explore the tool before connecting your own logs.

---

## 📄 License

LogLens is provided as a self-contained client-side tool. See the source file header for license details.

---

## 🙋 FAQ

**Does LogLens support streaming logs from a server?**
Yes. Configure a WebSocket endpoint in **Settings → Cloud Datasource** and click **Connect**. Incoming lines are parsed and appended to the tree in real time.

**Can I share my analysis with someone who doesn't have LogLens?**
Yes. Use **Export → HTML Report** to generate a fully self-contained interactive HTML file. The recipient can open it in any browser without needing LogLens.

**What happens if my regex doesn't match any lines?**
The Stats view will show an unparsed line count. Open the **Rule Test Suite** or use the **Live Match Preview** in the Advanced rule builder to diagnose the pattern.

**Can I use LogLens offline?**
Yes. Once the HTML file is loaded in the browser, it works entirely offline. No CDN resources are required.

**How many rules can a config have?**
There is no hard limit. Rule ordering matters — rules are applied in the order listed. Use drag-and-drop reordering in the Config panel to adjust priority.

**Is there a file size limit?**
LogLens parses in a Web Worker to avoid blocking the UI. Very large files (>500 MB) may be slow depending on the device. For extremely large files, consider pre-filtering with a tool like `grep` before loading.
