# LogLens Product Capability Document

---

## Document Control

| Field | Description |
| :--- | :--- |
| **Document Name** | LogLens Product Capability Document |
| **Product Name** | LogLens |
| **Version** | v6.2 |
| **Date** | June 26, 2026 |
| **Author** | Antigravity AI & Technical Documentation Specialist |
| **Intended Audience** | Product Managers, Stakeholders, Architects, Sales Engineers, Implementation Teams |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Product Overview](#product-overview)
3. [Product Goals and Design Intent](#product-goals-and-design-intent)
4. [Target Users and Personas](#target-users-and-personas)
5. [Key Use Cases](#key-use-cases)
6. [Capability Map](#capability-map)
7. [Detailed Capability Sections](#detailed-capability-sections)
8. [Feature Inventory Matrix](#feature-inventory-matrix)
9. [End-to-End Workflow Summary](#end-to-end-workflow-summary)
10. [Strengths and Differentiators](#strengths-and-differentiators)
11. [Operational Considerations](#operational-considerations)
12. [Constraints and Assumptions](#constraints-and-assumptions)
13. [Appendix](#appendix)

---

## 1. Executive Summary

Modern enterprise systems generate massive volumes of logs, often unstructured or semi-structured, which serve as the primary diagnostic record during software development, debugging, and incident response. Traditional log analysis pipelines rely on complex, centralized observability platforms (e.g., Splunk, Datadog, ELK stack). While powerful, these platforms present significant friction: they require high subscription costs, complex ingestion pipelines, long query latency, and, most critically, they mandate sending sensitive customer or system data to third-party cloud environments.

**LogLens** solves this diagnostic friction by introducing a zero-dependency, single-file HTML, client-side log analysis workbench. Operating entirely in the browser, LogLens performs local log ingestion, regex-based metadata rule evaluation, and hierarchical visualization without sending a single byte of data to external servers. It converts static flat log files into interactive, hierarchical timelines, dependency graphs, and structural execution trees. By combining local performance, absolute privacy, and visual representation, LogLens enables engineering and support teams to resolve issues in seconds rather than hours.

---

## 2. Product Overview

LogLens is a client-side web application packaged as a single, self-contained HTML file. It requires no installation, command-line dependencies, or database configuration. Users open `loglens.html` directly in any modern web browser, drag-and-drop log files, and instantly apply metadata rules to parse logs into high-fidelity visualizations.

```
+----------------------------------------------------------------------------------------+
|                                  LOGLENS WORKBENCH                                     |
+----------------------------------------------------------------------------------------+
|  [ Ingest Logs Local ] ---> [ Match Rules Local ] ---> [ Timeline / Gantt / Trees ]    |
|  - Drag & Drop Files        - High-perf Worker         - Outliers & SLAs               |
|  - Decompress Gzip          - Custom Regex Patterns    - Thread Overlaps & Heatmaps    |
+----------------------------------------------------------------------------------------+
|                              100% LOCAL & CLIENT-SIDE ONLY                             |
+----------------------------------------------------------------------------------------+
```

### Core Value Pillars

* **Absolute Data Privacy**: Log parsing, processing, and visualization take place exclusively within the browser's JavaScript environment and virtual sandbox. Sensitive transaction numbers, payload data, and security keys remain securely on the user's machine.
* **Instant Start (Zero Ingest Overhead)**: Bypasses elasticsearch indexes or cloud collector pipelines. Ingests and highlights structured intervals immediately.
* **Metadata-Driven Execution Models**: Transforms log files from flat text streams into parent-child execution blocks representing nesting and latency intervals.

---

## 3. Product Goals and Design Intent

The design of LogLens is governed by three core architectural values:

1. **Lightweight Accessibility**: Packaging the entire application as a single file allows distribution via email, download, or hosting on static pages. No server side, Node.js running backend, or database setup is needed to launch the app.
2. **Interactive Visual Speed**: Navigating log lines should feel like exploring code. Tree rendering and timeline waterfall grids must update instantly. Features like virtualized scrolling, dynamic SVG rendering, and Canvas 2D charts are chosen for performance over template frameworks.
3. **Flexible Adaptability**: Developers should be able to create match configurations for any log format—be it custom system logging, standard Log4j patterns, JSON dumps, or binary-origin text.

---

## 4. Target Users and Personas

### Persona A: The Site Reliability Engineer (SRE) / Incident Responder
* **Pain Point**: Production outages require rapid log triage, but searching cloud observability tools is slow, or log volume indexing delays hide critical errors.
* **How LogLens Helps**: The SRE downloads the raw log from the target node, drops it into LogLens, and uses the Outlier Detection and Timeline view to locate the root cause in milliseconds.

### Persona B: The Technical Support Engineer
* **Pain Point**: Customers share diagnostic logs containing highly sensitive PII, making cloud uploads a violation of security compliance guidelines.
* **How LogLens Helps**: LogLens processes the customer log locally, ensuring compliance with data storage mandates while allowing the agent to visualize the customer's call tree.

### Persona C: The Backend Developer
* **Pain Point**: Validating local multi-thread execution flows and database latency is tedious using terminal grep commands.
* **How LogLens Helps**: The developer configures SQL capture rules to inspect parallel transaction trees in Split view, measuring self-time and identifying bottleneck queries.

---

## 5. Key Use Cases

### Incident Triage (Hotspot Analysis)
During an active production latency incident, a developer imports a 100MB server log. Using the Stats panel's Outlier Table, they immediately identify that a database transaction block (`DB-QUERY-START` to `DB-QUERY-END`) for a specific SKU took 12.4 seconds, breaching the configured 500ms SLA. They right-click the outlier and select "Focus Node" to view the surrounding context.

### Deployment Regression Testing (Compare Mode)
An engineer tests a code optimization release by comparing staging logs before and after the change. They drop both files into the Multi-File interface and select "Compare Files". The Deploy Compare Mode overlays the rule frequency distributions side-by-side, revealing that the post-release system executes 3x more database queries than the pre-release version, identifying a regression.

### Off-Grid Customer Support Diagnostics
An on-site deployment engineer working in a secure, air-gapped data center needs to debug a middleware service. Without internet access or cloud tools, they open the pre-saved single-file `loglens.html` on their laptop, parse the local logs, and isolate the thread exception.

---

## 6. Capability Map

LogLens capabilities are organized into ten functional domains:

```
+--------------------------------------------------------------------------------------+
|                                   LOGLENS CAPABILITIES                               |
+--------------------------------------------------------------------------------------+
| 1. DATA INGESTION       | 2. CONFIGURATION        | 3. RULE AUTHORING                |
| - Local File Upload     - Config DB (IndexedDB)   - Guided Wizard                    |
| - Drag & Drop Anywhere  - Version History         - Token Builder / Regex Editor     |
| - Gzip Decompression    - Raw JSON Import/Export  - Log4j / Logback XML Conversion   |
+-------------------------+-------------------------+----------------------------------+
| 4. PARSING & ENGINE     | 5. VISUALIZATION        | 6. EXPORT & PERSISTENCE          |
| - Web Worker Parsing    - Timeline (Gantt Waterfall)- Session Save/Load (.lls files)  |
| - Inline/Push/Pop Stack - Execution Tree (Virtual)- Self-Contained HTML Report       |
| - Thread Discovery      - Split View / 3D Canvas  - CSV / JSON / SVG / PNG Export    |
+-------------------------+-------------------------+----------------------------------+
| 7. COLLABORATION        | 8. CONNECTIVITY         | 9. ADMINISTRATION                |
| - Threaded Comments     - WebSocket Log Tail      - App Preferences (S.appPrefs)     |
| - Bookmark Pinning      - Loki & CloudWatch REST  - Storage Cleaning                 |
| - URL Hash Deep Sharing - Git Config Synchronizer - Plugin Hook Loader               |
+--------------------------------------------------------------------------------------+
```

---

## 7. Detailed Capability Sections

### 7.1. Data Ingest Engine
* **Purpose**: Load local logs into browser memory without network transit.
* **Business Value**: Protects corporate compliance by processing logs locally, preventing data leakage.
* **User Value**: Fast file loading via stream utilities.
* **Main UI Entry Points**: Drop zone overlay, Control bar "Select File" button.
* **Dependencies/Prerequisites**: File System Access API support in browser (Chrome/Edge/Safari).
* **Typical Workflow**: 
  1. User drags a `.log` or `.gz` file onto the browser window.
  2. The decompression stream unpacks gzip data if applicable.
  3. The system scans the first 200KB for active thread IDs.
* **Outputs/Results**: List of active thread chips, updated status header showing active filename.

### 7.2. Config and Versioning Database
* **Purpose**: Manage, persist, and track changes to rule collections.
* **Business Value**: Encourages standardization of rules across engineering teams.
* **User Value**: Safely experiment with regex matching rules without losing previous configurations.
* **Main UI Entry Points**: Sidebar Config panel, "Config History" button.
* **Dependencies/Prerequisites**: IndexedDB browser storage.
* **Typical Workflow**:
  1. User edits an HTTP request match rule.
  2. The system auto-increments the configuration version and logs a diff snapshot.
  3. The user reviews historical diffs in the history panel.
* **Outputs/Results**: Version history database with restore actions and side-by-side diff.

### 7.3. Guided Rule Authoring
* **Purpose**: Simplify the process of creating regex parser rules.
* **Business Value**: Lowers the barrier to entry for team members unfamiliar with regular expressions.
* **User Value**: Create rules by selecting keywords and clicking tokens.
* **Main UI Entry Points**: Sidebar "Config" panel -> "Add Rule" -> Wizard tab.
* **Dependencies/Prerequisites**: None.
* **Typical Workflow**:
  1. User pastes a sample log line.
  2. The wizard segments the line. The user assigns elements (e.g. Timestamp, Thread, Level).
  3. The Regex Explainer splits the resulting pattern into annotated segments.
* **Outputs/Results**: A validated parser rule added to the active configuration list.

### 7.4. Multi-File Deploy Compare
* **Purpose**: Compare log execution profiles between two separate log files.
* **Business Value**: Rapid regression identification during release cycles.
* **User Value**: Side-by-side visual difference mappings of rule sequences.
* **Main UI Entry Points**: Multi-file chip bar -> "Compare Files" button.
* **Dependencies/Prerequisites**: At least two loaded log files.
* **Typical Workflow**:
  1. User uploads `app-v1.log` and `app-v2.log`.
  2. The system runs dual background worker parses.
  3. The user clicks "Compare Files" to view deltas and LCS-aligned execution trees.
* **Outputs/Results**: Latency/count comparison table and side-by-side difference view.

### 7.5. LogLens Query Language (LQL)
* **Purpose**: SQL-like query interface for filtering and aggregating log events.
* **Business Value**: Flexible data extraction without requiring specialized developer scripts.
* **User Value**: Search parsed nodes using standard SQL syntax.
* **Main UI Entry Points**: Results view tab bar -> "Query" tab.
* **Dependencies/Prerequisites**: Successfully parsed log files.
* **Typical Workflow**:
  1. User navigates to the Query tab.
  2. The user types `SELECT ruleName, duration WHERE duration > 200 ORDER BY duration DESC LIMIT 10`.
  3. The system parses, filters the event pool, and renders a table.
* **Outputs/Results**: Interactive tabular dataset, exportable to CSV.

---

## 8. Feature Inventory Matrix

| Module | Feature Name | Description | Primary User | Value Delivered |
| :--- | :--- | :--- | :--- | :--- |
| **Ingestion** | Drag & Drop | Ingestion of any log file by dragging it onto the window. | Developer / Support | Removes file browser dialog friction. |
| **Ingestion** | Gzip Decompression | Real-time browser-based decompression of compressed log packages. | SRE / Incident Responder | No manual decompression required. |
| **Config** | Log4j XML Import | Auto-generates regex matching rules from standard Log4j logging configurations. | System Administrator | Rapid tool onboarding. |
| **Config** | Git Synchronizer | Synchronizes active rule configurations with a Git repository. | SRE Lead | Ensures matching rule consistency across teams. |
| **Rule Editor** | Regex Explainer | Visual breakdown of regex patterns with color-coded tokens. | Developer | Simplifies regular expression debugging. |
| **Parser Engine** | Web Worker Parsing | Background processing of logs in multi-thread environment. | SRE / Incident Responder | Maintains UI responsiveness during large parses. |
| **Visualization** | Timeline (Gantt) | Renders waterfall execution path of push/pop rules. | Developer | Highlights slow operations. |
| **Visualization** | Stats Heatmaps | Renders thread overlap correlations and calendar heatmaps. | Incident Responder | Quickly exposes resource contention and timing hotspots. |
| **Productivity** | Quick Edit | Inline popup editor for rule name, color, and SLA. | Developer | Edit configuration properties without opening nested dialogs. |
| **Productivity** | Undo / Redo | Track modifications to rules configuration. | Support Engineer | Prevents accidental configuration loss. |
| **Collaboration** | Threaded Comments | Add nested comment trees to log event nodes. | Developer / Lead | Document investigation steps for reviews. |
| **Collaboration** | URL Deep Sharing | Encode active views, filters, and selections into URL hash. | Developer | Share diagnostic states with team members via chat. |

---

## 9. End-to-End Workflow Summary

```
+-----------------------------------------------------------------------------------+
|                        TYPICAL DIAGNOSTIC WORKFLOW IN LOGLENS                     |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [STEP 1: LOAD RULES]      -->   [STEP 2: DRAG LOGS]      -->   [STEP 3: PARSE]   |
|  - Load pre-configured JSON      - Drop server.log.gz           - Background worker|
|  - Or import Log4j XML           - Auto-decompression           - Parses in chunk  |
|                                                                                   |
|                                         |                                         |
|                                         v                                         |
|                                                                                   |
|  [STEP 6: EXPORT/SHARE]    <--   [STEP 5: ANNOTATE]       <--   [STEP 4: ANALYZE] |
|  - Generate self-contained       - Pin outlier nodes            - Locate hotspot   |
|    HTML report                   - Add threaded comments        - Run LQL queries  |
|  - Copy Deep Link Hash           - Check SLA breaches           - View correlation |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 10. Strengths and Differentiators

* **No Cloud / Local Only**: In an industry where observability data breaches are common, LogLens offers a zero-transit environment. Data does not leave the local browser frame.
* **Metadata-Driven Timelines**: Unlike simple log viewers that only highlight text matching keywords, LogLens interprets push/pop behavior to build nested execution trees.
* **Self-Contained Exports**: The HTML report exporter packages the active viewer, the matched configurations, and the specific log subset into a single file, allowing developers to share interactive diagnostics.

---

## 11. Operational Considerations

### 11.1. Browser Sandbox Limitations
LogLens runs entirely in the browser. It cannot read files directly from the host operating system without user permission. Large logs are processed in chunks to keep the browser tab responsive.

### 11.2. Memory Management
The browser engine holds parsed events in memory. For log files larger than 500MB, LogLens automatically adjusts chunk sizes. Users can manage resource utilization through the Performance Panel in the Settings sidebar.

### 11.3. Local Cache Persistence
LogLens stores configurations and the last five parse sessions locally using IndexedDB. This ensures rule modifications persist across browser updates without requiring a cloud profile database.

---

## 12. Constraints and Assumptions

* **Browser Compliance**: Requires modern CSS grid and Flexbox support. Tested on Google Chrome, Apple Safari, and Mozilla Firefox.
* **Timestamp Dependency**: To build structured waterfall trees, log lines must have parsing rules that identify timestamps.
* **JavaScript Dependency**: Disabling JavaScript in the browser renders the application inoperable.

---

## 13. Appendix

### 13.1. Glossary

| Term | Definition |
| :--- | :--- |
| **Push Rule** | A rule that opens a block. Placed on the thread call stack to calculate duration when popped. |
| **Pop Rule** | A rule that closes the last open push block on the thread, calculating elapsed time. |
| **Inline Rule** | A standalone event representing a single log entry, such as an exception dump or log warning. |
| **Hotspot** | A node that accounts for a high percentage of its parent node's execution time. |
| **LQL** | LogLens Query Language. A SQL-like syntax used to query parsed event attributes. |
| **LCS** | Longest Common Subsequence. An algorithm used in Deploy Compare Mode to align execution trees. |

### 13.2. Acronyms
* **SLA**: Service Level Agreement
* **IDB**: IndexedDB
* **FIFO**: First-In, First-Out
* **PII**: Personally Identifiable Information
* **CSV**: Comma-Separated Values
* **SVG**: Scalable Vector Graphics

---

### Required Screenshots to Capture
1. **Screenshot Name**: `Ingestion_Dropzone`
   * **Screen/View**: Main empty state viewport.
   * **Exact UI Area**: Center dashed container showing ingest instructions.
   * **Purpose**: Guide the user on dragging logs to initialize.
   * **Recommended Caption**: *Figure 1. Drag and drop zone with interactive file upload instructions.*

2. **Screenshot Name**: `Stats_Heatmaps`
   * **Screen/View**: Stats Panel view.
   * **Exact UI Area**: Thread overlap correlation grid and calendar heatmap dashboard.
   * **Purpose**: Show visual hotspots.
   * **Recommended Caption**: *Figure 2. Stats dashboard showing thread correlation matrix and contribution calendar.*
