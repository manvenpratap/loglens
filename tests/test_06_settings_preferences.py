"""
test_06_settings_preferences.py — LogLens Regression Suite
Tests: App Preferences panel sections (Performance, Appearance) expand/collapse.
Covers Phase 2 (Settings panel) and Phase 6 (Preferences expansion).
"""
import pytest
from playwright.async_api import expect


async def _load_settings(page):
    """Helper: open the Settings tab after demo data is injected."""
    await page.click('.vt[data-v="cfg"]')
    await page.wait_for_timeout(500)


@pytest.mark.asyncio
async def test_settings_panel_visible(page_with_data):
    """#p-cfg must be visible and display:flex after clicking Settings tab."""
    page = page_with_data
    await _load_settings(page)
    await expect(page.locator('#p-cfg')).to_be_visible(timeout=3000)
    display = await page.evaluate(
        "() => getComputedStyle(document.getElementById('p-cfg')).display"
    )
    assert display == 'flex', f'Expected flex, got {display}'


@pytest.mark.asyncio
async def test_preferences_card_visible(page_with_data):
    """App Preferences card #p-gs must be present in the Settings panel."""
    page = page_with_data
    await _load_settings(page)
    await expect(page.locator('#p-gs')).to_be_visible(timeout=3000)


@pytest.mark.asyncio
async def test_performance_section_expands(page_with_data):
    """Clicking Performance section header must reveal the body (display:flex)."""
    page = page_with_data
    await _load_settings(page)

    perf_hdr = page.locator('#ss-perf-hdr')
    await expect(perf_hdr).to_be_visible(timeout=3000)
    await perf_hdr.click()
    await page.wait_for_timeout(400)

    perf_body = page.locator('#ss-perf-body')
    await expect(perf_body).to_be_visible(timeout=3000)
    display = await page.evaluate(
        "() => getComputedStyle(document.getElementById('ss-perf-body')).display"
    )
    assert display == 'flex', f'Performance body should be flex, got {display}'


@pytest.mark.asyncio
async def test_appearance_section_expands(page_with_data):
    """Clicking Appearance section header must reveal the body (display:flex)."""
    page = page_with_data
    await _load_settings(page)

    appear_hdr = page.locator('#ss-appear-hdr')
    await expect(appear_hdr).to_be_visible(timeout=3000)
    await appear_hdr.click()
    await page.wait_for_timeout(400)

    appear_body = page.locator('#ss-appear-body')
    await expect(appear_body).to_be_visible(timeout=3000)
    display = await page.evaluate(
        "() => getComputedStyle(document.getElementById('ss-appear-body')).display"
    )
    assert display == 'flex', f'Appearance body should be flex, got {display}'
