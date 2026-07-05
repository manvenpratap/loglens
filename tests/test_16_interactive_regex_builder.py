"""
test_16_interactive_regex_builder.py — LogLens Regression Suite
Tests: Olaf Neumann style interactive regex builder functionality in the Rule Creator modal.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


async def _load_settings_and_open_modal(page):
    """Helper: open the Settings tab and click Add Rule."""
    await page.evaluate("() => { if (S.cfg === null) CFG.load(JSON.parse(JSON.stringify(DEF_CFG))); }")
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(500)
    await page.click('#btn-ar')
    await page.wait_for_timeout(400)


@pytest.mark.asyncio
async def test_interactive_regex_builder_flow(page_with_data):
    """Interactive regex builder must parse tracks, accept selections in input, suggest matches, and auto-populate capture mappings."""
    page = page_with_data
    await _load_settings_and_open_modal(page)

    # 1. Assert visual regex builder UI container is visible
    container = page.locator('#visual-regex-generator-step')
    await expect(container).to_be_visible()

    # 2. Enter a sample log line
    e_tl = page.locator('#e-tl')
    await e_tl.focus()
    await e_tl.fill("2026-07-05 10:00:00 [main] ERROR - connection timeout")
    await page.evaluate("() => document.getElementById('e-tl').dispatchEvent(new Event('input', { bubbles: true }))")
    await page.wait_for_timeout(450)

    # 3. Match badges should be rendered as options in the tracks container
    tracks_container = page.locator('#rg-tracks-container')
    # Use exact text to avoid matching "DateTime" when looking for "Date"
    date_badge = tracks_container.get_by_role('button', name='Date', exact=True)
    await expect(date_badge).to_be_visible()

    # 4. Click the Date option badge to select it
    await date_badge.first.click()
    await page.wait_for_timeout(400)

    # 5. Badge state should turn into selected (checked) — re-query after re-render
    selected_date_badge = tracks_container.get_by_role('button', name='✓ Date', exact=True)
    await expect(selected_date_badge).to_be_visible()

    # 6. Active selections container should display the badge
    selections = page.locator('#rg-active-selections')
    await expect(selections).to_contain_text("Date:")

    # 7. Regex pattern input e-rx must be populated with a capture group matching the date pattern
    e_rx = page.locator('#e-rx')
    rx_val = await e_rx.input_value()
    assert len(rx_val) > 0
    assert "(\\d{4}-\\d{2}-\\d{2})" in rx_val

    # 8. Check auto-population of Timestamp custom mapping
    cm_ts = page.locator('#cm-ts')
    await expect(cm_ts).to_have_value("1")

    # 9. Test selecting an arbitrary range to get suggestions (e.g. select "ERROR" at index 28 to 33)
    # "2026-07-05 10:00:00 [main] ERROR - connection timeout"
    # Index of "ERROR" is 27 to 32.
    await page.evaluate("() => { const el = document.getElementById('e-tl'); el.focus(); el.setSelectionRange(27, 32); el.dispatchEvent(new Event('select')); }")
    await page.wait_for_timeout(400)

    # Suggestions container should become visible
    suggestions_container = page.locator('#rg-selection-suggestions')
    await expect(suggestions_container).to_be_visible()
    await expect(page.locator('#rg-selected-text-preview')).to_have_text("ERROR")

    # Click the Log Levels suggestion button (using .first to avoid strict mode violation on multiple pattern options)
    log_level_sug = page.locator('#rg-suggestions-list button', has_text="Log Levels:").first
    await log_level_sug.click()
    await page.wait_for_timeout(400)

    # Suggestions container should now be hidden
    await expect(suggestions_container).not_to_be_visible()

    # Custom mapping for Log Level (#cm-lv) should be auto-populated to 2 (since ERROR is the second capture group)
    cm_lv = page.locator('#cm-lv')
    await expect(cm_lv).to_have_value("2")

    # Ensure no critical console errors occurred during the flow
    assert_no_critical_errors(page)
