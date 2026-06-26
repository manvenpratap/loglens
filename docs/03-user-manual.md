# LogLens User Manual

---

## Document Control

| Field | Description |
| :--- | :--- |
| **Document Name** | LogLens User Manual |
| **Product Name** | LogLens |
| **Version** | v6.2 |
| **Date** | June 26, 2026 |
| **Author** | Antigravity AI & Technical Documentation Specialist |
| **Intended Audience** | End Users, Developers, Operations Engineers, Customer Support Teams |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Product Layout Overview](#2-product-layout-overview)
3. [Prerequisites and Browser Compatibility](#3-prerequisites-and-browser-compatibility)
4. [Quick Start Guide](#4-quick-start-guide)
5. [Step-by-Step Walkthroughs](#5-step-by-step-walkthroughs)
6. [Visualization Guides](#6-visualization-guides)
7. [Advanced Features and Integrations](#7-advanced-features-and-integrations)
8. [Troubleshooting Guide](#8-troubleshooting-guide)
9. [Appendix: Keyboard Shortcuts Reference](#9-appendix-keyboard-shortcuts-reference)
10. [Appendix: Required Screenshots to Capture](#10-appendix-required-screenshots-to-capture)

---

## 1. Introduction

Welcome to **LogLens**, a browser-based, privacy-first log analysis and visualization workbench. LogLens allows you to transform raw, unstructured log files into interactive waterfall timelines, execution trees, and dependency graphs. Because LogLens runs entirely client-side, your data never leaves your computer, ensuring compliance with corporate privacy policies.

---

## 2. Product Layout Overview

The LogLens user interface is divided into three functional areas:

```
+-----------------------------------------------------------------------------------+
| HEADER (Search, Badges, Export, Theme Toggle, Sidebar Button)                     |
+-----------------------------------------------------------------------------------+
| SIDEBAR PANELS            | RESULTS WORKSPACE                                     |
| - CONFIG: Manage rules    | - VIEW TABS: Select Split, Gantt, Tree, Stats, Graph  |
| - SETTINGS: Customizations| - STATISTICS CHIPS: View parse speed and file sizes   |
| - LOG4J: Import patterns  | - DISPLAY CONTAINER: View execution timelines, trees  |
| - HELP: Pins, bookmarks   |                      and anomaly lists                |
+-----------------------------------------------------------------------------------+
```

---

## 3. Prerequisites and Browser Compatibility

### Browser Expectations
LogLens is optimized for modern web browsers. It requires support for HTML5, Web Workers, CSS Grid, and the File System Access API.
* **Recommended Browsers**: Google Chrome (v90+), Microsoft Edge (v90+), Apple Safari (v15+), Mozilla Firefox (v95+).

### Supported File Types
* Raw text logs (`.log`, `.txt`, `.csv`)
* Gzipped files (`.gz`)
* LogLens Saved Sessions (`.lls`)
* LogLens JSON Rule Configurations (`.json`)

---

## 4. Quick Start Guide

To parse a log file in under 60 seconds:
1. Open the `loglens.html` file in your browser.
2. Select **Download Sample Log** from the Help panel to get a test file.
3. Drag and drop the downloaded file onto the LogLens window.
4. Click **Parse** in the control bar.
5. Explore the parsed events in the default **Split View**.

---

## 5. Step-by-Step Walkthroughs

### 5.1. Creating a Configuration Rule

#### Goal
Create a custom parsing rule using the guided interface.

#### Prerequisites
- An open instance of LogLens.
- A sample log line matching the pattern you want to parse.

#### Steps
1. Open the left sidebar and click on the **Config** tab.
2. Click the **Add Rule** button.
3. Paste a sample log line into the input area.
4. Highlight the timestamp within the log line and select **Timestamp** from the token list.
5. Highlight the thread identifier and select **Thread**.
6. Set the stack behavior (e.g., choose **Push** to open a timed block, or **Pop** to close one).
7. Assign an accent color and emoji icon.
8. Click **Save Rule**.

```
+----------------------------------------------------------------------------------+
|                            GUIDED RULE WIZARD MODAL                              |
+----------------------------------------------------------------------------------+
| Paste Sample Line:                                                               |
| [2026-06-26 09:12:00.124] INFO [worker-1] Service - HTTP-REQ /api/data           |
|                                                                                  |
| Tokens Selected:                                                                 |
|  [Timestamp] -> (\d{4}-\d{2}-\d{2} ...)                                          |
|  [Thread]    -> \[(\S+)\]                                                        |
|  [Payload]   -> /api/data                                                        |
|                                                                                  |
| Accent Color: [ Blue (#58a6ff) ]   Icon: [ 🌐 ]                                  |
|                                                                                  |
|                                                     [ Cancel ] [ Save Rule ]     |
+----------------------------------------------------------------------------------+
```

#### What Happens Next
The new rule is compiled and added to the configuration sidebar. The system will now match this pattern on subsequent parses.

---

### 5.2. Parsing Log Files

#### Goal
Decompress and parse local log files.

#### Prerequisites
- LogLens rules loaded in the configuration panel.
- A log file saved locally.

#### Steps
1. Click the **Select Log File** button in the top control bar, or drag the log file onto the viewport drop zone.
2. If the file is a `.gz` archive, LogLens will decompress it in the browser.
3. The control bar will display the file name and size.
4. Click **Parse**.
5. The progress bar will update as the file is processed.
6. Once complete, the view updates to display the parsed results.

#### Tips
> [!TIP]
> If parsing takes too long, you can adjust the chunk size in the Settings panel or click the **Abort** button to stop parsing and view the events processed up to that point.

---

## 6. Visualization Guides

### 6.1. Timeline / Gantt View
The Gantt view displays parsed events as a horizontal waterfall chart, allowing you to quickly spot delays and parent-child execution paths.

```
+----------------------------------------------------------------------------------+
| GANTT TIMELINE DISPLAY                                                           |
+----------------------------------------------------------------------------------+
| Thread: worker-1 [ Zoom: =======o==== ]                                          |
|                                                                                  |
| 0ms                  200ms                  400ms                  600ms         |
| +------------------------------------------------------------------------------+ |
| | [▶ Transaction Begin]                                                        | |
| |   [🌐 HTTP Request: /api/auth]                                               | |
| |     [🗄 DB Query: auth.lookup]                                               | |
| |   [🌐 HTTP Request: /api/inventory]                                          | |
| +------------------------------------------------------------------------------+ |
+----------------------------------------------------------------------------------+
```

* **Timeline Zoom**: Use the zoom slider in the control bar, or hold the `Alt` key while scrolling your mouse wheel over the timeline.
* **Timeline Pan**: Click and drag your mouse cursor horizontally across the timeline to pan left or right.
* **Critical Path**: Click the **Critical Path** toggle to highlight the sequence of events that contributed most to the overall execution duration.

### 6.2. Execution Tree View
The Tree view offers a nested list of log events, showing parent-child hierarchies.
* **Expand/Collapse**: Click the arrow chevron to the left of any event node to toggle its children.
* **Inline Metrics**: Each row displays duration, self-time, and severity badges (e.g. hotspot indicator `↑↑85%`).

---

## 7. Advanced Features and Integrations

### 7.1. Deploy Compare Mode (Multi-File Diff)

#### Goal
Compare execution trees side-by-side to detect changes or regressions between two logs.

#### Prerequisites
- Two different log files loaded in the workspace.

#### Steps
1. Upload both log files. You will see two chips in the multi-file bar.
2. Click the **Compare Files** button in the control bar.
3. The workspace will update to show the Deploy Compare Mode view.
4. Click on any row in the comparison table to open the side-by-side execution trees.
5. Divergent events are highlighted with red and green indicator lines.

---

### 7.2. LogLens Query Language (LQL)

#### Goal
Filter and analyze log events using SQL-like queries.

#### Steps
1. Navigate to the **Query** tab in the results workspace.
2. Enter your query in the text box. Example:
   ```sql
   SELECT ruleName, duration WHERE duration > 500 ORDER BY duration DESC LIMIT 5
   ```
3. Click **Run Query** or press `Ctrl + Enter`.
4. The matching events are displayed in a table below the query input.
5. Click **Export CSV** to save the query results to your machine.

---

### 7.3. JIRA Ticket Integration

#### Goal
Create a JIRA issue directly from an event outlier or SLA breach.

#### Prerequisites
- JIRA API webhook URLs configured in the Settings sidebar.

#### Steps
1. Locate an outlier event (flagged in red in the Tree view or Stats panel).
2. Right-click the event node to open the context menu.
3. Select **Create JIRA Ticket**.
4. A draft window opens with pre-populated details (timestamp, thread, trace, log payload).
5. Click **Submit** to create the ticket.

---

## 8. Troubleshooting Guide

| Symptom | Cause | Resolution |
| :--- | :--- | :--- |
| **Blank screen after loading log** | The file timestamp pattern did not match the global settings. | Open the Config panel and adjust the `globalTimestampPattern` regex. |
| **"Out of Memory" alert** | Browser memory limits reached when parsing a very large log file. | Open Settings -> Performance, reduce parse chunk size to 256KB, and reload. |
| **Rules are not saving** | Browser IndexedDB storage is full or disabled. | Clear the cache using the Performance panel in the Settings sidebar. |
| **0 matches for a rule** | The regex pattern has a syntax error or does not match the log format. | Test the rule in the Rule Test Suite modal to debug matching issues. |

---

## 9. Appendix: Keyboard Shortcuts Reference

| Shortcut | Action | Scope |
| :--- | :--- | :--- |
| `Ctrl + K` / `Cmd + K` | Toggle Command Palette | Global |
| `/` | Focus search bar | Workspace |
| `Alt + 1` | Switch to Split View | Workspace |
| `Alt + 2` | Switch to Timeline View | Workspace |
| `Alt + 3` | Switch to Tree View | Workspace |
| `Alt + [` | Switch to previous Thread | Workspace |
| `Alt + ]` | Switch to next Thread | Workspace |
| `Escape` | Close active modal, dialog, or search query | Global |

---

## 10. Appendix: Required Screenshots to Capture

1. **Screenshot Name**: `Gantt_Waterfall_Timeline`
   * **Screen/View**: Timeline/Gantt Workspace.
   * **Exact UI Area**: Waterfall bar displays, event rows, and latency tags.
   * **Purpose**: Guide the user on interpreting Gantt charts.
   * **Recommended Caption**: *Figure 1. Gantt waterfall timeline showing nested operations.*

2. **Screenshot Name**: `Deploy_Compare_SideBySide`
   * **Screen/View**: Compare Files workspace.
   * **Exact UI Area**: Side-by-side execution trees with red/green highlights.
   * **Purpose**: Guide users through log comparison tasks.
   * **Recommended Caption**: *Figure 2. Side-by-side Deploy Compare View.*

3. **Screenshot Name**: `Query_LQL_Interface`
   * **Screen/View**: LQL Workspace.
   * **Exact UI Area**: Query input panel, history pills, and results table.
   * **Purpose**: Show query search execution.
   * **Recommended Caption**: *Figure 3. LogLens Query Language (LQL) interface.*
