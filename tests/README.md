# LogLens — Regression Test Suite

End-to-end browser automation tests for **LogLens** (`loglens.html`).
All tests run against the local single-file HTML app using **Playwright + pytest-asyncio**.

---

## 📁 Test Suite Structure

The test suite is organized into consolidated test modules for fast, session-scoped browser execution:

```
tests/
├── conftest.py                                      # Shared fixtures, browser lifecycle & helpers
├── requirements.txt                                 # Python dependencies (playwright, pytest, pytest-asyncio)
├── test_consolidated_navigation_and_shell.py        # 26 tests: Navigation, onboarding, 2-tier tabs, split sync, simultaneous sideways advancement, responsive containers, split view toolbar controls, comprehensive in-app documentation & user manual
├── test_consolidated_parser_and_ingestion.py        # 14 tests: Web Worker parser, multiline stack traces, Log4j XML, unparsed analyzer
├── test_consolidated_rules_and_regex.py             # 31 tests: Rule wizard, regex builder, token palette, group combiner, undo/redo, pipe-delimited auto-splitting
├── test_consolidated_settings_and_accessibility.py  # 8 tests: 4-pillar settings, appearance options, SLA guardrails configuration, a11y skip links, focus mode, AI insights
├── test_consolidated_visualizations_and_telemetry.py# 27 tests: Execution tree, resizable columns, thread grouping, split view row color sync, swimlane studio, enhanced trace explorer, rule editor telemetry mapping, tree multi-selection & rule creation
└── test_stress_and_performance.py                   # 3 tests: Trace Explorer memoized sorting performance, virtual scrolling DOM node ceiling, and 2.5k synthetic dataset ingestion throughput
```

**Total: 109 automated regression tests** with 100% pass rate.

---

## 🛠️ Prerequisites & Setup

```bash
# Install Python dependencies
pip install -r tests/requirements.txt

# Install Playwright Chromium browser binary
playwright install chromium
```

---

## 🚀 Running Tests

Use the canonical test runner script `./run_tests.sh`:

```bash
# Run the full regression test suite (95 tests)
./run_tests.sh

# Run a specific consolidated module
./run_tests.sh tests/test_consolidated_visualizations_and_telemetry.py
./run_tests.sh tests/test_consolidated_navigation_and_shell.py
./run_tests.sh tests/test_consolidated_parser_and_ingestion.py
./run_tests.sh tests/test_consolidated_rules_and_regex.py
./run_tests.sh tests/test_consolidated_settings_and_accessibility.py

# Run by keyword filter
./run_tests.sh -k "trace_dropdown"
./run_tests.sh -k "column_resizing"
./run_tests.sh -k "thread_grouping"

# Verbose output with stack traces
python3 -m pytest tests/ -v
```

> **Note on Sandbox / Permissions**: Playwright launches Chromium with native Mach port rendezvous. On macOS, running outside sandbox mode (`BypassSandbox: true` in agent runners) is required for Chromium to spawn its helper renderer processes.

---

## 🧩 Fixtures (`conftest.py`)

| Fixture | Scope | Description |
|---|---|---|
| `page_with_data` | function | Browser page loaded with onboarding dismissed and synthetic multi-thread logs (`S.trees`) injected |
| `blank_page` | function | Clean browser page at initial load state (no logs, onboarding displayed) |
| `browser_instance` | session | Session-scoped Chromium browser instance shared across tests to optimize execution speed (~3.5x faster) |

### Synthetic Baseline Data (`page_with_data`)
Injects 20 `main` thread events (every 5th marked as `ERROR`) and 10 `worker` thread events, spanning multiple threads with varying execution durations and SLA breaches. Provides all telemetry, tree, and timeline tests with a realistic, deterministic baseline.

---

## 📊 Coverage Map

| Module Suite | Scope & Features Covered | Test Count |
|---|---|:---:|
| `test_consolidated_navigation_and_shell.py` | • Onboarding modal lifecycle & dismissal<br>• Demo showcase end-to-end user journey<br>• 2-Tier navigation header & Analysis dropdown<br>• Command Palette (`Cmd+K` / `Ctrl+K`) search & actions<br>• Split View 32px lockstep row vertical alignment<br>• Split View bidirectional loop-safe scroll synchronization<br>• **Split View simultaneous sideways timeline advancement** (revealing Gantt bars dynamically as user scrolls down)<br>• Split View CSS Container Query responsive column adaptation<br>• Stat Cards scope exclusivity in Stats view & Graph persistence<br>• **Comprehensive In-App Documentation & User Manual**: 7 specialized tabs, field reference tables, 9 visualizer explanations, stack behavior rules, capture group mappings, LQL cookbook, shortcuts, and instant search filter | **26** |
| `test_consolidated_parser_and_ingestion.py` | • Web Worker parser (`WM.parse`) orchestration<br>• Stack behavior engine: `push`, `pop`, `inline` events<br>• Multiline block parsing & stack trace aggregation<br>• Log4j / Logback XML configuration importer<br>• Unparsed log line analyzer & regex pattern generator<br>• Multi-thread discovery scan (first 200 KB) & `.gz` decompression | **14** |
| `test_consolidated_rules_and_regex.py` | • Unified rule creation wizard & preset templates<br>• Token palette (timestamp, UUID, thread, duration tokens)<br>• Interactive regex builder tracks & visual segments<br>• Multi-capture group combiner (`#rg-combine-bar`)<br>• Regex undo/redo history buffer<br>• Auto-detect log format & file retention<br>• Custom log pattern setup journey & 100% parse verification | **31** |
| `test_consolidated_settings_and_accessibility.py` | • 4-Pillar settings dashboard (Rules, Sources, Storage, Prefs)<br>• Keyboard navigation (`J`, `K`, numbers `1`–`4`, shortcuts)<br>• Accessibility skip links & ARIA treeitem / tab roles<br>• Focus Mode (`F` hotkey) and uncluttered workspace<br>• AI Insights engine & anomaly summary cards<br>• Appearance customization (monospace typography, rounded bars, high contrast) and SLA guardrails recalculation | **8** |
| `test_consolidated_visualizations_and_telemetry.py` | • Event Inspector drawer lifecycle, metadata & auto-close<br>• **Enhanced Trace Explorer**: 4 KPI cards (P95 Latency), quick filter chips (SLA, Multi-Thread, Healthy), interactive column header sorting, latency distribution bars, slowest operation callouts, and direct Timeline/Tree view jumps<br>• **Dynamic Trace ID Filter Dropdown** mounting, search & clearing<br>• Execution Tree 3-zone architecture & depth filtering (`D1..D3`, `All`)<br>• Execution Tree **CSS custom properties virtualized column resizing**<br>• Execution Tree **inline column filter bar (`#tree-filter-bar`)**<br>• Execution Tree **critical path toggle (`✦ Critical`) & dimming**<br>• Execution Tree **thread grouping (`.tree-thr-group-row`) & color coding**<br>• **Execution Tree multi-row selection (Shift/Ctrl), floating action pill (`#tree-selection-bar`), context menu rule generator, and modal pre-population**<br>• **Split View row background color & border sync with Tree**<br>• **Timeline & Split View full scrollable width row background coverage** (preventing color clipping when scrolled right)<br>• **Advanced Swimlane Studio**: interval-scheduling concurrency stacking, KPI headers, crosshair guideline, hover card, search filtering, and multi-mode grouping<br>• Interactive inline `{ } Payload` button & anchored popover dialog<br>• Timeline Navigator mini-map (`TIMELINE_NAV`) view isolation & zoom<br>• Waterfall timeline bounded scrolling & header synchronization | **27** |
| `test_stress_and_performance.py` | • **Trace Explorer memoized sorting performance** (`< 25ms` benchmark over 20 repeated operations)<br>• **Execution Tree virtual scrolling DOM node ceiling** (`<= 55` nodes maintained during rapid scrolling)<br>• **Synthetic dataset ingestion throughput** (2,500 operations ingested and rendered in `< 800ms`) | **3** |
| **Total** | **Comprehensive End-to-End Regression Test Suite** | **109** |

---

## 📐 Conventions & Best Practices

### Writing New Tests
1. Locate the appropriate consolidated suite (`tests/test_consolidated_*.py`) based on the feature domain.
2. Decorate test functions with `@pytest.mark.asyncio`:
   ```python
   @pytest.mark.asyncio
   async def test_feature_behavior_and_expectation(page_with_data):
       page = page_with_data
       ...
       assert_no_critical_errors(page)
   ```
3. Use shared fixtures (`page_with_data` or `blank_page`) from `conftest.py`. Never instantiate ad-hoc browser sessions.
4. Always end tests with `assert_no_critical_errors(page)` to verify no uncaught JS exceptions occurred.
5. Keep tests independent and self-contained.

### Zero-Regression Policy
- **Never delete existing tests**: If UI behaviors change, update the expected selectors or assertions rather than deleting tests.
- **Run the full suite before shipping**: Always execute `./run_tests.sh` to confirm all 95 tests pass.
- **Automated shipping**: Run `./ship.sh "<commit message>"` to synchronize `dist/index.html`, commit, and push upstream.
