# LogLens Functional Specifications Document

---

## Document Control

| Field | Description |
| :--- | :--- |
| **Document Name** | LogLens Functional Specifications Document |
| **Product Name** | LogLens |
| **Version** | v6.2 |
| **Date** | June 26, 2026 |
| **Author** | Antigravity AI & Technical Documentation Specialist |
| **Intended Audience** | Developers, QA Engineers, Product Owners, Technical Support, UAT Reviewers |

---

## Table of Contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Product Context](#2-product-context)
3. [System Overview](#3-system-overview)
4. [Screen Architecture and Navigation Model](#4-screen-architecture-and-navigation-model)
5. [Global UI Shell Specification](#5-global-ui-shell-specification)
6. [Sidebar Panels and Workflows](#6-sidebar-panels-and-workflows)
7. [Main Work Area and Control Bar](#7-main-work-area-and-control-bar)
8. [Analysis Views Specification](#8-analysis-views-specification)
9. [Interaction and PERSISTENCE Systems](#9-interaction-and-persistence-systems)
10. [Data Object Schema Definitions](#10-data-object-schema-definitions)
11. [Event and Action Matrix](#11-event-and-action-matrix)
12. [Validation and Error Handling Rules](#12-validation-and-error-handling-rules)
13. [Appendix: Required Screenshots to Capture](#13-appendix-required-screenshots-to-capture)

---

## 1. Purpose and Scope

This document defines the functional requirements, field-level user interface elements, operational logic, constraints, and data object models for **LogLens**. This specification serves as the core source of truth for developer implementation, quality assurance test case definition, and system integration verification.

---

## 2. Product Context

LogLens is a self-contained, browser-only, zero-dependency log visualization and analysis application. It is delivered to the client as a single HTML file containing embedded CSS styles and JavaScript logic. No backend application servers or cloud resources are required to run the tool under standard local operations.

---

## 3. System Overview

```
+-----------------------------------------------------------------------------------------+
|                                    LOGLENS ENGINE                                       |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|   +--------------------------+                                +----------------------+  |
|   |    FILE SYSTEM INGEST    |                                |   CONFIG MANAGER     |  |
|   |  - Gzip Decompression    |                                | - IndexedDB Sync     |  |
|   |  - Directory Watcher     |                                | - Config Versioning  |  |
|   +------------+-------------+                                +----------+-----------+  |
|                |                                                         |              |
|                v                                                         v              |
|   +----------------------------------------------------------------------+-----------+  |
|   |                              WEB WORKER PARSER (W_SRC)                           |  |
|   |  - Processes log data in chunks                                                  |  |
|   |  - Runs rule regex evaluations on each log line                                  |  |
|   |  - Maintains thread stacks (push/pop/inline)                                     |  |
|   +--------------------------------------+-------------------------------------------+  |
|                                          |                                              |
|                                          v                                              |
|   +----------------------------------------------------------------------------------+  |
|   |                               VIEW CONTROLLER (UI.rv)                            |  |
|   |  - Renders virtual tree list / Gantt timeline                                    |  |
|   |  - Computes pattern anomalies, thread correlations, and contribution heatmaps    |  |
|   +----------------------------------------------------------------------------------+  |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```

---

## 4. Screen Architecture and Navigation Model

The application viewport is split into three permanent segments:
1. **Header Bar**: Top-level status indicator, search box, and global actions.
2. **Left Navigation Sidebar**: Collaspible panel displaying Config, Settings, Log4j import, or Help utilities.
3. **Results Area**: Segment containing view tabs, statistics, and visualizations (Waterfall timelines, execution trees, dashboards, or query inputs).

```
+-----------------------------------------------------------------------------------------+
| HEADER BAR (Logo | Watcher | Config State | Search Box | Export Button | Theme Toggle) |
+-----------------------------------------------------------------------------------------+
| NAVIGATION  | RESULTS WORKSPACE                                                        |
| SIDEBAR     |                                                                           |
| - Config    | +-----------------------------------------------------------------------+ |
| - Settings  | | VIEW TABS (Split View | Timeline / Gantt | Tree | Stats | Graph | 3D) | |
| - Log4j     | +-----------------------------------------------------------------------+ |
| - Help      | | STATS SUMMARY CHIPS BAR                                               | |
|             | +-----------------------------------------------------------------------+ |
| (Collapses  | | RESULTS / TIMELINE DISPLAY VIEWER                                     | |
|  to icons)  | |                                                                       | |
|             | +-----------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------------+
```

---

## 5. Global UI Shell Specification

### 5.1. Header Controls

* **Name**: Global Header Bar
* **Location in UI**: Top of the screen (100% width, 48px height)
* **Purpose**: Provide global search, layout selectors, status indicators, and export commands.
* **Visibility Conditions**: Always visible.
* **User Roles**: All users.

#### Control Catalog

| Control ID | Label | Control Type | Purpose | Data Type | Default Value | Editable | Triggered Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `hdr-search` | "Search..." | Text Input | Search text and tags across the execution tree. | String | `""` | Yes | Triggers `SEARCH_HL.highlight` on input. |
| `search-hl-count` | N matches | Status Badge | Displays number of matching events. | String | Hidden | Read-only | Updates dynamically on search match. |
| `btn-exp-menu` | "Export" | Dropdown Button | Exposes data and session export formats. | Menu Trigger | Disabled | Read-only | Toggles class `.open` on `#exp-menu`. |
| `btn-theme-toggle` | Emoji (🌙/☀️) | Button | Toggle app design between dark and light themes. | Button | `🌙` | Read-only | Changes color classes on `html` root. |
| `hdr-unmatched` | "⚠️ N Unmatched" | Badge Link | Alerts user to push blocks missing matching pops. | Badge | Hidden | Read-only | Jumps focus to first unmatched node. |

---

## 6. Sidebar Panels and Workflows

### 6.1. Config Manager Panel

* **Name**: Config Panel
* **Location in UI**: Sidebar first tab
* **Purpose**: Import, export, delete, and modify rules matching log text patterns.
* **Visibility Conditions**: Visible when Config tab is active.
* **Inputs**: JSON configuration uploads, manual text rules.
* **Outputs**: Updated configuration stored in local IndexedDB.

#### Control Catalog

| Control ID | Label | Control Type | Purpose | Data Type | Default Value | Editable | Triggered Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `btn-connect-dir` | "Connect Config DB" | Button | Accesses local rule directories via File System Access API. | Button | Active | Read-only | Triggers native file selector. |
| `btn-import-cfg` | "Import Config" | Button | Import JSON log matching rules from disk. | Button | Active | Read-only | Launches hidden file input. |
| `btn-add-rule` | "Add Rule" | Button | Create a parsing pattern via Advanced or Guided wizard. | Button | Active | Read-only | Opens Rule Modal dialog `#mm`. |

---

## 7. Main Work Area and Control Bar

### 7.1. Ingestion Control Bar

* **Name**: Control Bar
* **Location in UI**: Top of the Results Workspace
* **Purpose**: Select, scan, parse, and monitor log files.
* **Visibility Conditions**: Always visible.

#### Control Catalog

| Control ID | Label | Control Type | Purpose | Data Type | Default Value | Editable | Triggered Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `btn-file-select` | "Select Log File" | Button | Launch file explorer window to load raw log file. | Button | Active | Read-only | Launches system file browser. |
| `btn-compare-files` | "Compare Files" | Button | Activate Deploy Compare Mode comparing loaded files. | Button | Hidden | Read-only | Triggers `DIFF.compare()`. |
| `btn-parse` | "Parse" | Button | Start processing selected file chunks via Web Worker. | Button | Disabled | Read-only | Launches `WM.parse()`. |
| `progress-bar-wrap` | Progress Bar | Graphic | Displays log file parsing completion percentage. | Visual | Hidden | Read-only | Updates dynamically on worker chunk load. |

---

## 8. Analysis Views Specification

### 8.1. Split View Mode

* **Name**: Split View Workspace
* **Location in UI**: Center Results viewport (tab index 0)
* **Purpose**: Side-by-side execution display. Left panel contains Gantt waterfall, right panel contains Virtual Tree.
* **Visibility Conditions**: Visible when `S.viewMode === 'split'`.
* **Inputs**: Mouse drag on split handle resizing width proportions (10% to 90%).
* **Outputs**: Resized view boundaries.

### 8.2. Gantt Waterfall View

* **Name**: Gantt View Workspace
* **Location in UI**: Center Results viewport (tab index 1)
* **Purpose**: Horizontal timeline chart illustrating duration spans of push/pop logs.
* **Visibility Conditions**: Visible when `S.viewMode === 'gantt'`.

#### Timeline Controls

| Control ID | Label | Control Type | Purpose | Data Type | Default Value | Editable | Triggered Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `gantt-zoom-slider` | Zoom Slider | Slider Input | Scales timeline width via CSS variable `--g-zoom`. | Integer | `1` (100%) | Yes | Multiplies event row display widths. |
| `g-bar` | Operation block | Graphic Bar | Visual representation of block duration. Hover displays details. | Visual | Rule Accent Color | Read-only | Hover opens context tooltip. |

---

## 9. Interaction and Persistence Systems

### 9.1. Context Menu actions
Right-clicking any execution row inside the virtualized tree or Gantt timeline displays a custom modal context menu (`#ctx-menu`) positioned at the cursor coordinates.

* **Menu Actions**:
  1. **Focus Node**: Hides all sibling events, focusing exclusively on the selected sub-tree.
  2. **Pin / Bookmark Node**: Adds target node reference to the Help tab sidebar with custom notes.
  3. **Copy Line Payload**: Extracts and copies payload fields to the clipboard.
  4. **Highlight Matches**: Highlights matching sibling rule identifiers.

### 9.2. IndexedDB Session Caching (`IDB` namespace)
To prevent processing delays when re-opening large logs, LogLens implements local cache serialization using IndexedDB storage.
* **Logic**: On parsing completion, LogLens computes a SHA-256 hash of the log content. It stores the resulting parsed event tree and metadata arrays inside IndexedDB under the calculated hash key.
* **Hit Check**: On loading a log file, LogLens checks IndexedDB for matching hashes. If a match is found, it prompts: `"Cached session found. Load instantly?"` Clicking Load retrieves the cached session in milliseconds, skipping the parsing process.

---

## 10. Data Object Schema Definitions

### 10.1. Configuration Object Schema
```json
{
  "globalSettings": {
    "appName": "LogLens Default",
    "globalTimestampPattern": "^(\\d{4}-\\d{2}-\\d{2}[T ]\\d{2}:\\d{2}:\\d{2}[.,]\\d{3})",
    "description": "Standard diagnostic pattern rules configuration."
  },
  "elementRules": [
    {
      "id": "r_tx_start",
      "name": "Transaction Begin",
      "regexPattern": "TX-BEGIN\\s+(\\S+)",
      "captureMapping": {
        "1": "elementName"
      },
      "stackBehavior": "push",
      "visualStyle": {
        "accentColor": "#58a6ff",
        "icon": "▶"
      },
      "slaThresholdMs": 1000,
      "disabled": false
    }
  ]
}
```

---

## 11. Event and Action Matrix

```
+------------------------------------------------------------------------------------------+
|                                EVENT AND ACTION FLOWS                                    |
+------------------------------------------------------------------------------------------+
|  USER ACTION                   | UI STATE CHANGE               | ENGINE ACTION           |
+--------------------------------+-------------------------------+-------------------------+
|  Drag and Drop Log file        | Shows parsing dropzone overlay| Reads file metadata     |
|                                |                               | Decompresses gzip data  |
+--------------------------------+-------------------------------+-------------------------+
|  Input search text             | Filters tree display          | Runs SEARCH_HL to add   |
|                                | Highlights matching text      | mark.hl tags            |
+--------------------------------+-------------------------------+-------------------------+
|  Click "Compare Files"         | Opens Deploy Compare panel    | Executes LCS alignment  |
|                                |                               | Parses rules side-by-side|
+--------------------------------+-------------------------------+-------------------------+
|  Modify rule (Quick Edit)      | Refreshes configuration panel | Calls CFG.persist()     |
|                                |                               | Updates IndexedDB       |
+--------------------------------+-------------------------------+-------------------------+
```

---

## 12. Validation and Error Handling Rules

### 12.1. Regex Pattern Validation
When saving an edit on the Rule Modal:
* **Validation**: Checks if input regex is valid using `new RegExp(pattern)`.
* **Failure Handling**: If invalid, applies class `.error` border to input field, displays toast: `"Invalid regex pattern configuration."`, and prevents dialog closure.

### 12.2. Out-of-Memory Safeguards
When parsing logs larger than 500MB:
* **Handling**: Adjusts chunk size dynamically (splits file into 1MB chunks instead of 512KB). If browser memory limits are reached, the system aborts parsing, returns successfully parsed blocks, and displays toast: `"Memory limit warning: Parsing halted. Displaying partial events."`

---

## 13. Appendix: Required Screenshots to Capture

1. **Screenshot Name**: `Rule_Wizard_Guided`
   * **Screen/View**: Configuration sidebar panel -> Guided tab modal.
   * **Exact UI Area**: Rule Creation Wizard steps with line selection mapping.
   * **Purpose**: Detail step-by-step rule authoring interfaces.
   * **Recommended Caption**: *Figure 3. Guided wizard view showing line segment mappings.*

2. **Screenshot Name**: `Timeline_Zoom_Pan`
   * **Screen/View**: Timeline/Gantt Workspace.
   * **Exact UI Area**: Waterfall bar displays, zoom slider controls, and active timeline grids.
   * **Purpose**: Detail waterfall diagnostic capabilities.
   * **Recommended Caption**: *Figure 4. Gantt waterfall workspace with interactive zoom sliders.*

3. **Screenshot Name**: `Quick_Edit_Popover`
   * **Screen/View**: Config Panel Sidebar -> Rules list.
   * **Exact UI Area**: Popover card overlay next to rule card showing editSwatches.
   * **Purpose**: Detail inline rapid editing flows.
   * **Recommended Caption**: *Figure 5. Quick edit popover overlay on a selected rule.*
