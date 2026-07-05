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
