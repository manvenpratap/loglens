"""
test_18_custom_log_pattern_journey.py — LogLens Regression Suite
Tests: Ease of use and defect-free user journey for custom log patterns.
Covers:
  1. Empty-state entry point (+ Custom Rule Builder CTA).
  2. End-to-end custom pattern rule creation with Interactive Regex Builder.
  3. Format badge reflection and capture group mapping.
  4. Rule Test Suite (RTS) enablement and multi-line testing.
  5. Parsing custom lines into structured trees and rendering.
  6. Unparsed adaptive rescue flow for unknown custom patterns.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors, DISMISS_ONBOARDING_JS


@pytest.mark.asyncio
async def test_empty_state_custom_rule_builder_discovery(blank_page):
    """User on empty state can discover and immediately launch Custom Rule Builder."""
    page = blank_page

    # Dismiss onboarding welcome overlay and switch to empty state view
    await page.evaluate(DISMISS_ONBOARDING_JS)
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(300)

    # Empty state card actions must include the Custom Rule Builder CTA
    btn_custom = page.locator('#btn-emp-create-rule')
    await expect(btn_custom).to_be_visible()
    await expect(btn_custom).to_contain_text("Custom Rule Builder")

    # Clicking launches the Rule Creator modal
    await btn_custom.click()
    await page.wait_for_timeout(300)

    modal = page.locator('#mm')
    await expect(modal).to_be_visible()
    await expect(page.locator('#m-ttl')).to_contain_text("Add New Rule")

    # Verify rule modal inputs are active and configuration is initialized
    cfg_init = await page.evaluate("() => S.cfg !== null && Array.isArray(S.cfg.elementRules)")
    assert cfg_init is True

    # Close modal
    await page.locator('#btn-mx').click()
    await expect(modal).not_to_be_visible()

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_custom_log_pattern_interactive_builder_flow(blank_page):
    """User pastes a custom log line, selects pattern tokens, maps groups, and saves rule."""
    page = blank_page

    # Dismiss onboarding and show empty state view
    await page.evaluate(DISMISS_ONBOARDING_JS)
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(300)

    # Launch Rule Creator
    await page.locator('#btn-emp-create-rule').click()
    await page.wait_for_timeout(300)

    # Fill Rule Name and Stack Behavior
    await page.locator('#e-name').fill("Custom Auth Service")
    await page.locator('#e-beh').select_option("push")

    # Enter custom line of log
    sample_line = "2026-10-08 14:23:45.123 [worker-4] [auth-svc] INFO - User login ok user_id=42"
    tl_input = page.locator('#e-tl')
    await tl_input.fill(sample_line)
    await page.wait_for_timeout(300)

    # Check that format status badge recognizes custom pattern
    badge = page.locator('#preview-format-badge')
    await expect(badge).to_contain_text("Custom Pattern")

    # Badges must render in interactive builder tracks container
    tracks = page.locator('#rg-tracks-container')
    await expect(tracks).to_be_visible()
    badges = page.locator('.rg-match-badge')
    badge_count = await badges.count()
    assert badge_count > 0, "Expected match badges to be generated for custom line"

    # Click DateTime badge to select timestamp
    dt_badge = page.locator('.rg-match-badge', has_text="DateTime").first
    if await dt_badge.is_visible():
        await dt_badge.click()
        await page.wait_for_timeout(200)

    # Click Thread name badge
    thr_badge = page.locator('.rg-match-badge', has_text="Thread name").first
    if await thr_badge.is_visible():
        await thr_badge.click()
        await page.wait_for_timeout(200)

    # Click Log level badge
    lvl_badge = page.locator('.rg-match-badge', has_text="Log level").first
    if await lvl_badge.is_visible():
        await lvl_badge.click()
        await page.wait_for_timeout(200)

    # Verify generated regex and group mappings
    rx_val = await page.locator('#e-rx').input_value()
    assert len(rx_val) > 10, f"Expected valid regex in #e-rx, got: {rx_val}"
    assert rx_val.startswith('^'), "Regex should begin with anchor ^"

    # Verify timestamp mapping auto-populated
    ts_map = await page.locator('#cm-ts').input_value()
    assert ts_map == "1", f"Timestamp mapping expected 1, got {ts_map}"

    # Verify thread mapping auto-populated
    th_map = await page.locator('#cm-th').input_value()
    assert th_map == "2", f"Thread mapping expected 2, got {th_map}"

    # Verify level mapping auto-populated
    lv_map = await page.locator('#cm-lv').input_value()
    assert lv_map == "3", f"Level mapping expected 3, got {lv_map}"

    # Verify live preview in Step 1 rendered without error
    rx_pre = page.locator('#rx-pre')
    await expect(rx_pre).to_be_visible()
    await expect(rx_pre).not_to_contain_text("Error:")

    # Save rule
    await page.locator('#btn-ms').click()
    await page.wait_for_timeout(300)

    # Verify modal closed
    await expect(page.locator('#mm')).not_to_be_visible()

    # Verify rule was added to S.cfg.elementRules
    rules = await page.evaluate("() => S.cfg.elementRules")
    assert len(rules) == 1
    assert rules[0]["name"] == "Custom Auth Service"
    assert rules[0]["stackBehavior"] == "push"
    assert rules[0]["captureMapping"]["1"] == "timestamp"
    assert rules[0]["captureMapping"]["2"] == "thread"
    assert rules[0]["captureMapping"]["3"] == "level"

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_rule_test_suite_evaluates_custom_lines(page_with_data):
    """Rule Test Suite button is enabled and tests sample lines against rules without defects."""
    page = page_with_data

    # Ensure a rule set is active
    await page.evaluate("() => { if (!S.cfg || !S.cfg.elementRules?.length) CFG.load(JSON.parse(JSON.stringify(DEF_CFG))); }")

    # Open Settings tab
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(300)

    # Assert Rule Test button is enabled when rules are loaded
    btn_rts = page.locator('#btn-rule-test')
    await expect(btn_rts).to_be_visible()
    await expect(btn_rts).to_be_enabled()

    # Open Rule Test Suite
    await btn_rts.click()
    await page.wait_for_timeout(300)

    rts_modal = page.locator('#rts-mm')
    await expect(rts_modal).to_be_visible()

    # Paste sample lines into RTS textarea
    sample_text = (
        "2026-10-08 14:23:45.123 [main] INFO com.example.App - TX-BEGIN Order 100\n"
        "2026-10-08 14:23:46.456 [main] INFO com.example.App - TX-END Order 100\n"
        "2026-10-08 14:23:47.789 [main] ERROR com.example.App - Database connection timeout"
    )
    await page.locator('#rts-inp').fill(sample_text)

    # Run test
    btn_run = page.locator('#rts-mm button', has_text="Test All Rules")
    await btn_run.click()
    await page.wait_for_timeout(300)

    # Check results container
    out = page.locator('#rts-out')
    await expect(out).to_be_visible()
    out_text = await out.inner_text()
    assert "rules matched" in out_text
    assert "✓" in out_text

    # Close modal
    await page.locator('#rts-mm button[aria-label="Close rule test results"]').click()
    await expect(rts_modal).not_to_be_visible()

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_custom_log_file_parse_journey(blank_page):
    """End-to-end parse journey with custom rule and log line."""
    page = blank_page

    # Dismiss onboarding
    await page.evaluate(DISMISS_ONBOARDING_JS)
    await page.wait_for_timeout(300)

    # Define custom rule
    await page.evaluate("""() => {
        const customRule = {
            id: 'r_custom_op',
            name: 'ProcessOrder',
            regexPattern: '^(\\\\d{4}-\\\\d{2}-\\\\d{2} \\\\d{2}:\\\\d{2}:\\\\d{2}[.,]\\\\d{3})\\\\s+\\\\[([^\\\\]]+)\\\\]\\\\s+(INFO|ERROR)\\\\s+-\\\\s+(.+)$',
            captureMapping: { '1': 'timestamp', '2': 'thread', '3': 'level', '4': 'payload' },
            stackBehavior: 'inline',
            visualStyle: { accentColor: '#38bdf8', icon: '⚡' },
            enabled: true
        };
        CFG.load({
            globalSettings: { appName: 'CustomApp', defaultTimeZone: 'UTC' },
            elementRules: [customRule]
        });
    }""")

    # Parse custom log text
    log_content = (
        "2026-10-08 14:20:00.000 [worker-1] INFO - ProcessOrder starting id=A101\n"
        "2026-10-08 14:20:01.500 [worker-1] INFO - ProcessOrder validated id=A101\n"
        "2026-10-08 14:20:02.000 [worker-2] ERROR - ProcessOrder payment failed id=A102\n"
    )

    await page.evaluate(f"""async () => {{
        const blob = new Blob([`{log_content}`], {{ type: 'text/plain' }});
        const file = new File([blob], 'custom.log', {{ type: 'text/plain' }});
        S.logFile = file;
        const res = await WM.parse(file, S.cfg, '');
        UI.render(res.trees, res.threads, res.stats);
    }}""")

    # Wait for parser to complete
    await page.wait_for_timeout(500)

    # Verify trees exist for threads worker-1 and worker-2
    threads = await page.evaluate("() => Object.keys(S.trees)")
    assert "worker-1" in threads
    assert "worker-2" in threads

    # Verify node contents
    w1_nodes = await page.evaluate("() => S.trees['worker-1']")
    assert len(w1_nodes) == 2
    assert w1_nodes[0]["thread"] == "worker-1"
    assert "ProcessOrder starting" in w1_nodes[0]["payload"]

    w2_nodes = await page.evaluate("() => S.trees['worker-2']")
    assert len(w2_nodes) == 1
    assert w2_nodes[0]["level"] == "ERROR"

    # Switch views to verify rendering without JS errors
    await page.evaluate("() => UI.svm('tree')")
    await page.wait_for_timeout(300)
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(300)

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_unparsed_rescue_flow_for_custom_patterns(blank_page):
    """When custom log lines exceed unparsed threshold, Adaptive Rescue banner appears and launches Custom Regex editor."""
    page = blank_page

    # Dismiss onboarding
    await page.evaluate(DISMISS_ONBOARDING_JS)
    await page.wait_for_timeout(300)

    # Trigger Adaptive Rescue with unparsed sample lines
    await page.evaluate("""() => {
        const stats = {
            linesProcessed: 100,
            matchedLines: 10,
            unparsedSample: [
                "2026-10-08 14:23:45.123 [worker-4] [custom-mod] UNKNOWN_OP payload=foo",
                "2026-10-08 14:23:45.124 [worker-4] [custom-mod] UNKNOWN_OP payload=bar",
                "2026-10-08 14:23:45.125 [worker-4] [custom-mod] UNKNOWN_OP payload=baz"
            ]
        };
        S.stats = stats;
        SNIFFER.checkUnparsedRescue(stats);
    }""")

    await page.wait_for_timeout(300)

    # Verify rescue banner is visible
    banner = page.locator('#rescue-banner')
    await expect(banner).to_be_visible()
    await expect(banner).to_contain_text("Adaptive Rescue")

    # Click "Custom Regex" button
    btn_custom_rx = page.locator('#btn-rescue-custom')
    await expect(btn_custom_rx).to_be_visible()
    await btn_custom_rx.click()
    await page.wait_for_timeout(400)

    # Verify Rule Creator modal opens pre-populated
    modal = page.locator('#mm')
    await expect(modal).to_be_visible()

    tl_val = await page.locator('#e-tl').input_value()
    assert "UNKNOWN_OP" in tl_val

    rx_val = await page.locator('#e-rx').input_value()
    assert len(rx_val) > 5

    # Default name should be pre-populated
    name_val = await page.locator('#e-name').input_value()
    assert len(name_val) > 0

    # Dismiss modal
    await page.locator('#btn-mx').click()
    await expect(modal).not_to_be_visible()

    assert_no_critical_errors(page)
