"""
test_10_focus_mode.py — LogLens Regression Suite
Tests: F-key toggle, body class, sidebar hidden, toast, sessionStorage, deactivation, input isolation.
Covers Phase 9 (FOCUS_MODE).
Consolidated for high-speed regression verification.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_focus_mode_toggle_cycle_and_storage(page_with_data):
    """F-key toggle cycle activates focus mode, updates DOM/storage, and deactivates cleanly on second press."""
    page = page_with_data

    # 1. Inactive on load
    has_fm = await page.evaluate("() => document.body.classList.contains('focus-mode')")
    assert not has_fm, 'focus-mode should not be active on load'

    # 2. Press F to activate
    await page.keyboard.press('f')
    await page.wait_for_timeout(300)
    assert await page.evaluate("() => document.body.classList.contains('focus-mode')")

    # Toast validation
    toast = page.locator('#focus-mode-toast')
    await expect(toast).to_be_visible(timeout=2000)
    assert 'Focus Mode ON' in (await toast.inner_text())
    assert await toast.get_attribute('role') == 'status'

    # Sidebar hidden
    sidebar = page.locator('.sb')
    if await sidebar.count() > 0:
        display = await sidebar.evaluate("el => getComputedStyle(el).display")
        assert display == 'none', f'Sidebar should be none in focus mode, got {display}'

    # sessionStorage tracking
    assert await page.evaluate("() => sessionStorage.getItem('ll_focus_mode')") == '1'

    # 3. Press F second time to deactivate
    await page.keyboard.press('f')
    await page.wait_for_function("() => !document.body.classList.contains('focus-mode')")
    assert 'Focus Mode OFF' in (await toast.inner_text())
    assert await page.evaluate("() => sessionStorage.getItem('ll_focus_mode')") == '0'

    assert_no_critical_errors(page)


import re
re_pattern = re.compile(r'focus-mode')


@pytest.mark.asyncio
async def test_focus_mode_input_isolation(page_with_data):
    """F key must NOT activate focus mode when typed into an input field."""
    page = page_with_data
    await page.focus('#hdr-search')
    await page.keyboard.type('f')
    await page.wait_for_timeout(100)

    has_fm = await page.evaluate("() => document.body.classList.contains('focus-mode')")
    assert not has_fm, 'Typing F into search input should not trigger focus mode'
    assert_no_critical_errors(page)
