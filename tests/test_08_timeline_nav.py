"""
test_08_timeline_nav.py — LogLens Regression Suite
Tests: Timeline Navigator mini-map panel (mount, chips, zoom presets, ARIA, focus mode integration).
Covers Phase 7 (Timeline Navigator).
Consolidated for high-speed regression verification.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_timeline_nav_mounting_chips_and_presets(page_with_data):
    """Timeline navigator mounts in Gantt view with canvas, interactive ARIA chips, and zoom presets."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")

    # Wrapper and mini-map canvas
    nav_wrap = page.locator('.tl-nav-wrap')
    await expect(nav_wrap).to_be_visible(timeout=5000)
    await expect(page.locator('#tl-nav-canvas')).to_be_attached(timeout=3000)

    # Overlay chips with ARIA role=switch
    chips = page.locator('.tl-overlay-chip')
    assert await chips.count() >= 1
    chip = chips.first
    assert await chip.get_attribute('role') == 'switch'
    assert (await chip.get_attribute('aria-checked')) in ('true', 'false')

    # Toggle chip
    before = await chip.evaluate("el => el.classList.contains('active')")
    await chip.click()
    after = await chip.evaluate("el => el.classList.contains('active')")
    assert before != after, 'Clicking chip should toggle .active class'

    # Zoom presets and Fit button
    assert await page.locator('.tl-zoom-preset').count() >= 4
    await expect(page.locator('.tl-zoom-preset:has-text("Fit")')).to_be_visible(timeout=3000)

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_timeline_nav_focus_mode_integration(page_with_data):
    """Timeline navigator is cleanly hidden when focus mode is active."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await expect(page.locator('.tl-nav-wrap')).to_be_visible(timeout=4000)

    # Activate focus mode
    await page.keyboard.press('f')
    nav = page.locator('.tl-nav-wrap')
    if await nav.count() > 0:
        display = await nav.evaluate("el => getComputedStyle(el).display")
        assert display == 'none', f'.tl-nav-wrap should be hidden in focus mode, got display={display}'

    # Restore
    await page.keyboard.press('f')
    assert_no_critical_errors(page)
