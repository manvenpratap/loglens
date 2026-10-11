"""
test_06_settings_preferences.py — LogLens Regression Suite
Tests: App Preferences panel sections (Performance, Appearance) expand/collapse.
Covers Phase 2 (Settings panel) and Phase 6 (Preferences expansion).
Consolidated for high-speed regression verification.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_settings_panel_and_preferences_accordions(page_with_data):
    """Settings panel renders as flex container, houses preferences card, and expands Performance/Appearance accordions."""
    page = page_with_data
    await page.click('.vt[data-v="cfg"]')

    # Panel visible and flex
    cfg_panel = page.locator('#p-cfg')
    await expect(cfg_panel).to_be_visible(timeout=3000)
    display = await page.evaluate("() => getComputedStyle(document.getElementById('p-cfg')).display")
    assert display == 'flex', f'Expected flex, got {display}'

    # Preferences card visible
    await expect(page.locator('#p-gs')).to_be_visible(timeout=3000)

    # Performance accordion expansion
    perf_hdr = page.locator('#ss-perf-hdr')
    await expect(perf_hdr).to_be_visible(timeout=3000)
    await perf_hdr.click()
    perf_body = page.locator('#ss-perf-body')
    await expect(perf_body).to_be_visible(timeout=3000)
    perf_disp = await page.evaluate("() => getComputedStyle(document.getElementById('ss-perf-body')).display")
    assert perf_disp == 'flex', f'Performance body should be flex, got {perf_disp}'

    # Appearance accordion expansion
    appear_hdr = page.locator('#ss-appear-hdr')
    await expect(appear_hdr).to_be_visible(timeout=3000)
    await appear_hdr.click()
    appear_body = page.locator('#ss-appear-body')
    await expect(appear_body).to_be_visible(timeout=3000)
    appear_disp = await page.evaluate("() => getComputedStyle(document.getElementById('ss-appear-body')).display")
    assert appear_disp == 'flex', f'Appearance body should be flex, got {appear_disp}'

    assert_no_critical_errors(page)
