"""
test_10_focus_mode.py — LogLens Regression Suite
Tests: F-key toggle, body class, sidebar hidden, toast, sessionStorage, deactivation.
Covers Phase 9 (FOCUS_MODE).
"""
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_focus_mode_inactive_on_load(page_with_data):
    """body.focus-mode must NOT be active on page load."""
    page = page_with_data
    has_fm = await page.evaluate("() => document.body.classList.contains('focus-mode')")
    assert not has_fm, 'focus-mode should not be active on load'


@pytest.mark.asyncio
async def test_focus_mode_activates_via_f_key(page_with_data):
    """Pressing F must add .focus-mode to body."""
    page = page_with_data
    await page.keyboard.press('f')
    await page.wait_for_timeout(300)
    has_fm = await page.evaluate("() => document.body.classList.contains('focus-mode')")
    assert has_fm, 'body should have .focus-mode after pressing F'


@pytest.mark.asyncio
async def test_focus_mode_shows_toast(page_with_data):
    """Pressing F must show the focus-mode toast with 'Focus Mode ON' text."""
    page = page_with_data
    await page.keyboard.press('f')
    await page.wait_for_timeout(300)
    toast = page.locator('#focus-mode-toast')
    await expect(toast).to_be_visible(timeout=2000)
    text = await toast.inner_text()
    assert 'Focus Mode ON' in text, f'Toast should say Focus Mode ON, got: {text}'


@pytest.mark.asyncio
async def test_focus_mode_hides_sidebar(page_with_data):
    """Sidebar (.sb) must be display:none while focus-mode is active."""
    page = page_with_data
    await page.keyboard.press('f')
    await page.wait_for_timeout(300)
    sidebar = page.locator('.sb')
    if await sidebar.count() > 0:
        display = await sidebar.evaluate("el => getComputedStyle(el).display")
        assert display == 'none', f'Sidebar should be none in focus mode, got {display}'


@pytest.mark.asyncio
async def test_focus_mode_deactivates_on_second_f(page_with_data):
    """Pressing F twice must deactivate focus-mode."""
    page = page_with_data
    await page.keyboard.press('f')
    await page.wait_for_timeout(200)
    await page.keyboard.press('f')
    await page.wait_for_timeout(300)
    has_fm = await page.evaluate("() => document.body.classList.contains('focus-mode')")
    assert not has_fm, 'focus-mode should deactivate on second F press'


@pytest.mark.asyncio
async def test_focus_mode_exit_toast(page_with_data):
    """Exiting focus mode must show 'Focus Mode OFF' toast."""
    page = page_with_data
    await page.keyboard.press('f')
    await page.wait_for_timeout(200)
    await page.keyboard.press('f')
    await page.wait_for_timeout(300)
    toast = page.locator('#focus-mode-toast')
    text = await toast.inner_text()
    assert 'Focus Mode OFF' in text, f'Exit toast should say Focus Mode OFF, got: {text}'


@pytest.mark.asyncio
async def test_focus_mode_session_storage(page_with_data):
    """sessionStorage must track focus mode state."""
    page = page_with_data
    await page.keyboard.press('f')
    await page.wait_for_timeout(200)
    on_val = await page.evaluate("() => sessionStorage.getItem('ll_focus_mode')")
    assert on_val == '1', f'sessionStorage should be 1 when active, got: {on_val}'

    await page.keyboard.press('f')
    await page.wait_for_timeout(200)
    off_val = await page.evaluate("() => sessionStorage.getItem('ll_focus_mode')")
    assert off_val == '0', f'sessionStorage should be 0 when inactive, got: {off_val}'


@pytest.mark.asyncio
async def test_focus_mode_toast_has_role_status(page_with_data):
    """Focus mode toast must have role=status for accessibility."""
    page = page_with_data
    await page.keyboard.press('f')
    await page.wait_for_timeout(300)
    toast = page.locator('#focus-mode-toast')
    role = await toast.get_attribute('role')
    assert role == 'status', f'Focus mode toast should have role=status, got: {role}'


@pytest.mark.asyncio
async def test_focus_mode_not_triggered_in_input(page_with_data):
    """F key must NOT activate focus mode when typed into an input field."""
    page = page_with_data
    await page.focus('#hdr-search')
    await page.wait_for_timeout(100)
    await page.keyboard.type('f')
    await page.wait_for_timeout(200)
    has_fm = await page.evaluate("() => document.body.classList.contains('focus-mode')")
    assert not has_fm, 'focus-mode should NOT activate when F typed in input'
