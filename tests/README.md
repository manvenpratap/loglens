# LogLens — Regression Test Suite

End-to-end browser automation tests for **LogLens** (`loglens.html`).
All tests run against the local single-file HTML app using **Playwright + pytest**.

---

## Structure

```
tests/
├── conftest.py                    # Shared fixtures & helpers
├── requirements.txt               # Python dependencies
├── test_01_onboarding.py          # Onboarding overlay + first-run guide
├── test_02_view_navigation.py     # Tab switching, Settings/Help/Split views
├── test_03_parser.py              # WM.parse stack behaviours (push/swap/popAll/inline)
├── test_04_command_palette.py     # Ctrl+K, search, Enter, Escape, recent history
├── test_05_event_inspector.py     # Inspector open/close, metadata, Escape dismiss
├── test_06_settings_preferences.py  # App Prefs accordion (Performance, Appearance)
├── test_07_trace_explorer.py      # Trace view, metric cards, search, active select
├── test_08_timeline_nav.py        # Mini-map panel, chips, zoom presets, ARIA
├── test_09_ai_insights.py         # AI Insights card, severity, ARIA, empty state
├── test_10_focus_mode.py          # F-key toggle, toast, sidebar, sessionStorage
├── test_11_accessibility.py       # Skip link, aria-live, chip ARIA, keyboard access
├── test_12_log4j_import.py        # Log4j Config XML Import
├── test_13_rule_creator.py        # Unified Rule Creator & Tooltips
└── test_14_unparsed_analyzer.py   # Unparsed Analyzer Create Rule flow
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
| Command Palette | test_04_command_palette | 7 |
| Event Inspector | test_05_event_inspector | 5 |
| Settings & Preferences | test_06_settings_preferences | 4 |
| Trace Explorer | test_07_trace_explorer | 8 |
| Timeline Navigator | test_08_timeline_nav | 8 |
| AI Insights Engine | test_09_ai_insights | 9 |
| Focus Mode | test_10_focus_mode | 9 |
| Accessibility Polish | test_11_accessibility | 8 |
| Log4j Config XML Import | test_12_log4j_import | 1 |
| Unified Rule Creator & Tooltips | test_13_rule_creator | 8 |
| Unparsed Analyzer | test_14_unparsed_analyzer | 1 |
| **Total** | | **83** |

---

## Agent Rules (for future AI sessions)

> When implementing any new feature in `loglens.html`:
> 1. **Write tests first** (or immediately after) in a new `tests/test_NN_...py` file.
> 2. **Run** `./run_tests.sh tests/test_NN_...py` to verify before committing.
> 3. **Run** `./run_tests.sh` (full suite) to catch regressions.
> 4. **Never delete** existing test files — extend them if a feature changes.
> 5. **Update this README's Coverage Map** when adding new test files.
> 6. After all tests pass, `git add tests/ pytest.ini run_tests.sh && git commit`.
