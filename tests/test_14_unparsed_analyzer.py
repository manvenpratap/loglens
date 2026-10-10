"""
test_14_unparsed_analyzer.py — LogLens Regression Suite
Tests: Unparsed Analyzer view, parsing suggestion rules, and + Create Rule integration.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


async def _load_settings_with_unparsed_data(page):
    """Helper: open the Settings tab and inject unparsed log samples."""
    await page.evaluate("() => { if (S.cfg === null) CFG.load(JSON.parse(JSON.stringify(DEF_CFG))); }")
    await page.evaluate("""() => {
        S.stats = {
            fileSize: 5000,
            linesProcessed: 10,
            matchedLines: 7,
            unparsedSample: [
                "2026-07-05 10:00:00 [main] ERROR - Database connection timeout",
                "2026-07-05 10:00:01 [main] ERROR - Database connection timeout",
                "2026-07-05 10:00:02 [main] ERROR - Database connection timeout"
            ]
        };
        stats = S.stats;
    }""")
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(500)


@pytest.mark.asyncio
async def test_unparsed_analyzer_create_rule_button(page_with_data):
    """Clicking + Create Rule on unparsed analyzer must populate the rule creator modal correctly."""
    page = page_with_data
    await _load_settings_with_unparsed_data(page)

    # 1. Click "Analyze Unparsed"
    btn_analyze = page.locator('#btn-analyze-unparsed')
    await expect(btn_analyze).to_be_visible()
    await btn_analyze.click()
    await page.wait_for_timeout(500)

    # 2. Check that pattern list is populated
    results = page.locator('#unparsed-results')
    await expect(results).to_contain_text("Top Unparsed Patterns:")
    
    # 3. Locate the "+ Create Rule" button
    btn_create_rule = page.locator('#unparsed-results >> text=+ Create Rule').first
    await expect(btn_create_rule).to_be_visible()

    # 4. Click "+ Create Rule"
    await btn_create_rule.click()
    await page.wait_for_timeout(500)

    # 5. Rule modal must be visible
    modal = page.locator('#mm')
    await expect(modal).not_to_have_class(r"hidden")

    # 6. Advanced option must be checked and e-rx value populated
    use_custom = page.locator('#e-use-custom-rx')
    await expect(use_custom).to_be_checked()

    e_rx = page.locator('#e-rx')
    rx_val = await e_rx.input_value()
    assert len(rx_val) > 0
    assert "^" in rx_val

    # 7. Sample log line (e-tl) must be pre-populated
    e_tl = page.locator('#e-tl')
    tl_val = await e_tl.input_value()
    assert tl_val == "2026-07-05 10:00:00 [main] ERROR - Database connection timeout"

    # Ensure no critical console errors occurred during the flow
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_unparsed_analyzer_100_percent_coverage(page_with_data):
    """When a log has 100% rule coverage (0 unparsed lines), Analyzer displays success rather than false error."""
    page = page_with_data
    # Set up 100% matched state with empty unparsedSample
    await page.evaluate("""() => {
        S.stats = {
            fileSize: 5000,
            linesProcessed: 35,
            matchedLines: 35,
            unparsedSample: []
        };
        UI.svm('cfg');
    }""")
    await page.wait_for_timeout(300)

    btn_analyze = page.locator('#btn-analyze-unparsed')
    await expect(btn_analyze).to_be_visible()
    await btn_analyze.click()
    await page.wait_for_timeout(300)

    results = page.locator('#unparsed-results')
    # Must celebrate 100% coverage and NOT display the error "No unparsed lines to analyze. Parse a log file first."
    await expect(results).to_contain_text("100% rule coverage")
    await expect(results).to_contain_text("Zero unparsed lines detected")
    results_text = await results.inner_text()
    assert "No unparsed lines to analyze. Parse a log file first." not in results_text

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_unparsed_analyzer_when_no_log_parsed(blank_page):
    """When no log file has been parsed yet, Analyzer shows actionable guidance instead of a dead error."""
    page = blank_page
    await page.evaluate("() => { if (typeof ONBOARD !== 'undefined') ONBOARD.dismiss(); UI.svm('cfg'); }")
    await page.wait_for_timeout(300)

    btn_analyze = page.locator('#btn-analyze-unparsed')
    await expect(btn_analyze).to_be_visible()
    await btn_analyze.click()
    await page.wait_for_timeout(300)

    results = page.locator('#unparsed-results')
    await expect(results).to_contain_text("No log file parsed yet")
    await expect(results.locator('button >> text=Select Log File')).to_be_visible()
    await expect(results.locator('button >> text=Load Demo Log')).to_be_visible()

    assert_no_critical_errors(page)

