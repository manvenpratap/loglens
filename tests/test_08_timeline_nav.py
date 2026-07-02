"""
test_08_timeline_nav.py — LogLens Regression Suite
Tests: Timeline Navigator mini-map panel (mount, chips, zoom presets, ARIA).
Covers Phase 7 (Timeline Navigator).
"""
import pytest
from playwright.async_api import expect
from conftest import DEMO_TREES_JS


@pytest.mark.asyncio
async def test_timeline_nav_mounts_in_gantt(page_with_data):
    """Timeline navigator wrap (.tl-nav-wrap) must be visible in Gantt view."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(500)
    await expect(page.locator('.tl-nav-wrap')).to_be_visible(timeout=5000)


@pytest.mark.asyncio
async def test_timeline_nav_canvas_present(page_with_data):
    """The mini-map canvas (#tl-nav-canvas) must be in the DOM."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(500)
    await expect(page.locator('#tl-nav-canvas')).to_be_attached(timeout=5000)


@pytest.mark.asyncio
async def test_timeline_nav_overlay_chips_present(page_with_data):
    """At least 1 .tl-overlay-chip must be rendered."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(500)
    count = await page.locator('.tl-overlay-chip').count()
    assert count >= 1, f'Expected at least 1 overlay chip, got {count}'


@pytest.mark.asyncio
async def test_timeline_nav_chip_aria_attributes(page_with_data):
    """Overlay chips must have role=switch and aria-checked."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(500)
    chip = page.locator('.tl-overlay-chip').first
    role = await chip.get_attribute('role')
    aria_checked = await chip.get_attribute('aria-checked')
    assert role == 'switch', f'Chip role should be switch, got {role}'
    assert aria_checked in ('true', 'false'), f'aria-checked should be true/false, got {aria_checked}'


@pytest.mark.asyncio
async def test_timeline_nav_chip_toggles_active_class(page_with_data):
    """Clicking an overlay chip must toggle its .active class."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(500)
    chip = page.locator('.tl-overlay-chip').first
    before = await chip.evaluate("el => el.classList.contains('active')")
    await chip.click()
    await page.wait_for_timeout(200)
    after = await chip.evaluate("el => el.classList.contains('active')")
    assert before != after, 'Clicking chip should toggle .active class'


@pytest.mark.asyncio
async def test_timeline_nav_zoom_presets_present(page_with_data):
    """At least 4 .tl-zoom-preset preset buttons must be present."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(500)
    count = await page.locator('.tl-zoom-preset').count()
    assert count >= 4, f'Expected at least 4 zoom buttons, got {count}'


@pytest.mark.asyncio
async def test_timeline_nav_fit_button_present(page_with_data):
    """A 'Fit' zoom button must be present."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(500)
    fit_btn = page.locator('.tl-zoom-preset:has-text("Fit")')
    await expect(fit_btn).to_be_visible(timeout=3000)


@pytest.mark.asyncio
async def test_timeline_nav_hidden_in_focus_mode(page_with_data):
    """Timeline navigator must be hidden when body.focus-mode is active."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(400)
    # Activate focus mode
    await page.keyboard.press('f')
    await page.wait_for_timeout(300)
    nav = page.locator('.tl-nav-wrap')
    if await nav.count() > 0:
        display = await nav.evaluate("el => getComputedStyle(el).display")
        assert display == 'none', f'.tl-nav-wrap should be hidden in focus mode, got display={display}'
    # Restore
    await page.keyboard.press('f')
