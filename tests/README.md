# LogLens — Regression Test Suite

End-to-end browser automation tests for **LogLens** (`loglens.html`).
All tests run against the local single-file HTML app using **Playwright + pytest**.

---

## Structure

```
tests/
├── conftest.py                    # Shared fixtures, browser lifecycle & helpers
├── requirements.txt               # Python dependencies
├── test_consolidated_navigation_and_shell.py         # Onboarding, Demo showcase, 2-tier nav, command palette, tabs
├── test_consolidated_parser_and_ingestion.py         # WM.parse stack behaviors, Log4j import, multiline, unparsed analyzer
├── test_consolidated_rules_and_regex.py              # Rule creator, regex builder, auto-sniff, pattern journey, capture groups
├── test_consolidated_settings_and_accessibility.py   # Settings preferences, a11y skip links, focus mode, AI insights
└── test_consolidated_visualizations_and_telemetry.py # Gantt, Waterfall scrolling, Trace Explorer, Execution Tree, Event Inspector
```

---

## Prerequisites

```bash
pip install -r tests/requirements.txt
playwright install chromium
```

---

## Running Tests

```bash
# Run the full suite
./run_tests.sh

# Run a single module
./run_tests.sh tests/test_09_ai_insights.py

# Run by keyword
./run_tests.sh -k "focus"

# Run only smoke tests (when marked)
./run_tests.sh -m smoke

# Verbose output
python3 -m pytest tests/ -v
```

---

## Fixtures (conftest.py)

| Fixture | Scope | Description |
|---|---|---|
| `page_with_data` | function | Chromium page with onboarding dismissed and synthetic `S.trees` injected |
| `blank_page` | function | Chromium page at load state — no data, onboarding shown |

### `page_with_data` Demo Data

Injects 20 `main` thread events (every 5th is `ERROR`) and 10 `worker` thread events, spanning 2 threads with varying durations and SLA breaches. Gives all feature tests a consistent, realistic baseline.

---

## Conventions

### Adding a New Test
1. Create `tests/test_NN_feature_name.py`
2. Use `page_with_data` (data loaded) or `blank_page` (empty state)
3. All test functions must be `async def test_...` decorated with `@pytest.mark.asyncio`
4. Use `from conftest import assert_no_critical_errors` for JS error checks
5. Keep each test focused on one assertion (one reason to fail)

### Test Naming
```
test_<what>_<expected_outcome>
```
Examples:
- `test_focus_mode_activates_via_f_key`
- `test_ai_insights_card_visible_in_stats`

### Marking Slow Tests
```python
@pytest.mark.slow
async def test_large_log_parse_performance(blank_page):
    ...
```
Run slow tests explicitly: `./run_tests.sh -m slow`

---

## Coverage Map

| Module / Feature | Test File | # Tests |
|---|---|---|
| Onboarding + First-Run UX | test_01_onboarding | 5 |
| View navigation & panel routing | test_02_view_navigation | 6 |
| Parser (stack behaviours) | test_03_parser | 4 |
| Command Palette | test_04_command_palette | 2 |
| Event Inspector | test_05_event_inspector | 2 |
| Settings & Preferences | test_06_settings_preferences | 1 |
| Trace Explorer | test_07_trace_explorer | 2 |
| Timeline Navigator | test_08_timeline_nav | 2 |
| AI Insights Engine | test_09_ai_insights | 2 |
| Focus Mode | test_10_focus_mode | 2 |
| Accessibility Polish | test_11_accessibility | 2 |
| Log4j Config XML Import | test_12_log4j_import | 1 |
| Unified Rule Creator & Tooltips | test_13_rule_creator | 9 |
| Unparsed Analyzer | test_14_unparsed_analyzer | 3 |
| Regex Pattern Undo/Redo | test_15_regex_undo_redo | 1 |
| Interactive Regex Builder | test_16_interactive_regex_builder | 1 |
| Auto-Detect & File Retention | test_17_auto_detect_and_retention | 5 |
| Custom Log Pattern Journey & Rule Setup | test_18_custom_log_pattern_journey | 5 |
| Multiline Block & Class Payload Parsing | test_19_multiline_block_payload | 6 |
| Demo Showcase All Features | test_20_demo_showcase | 3 |
| Custom Log Setup Journey & 100% Parsing | test_21_custom_log_setup_journey | 5 |
| 2-Tier Navigation & Toolbar Utilities | test_22_two_tier_navigation | 4 |
| Combine Capture Groups into 1 Element | test_23_combine_capture_groups | 4 |
| Waterfall View Scrolling & Header Sync | test_24_waterfall_scrolling | 5 |
| Execution Tree Telemetry, Controls, Resizing, Filters & Critical Path | test_consolidated_visualizations_and_telemetry | 7 |
| Stat Cards Scope Exclusivity & Graph Navigation Persistence | test_consolidated_navigation_and_shell | 4 |
| Timeline Navigator View Isolation & Gantt Exclusivity | test_consolidated_visualizations_and_telemetry | 1 |
| Dynamic Trace Dropdown Interaction & Filtering | test_consolidated_visualizations_and_telemetry | 1 |
| **Total** | | **94** |

---

## Agent Rules (for future AI sessions)

> When implementing any new feature in `loglens.html`:
> 1. **Write tests first** (or immediately after) in a new `tests/test_NN_...py` file.
> 2. **Run** `./run_tests.sh tests/test_NN_...py` to verify before committing.
> 3. **Run** `./run_tests.sh` (full suite) to catch regressions.
> 4. **Never delete** existing test files — extend them if a feature changes.
> 5. **Update this README's Coverage Map** when adding new test files.
> 6. After all tests pass, `git add tests/ pytest.ini run_tests.sh && git commit`.
