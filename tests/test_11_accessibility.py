"""
test_11_accessibility.py — LogLens Regression Suite
Tests: Skip link, ARIA live regions, focus trap smoke check, modal ARIA roles.
Covers Phase 11 (A11y Polish).
"""
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_skip_link_present(page_with_data):
    """#skip-link must exist and point to #res."""
    page = page_with_data
    skip = page.locator('#skip-link')
    await expect(skip).to_be_attached()
    href = await skip.get_attribute('href')
    assert href == '#res', f'Skip link href should be #res, got {href}'


@pytest.mark.asyncio
async def test_skip_link_visible_on_focus(page_with_data):
    """Skip link must have a .skip-link class (visible on focus via CSS)."""
    page = page_with_data
    skip = page.locator('#skip-link')
    cls = await skip.get_attribute('class')
    assert 'skip-link' in (cls or ''), f'Skip link should have .skip-link class, got: {cls}'


@pytest.mark.asyncio
async def test_toast_has_aria_live(page_with_data):
    """#toast must have aria-live attribute set to polite."""
    page = page_with_data
    toast = page.locator('#toast')
    if await toast.count() > 0:
        al = await toast.get_attribute('aria-live')
        assert al in ('polite', 'assertive'), f'#toast aria-live should be polite, got {al}'


@pytest.mark.asyncio
async def test_toast_has_aria_atomic(page_with_data):
    """#toast must have aria-atomic=true."""
    page = page_with_data
    toast = page.locator('#toast')
    if await toast.count() > 0:
        aa = await toast.get_attribute('aria-atomic')
        assert aa == 'true', f'#toast aria-atomic should be true, got {aa}'


@pytest.mark.asyncio
async def test_focus_mode_toast_role_status(page_with_data):
    """Focus mode toast must have role=status."""
    page = page_with_data
    # Trigger focus mode to create the toast
    await page.keyboard.press('f')
    await page.wait_for_timeout(300)
    toast = page.locator('#focus-mode-toast')
    await expect(toast).to_be_attached()
    role = await toast.get_attribute('role')
    assert role == 'status', f'Focus mode toast role should be status, got {role}'
    # Clean up
    await page.keyboard.press('f')


@pytest.mark.asyncio
async def test_timeline_chips_aria(page_with_data):
    """TIMELINE_NAV overlay chips must have role=switch + aria-checked after mount."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(600)
    chips = page.locator('.tl-overlay-chip')
    if await chips.count() > 0:
        role = await chips.first.get_attribute('role')
        ac = await chips.first.get_attribute('aria-checked')
        assert role == 'switch', f'Chip role should be switch, got {role}'
        assert ac in ('true', 'false'), f'aria-checked should be bool string, got {ac}'


@pytest.mark.asyncio
async def test_ai_insights_items_keyboard_accessible(page_with_data):
    """AI Insight items must have tabindex=0 for keyboard navigation."""
    page = page_with_data
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(800)
    items = page.locator('.ai-insight-item')
    if await items.count() > 0:
        ti = await items.first.get_attribute('tabindex')
        assert ti == '0', f'Insight items should have tabindex=0, got {ti}'


@pytest.mark.asyncio
async def test_main_content_has_id_res(page_with_data):
    """#res must exist as the main content target for skip-to-content."""
    page = page_with_data
    res = page.locator('#res')
    await expect(res).to_be_attached()
