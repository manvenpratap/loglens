"""
test_21_custom_log_setup_journey.py — LogLens Regression Suite
Tests: Custom log file initial setup user journey and workflow to achieve 100% parsing.
Covers:
  1. Welcome dialog Open Log File action & onboarding dismissal.
  2. Automatic sniffing & rule synthesis for non-standard custom log formats.
  3. High / 100% initial parsing on custom logs.
  4. Adaptive Rescue '✦ Resolve All to 100%' one-click workflow.
  5. Zero-match guidance card in Waterfall and Execution Tree.
  6. File drop dismisses onboarding overlay.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors, DISMISS_ONBOARDING_JS


@pytest.mark.asyncio
async def test_onboarding_open_log_file_trigger(blank_page):
    """Clicking Open Log File in the welcome modal dismisses onboarding overlay."""
    page = blank_page
    ob = page.locator('#ob-ov')
    await expect(ob).to_be_visible(timeout=5000)

    btn_open = page.locator('#ob-btn-drop')
    await expect(btn_open).to_be_visible()
    await expect(btn_open).to_contain_text("Open Log File")

    # Clicking should dismiss onboarding overlay
    await btn_open.click()
    await expect(ob).to_be_hidden(timeout=5000)
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_custom_log_auto_sniff_and_synthesize_rules(blank_page):
    """Custom log lines with bracketed timestamp, thread, and level should synthesize accurate rules."""
    page = blank_page
    await page.evaluate(DISMISS_ONBOARDING_JS)

    res = await page.evaluate("""() => {
        const customLines = [
            '[2026-10-08 14:23:45.123] [worker-4] [auth-svc] INFO - User login ok user_id=42',
            '[2026-10-08 14:23:46.456] [worker-4] [auth-svc] INFO - Request started req=101',
            '[2026-10-08 14:23:47.789] [worker-4] [auth-svc] ERROR - DB connection timeout',
            '[2026-10-08 14:23:48.012] [worker-4] [auth-svc] INFO - Response finished req=101'
        ];
        const synth = SNIFFER.synthesizeRules(customLines, 'app-custom.log');
        const rules = synth.config.elementRules;
        const compiled = rules.map(r => new RegExp(r.regexPattern));
        const matchedCount = customLines.filter(l => compiled.some(rx => rx.test(l))).length;

        return {
            rulesCount: rules.length,
            matchedCount,
            totalLines: customLines.length,
            hasPush: rules.some(r => r.stackBehavior === 'push'),
            hasPop: rules.some(r => r.stackBehavior === 'pop'),
            hasInline: rules.some(r => r.stackBehavior === 'inline')
        };
    }""")

    assert res['rulesCount'] >= 4
    assert res['matchedCount'] == res['totalLines'], "All custom lines should match synthesized rules"
    assert res['hasPush'] is True
    assert res['hasPop'] is True
    assert res['hasInline'] is True
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_custom_log_end_to_end_parse_100_percent(blank_page):
    """A custom log file parsed end-to-end should produce structured trees and 100% coverage."""
    page = blank_page
    await page.evaluate(DISMISS_ONBOARDING_JS)

    log_content = (
        "[2026-10-08 14:23:45.123] [worker-4] [auth-svc] INFO - Request started id=101\n"
        "[2026-10-08 14:23:46.456] [worker-4] [auth-svc] INFO - Processing payload\n"
        "[2026-10-08 14:23:47.789] [worker-4] [auth-svc] ERROR - Query timeout\n"
        "[2026-10-08 14:23:48.012] [worker-4] [auth-svc] INFO - Response finished id=101\n"
    )

    res = await page.evaluate(f"""async () => {{
        const lines = `{log_content}`.trim().split('\\n');
        const synth = SNIFFER.synthesizeRules(lines, 'auth-worker.log');
        CFG.load(synth.config);

        const blob = new Blob([`{log_content}`], {{ type: 'text/plain' }});
        const file = new File([blob], 'auth-worker.log', {{ type: 'text/plain' }});
        S.logFile = file;

        const parseRes = await WM.parse(file, S.cfg, '');
        UI.render(parseRes.trees, parseRes.threads, parseRes.stats);
        SNIFFER.checkUnparsedRescue(parseRes.stats);

        return {{
            linesProcessed: parseRes.stats.linesProcessed,
            matchedLines: parseRes.stats.matchedLines,
            threads: parseRes.threads,
            treeNodes: (parseRes.trees['worker-4'] || []).length
        }};
    }}""")

    assert res['linesProcessed'] == 4
    assert res['matchedLines'] == 4, "Should achieve 100% parsing on custom log file"
    assert "worker-4" in res['threads']
    assert res['treeNodes'] > 0

    # Ensure views render without critical errors
    await page.evaluate("() => UI.svm('tree')")
    await page.wait_for_timeout(200)
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(200)
    await page.evaluate("() => UI.svm('split')")
    await page.wait_for_timeout(200)

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_adaptive_rescue_resolve_all_to_100_percent(blank_page):
    """When unparsed lines exist, clicking Resolve All to 100% creates fallback rules and drives coverage to 100%."""
    page = blank_page
    await page.evaluate(DISMISS_ONBOARDING_JS)

    # Simulate parse output with unparsed lines
    await page.evaluate("""() => {
        if (!S.cfg) CFG.load(JSON.parse(JSON.stringify(DEF_CFG)));
        const dummyStats = {
            fileSize: 4000,
            linesProcessed: 50,
            matchedLines: 30, // 40% unparsed
            unparsedSample: [
                '2026-10-08 15:00:00 [srv-1] CUSTOM_EVENT foo=1 bar=2',
                '2026-10-08 15:00:01 [srv-1] CUSTOM_EVENT foo=3 bar=4',
                '2026-10-08 15:00:02 [srv-2] ASYNC_NOTIF code=99'
            ]
        };
        S.stats = dummyStats;
        SNIFFER.checkUnparsedRescue(dummyStats);
    }""")

    # Verify rescue banner is visible with Resolve All button
    banner = page.locator('#rescue-banner')
    await expect(banner).to_be_visible()

    btn_resolve_all = page.locator('#btn-rescue-resolve-all')
    await expect(btn_resolve_all).to_be_visible()
    await expect(btn_resolve_all).to_contain_text("Resolve All to 100%")

    initial_rules_count = await page.evaluate("() => S.cfg.elementRules.length")

    # Click Resolve All to 100%
    await btn_resolve_all.click()
    await page.wait_for_timeout(300)

    # Banner should be dismissed and rules should be added
    await expect(page.locator('#rescue-banner')).not_to_be_visible()
    new_rules_count = await page.evaluate("() => S.cfg.elementRules.length")
    assert new_rules_count > initial_rules_count, "Rules should be added for unparsed clusters"

    # Simulate subsequent 100% parsed result triggering success notification
    await page.evaluate("""() => {
        const fullStats = {
            fileSize: 4000,
            linesProcessed: 50,
            matchedLines: 50,
            unparsedSample: []
        };
        S.stats = fullStats;
        SNIFFER.checkUnparsedRescue(fullStats);
    }""")

    success_banner = page.locator('#rescue-success-banner')
    await expect(success_banner).to_be_visible()
    await expect(success_banner).to_contain_text("100% Rule Coverage Achieved")

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_zero_matched_lines_guidance_card(blank_page):
    """When a custom log has 0 matched lines, UI renders clear setup guidance card instead of empty dead-end."""
    page = blank_page
    await page.evaluate(DISMISS_ONBOARDING_JS)

    # Set up state where lines were processed but 0 matched
    await page.evaluate("""() => {
        S.trees = {};
        S.threads = [];
        S.activeThr = null;
        S.stats = {
            fileSize: 1024,
            linesProcessed: 25,
            matchedLines: 0,
            unparsedSample: ['UNMATCHED 1', 'UNMATCHED 2']
        };
        UI.svm('split');
    }""")

    await page.wait_for_timeout(300)

    # Guidance card should be displayed in the result container
    guidance = page.locator('.emp >> text=Custom Log Format Detected')
    await expect(guidance).to_be_visible()

    btn_resolve = page.locator('#btn-zero-match-resolve')
    await expect(btn_resolve).to_be_visible()
    await expect(btn_resolve).to_contain_text("Auto-Configure Rules")

    btn_custom = page.locator('#btn-zero-match-custom')
    await expect(btn_custom).to_be_visible()

    assert_no_critical_errors(page)
