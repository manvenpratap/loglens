"""
test_04_command_palette.py — LogLens Regression Suite
Tests: Ctrl+K open, search filtering, Enter navigation, Escape close, recent history.
Covers Phase 5 (Command Palette feature).
Consolidated for high-speed regression verification.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_command_palette_execution_and_recent_history(page_with_data):
    """Command Palette opens on shortcut, filters, navigates on Enter, and records Recent history."""
    page = page_with_data
    palette = page.locator('#cmd-palette')
    assert not await palette.is_visible(), 'Command Palette should be hidden on load'

    # Open palette
    await page.keyboard.press('Control+k')
    await expect(palette).to_be_visible(timeout=3000)

    # Input focused
    focused = await page.evaluate("() => document.activeElement.id === 'cmd-input'")
    assert focused, '#cmd-input should be focused when palette opens'

    # Filter actions
    await page.locator('#cmd-input').fill('stats')
    active_item = page.locator('.cmd-item.cmd-active')
    await expect(active_item).to_be_visible(timeout=2000)
    item_text = await active_item.locator('.cmd-item-name').text_content()
    assert 'Stats' in item_text, f'Expected Stats at top of results, got: {item_text}'

    # Navigate on Enter
    await page.keyboard.press('Enter')
    await expect(palette).not_to_be_visible(timeout=2000)

    active_tab = page.locator('.vt.active')
    tab_v = await active_tab.evaluate("el => el.dataset.v")
    assert tab_v == 'stats', f'Expected stats view, got {tab_v}'

    # Re-open and verify Recent history
    await page.keyboard.press('Control+k')
    await expect(palette).to_be_visible(timeout=2000)
    first = page.locator('.cmd-item').first
    cat = await first.locator('.cmd-item-cat').text_content()
    name = await first.locator('.cmd-item-name').text_content()
    assert 'Recent' in cat and 'Stats' in name, f'Expected Recent → Stats at top, got cat={cat} name={name}'

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_command_palette_dismissal(page_with_data):
    """Escape key cleanly dismisses the Command Palette."""
    page = page_with_data
    palette = page.locator('#cmd-palette')
    await page.keyboard.press('Control+k')
    await expect(palette).to_be_visible(timeout=3000)

    await page.keyboard.press('Escape')
    await expect(palette).not_to_be_visible(timeout=2000)
    assert_no_critical_errors(page)
