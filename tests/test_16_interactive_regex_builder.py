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
    """Interactive regex builder must parse tokens, accept clicks, show dropdown, add selection badge, and generate regex."""
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
    await page.wait_for_timeout(400)

    # 3. Tokens should be rendered as clickable spans in the interactive line
    interactive_line = page.locator('#rg-interactive-line')
    first_tok = interactive_line.locator('.rg-tok-btn').first
    await expect(first_tok).to_be_visible()
    await expect(first_tok).to_have_text("2026-07-05")

    # 4. Click the first token to open the pattern dropdown
    await first_tok.click()
    await page.wait_for_timeout(300)

    # Dropdown should appear on the body
    dropdown = page.locator('#rg-dropdown')
    await expect(dropdown).to_be_visible()

    # 5. Click the Date pattern option (first pattern option)
    opt = dropdown.locator('.rg-dropdown-item').first
    await opt.click()
    await page.wait_for_timeout(400)

    # Dropdown should be removed
    await expect(dropdown).not_to_be_visible()

    # 6. Active selections container should display a badge
    selections = page.locator('#rg-active-selections')
    await expect(selections).to_contain_text("Date (YYYY-MM-DD):")

    # 7. Regex pattern input e-rx must be populated with a capture group matching the date pattern
    e_rx = page.locator('#e-rx')
    rx_val = await e_rx.input_value()
    assert len(rx_val) > 0
    assert "(\\d{4}-\\d{2}-\\d{2})" in rx_val

    # Ensure no critical console errors occurred during the flow
    assert_no_critical_errors(page)
