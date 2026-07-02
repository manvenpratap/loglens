"""
test_04_command_palette.py — LogLens Regression Suite
Tests: Ctrl+K open, search filtering, Enter navigation, Escape close, recent history.
Covers Phase 5 (Command Palette feature).
"""
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_command_palette_hidden_initially(page_with_data):
    """Command Palette must be hidden before Ctrl+K is pressed."""
    page = page_with_data
    palette = page.locator('#cmd-palette')
    # Must be hidden
    assert not await palette.is_visible(), 'Command Palette should be hidden on load'


@pytest.mark.asyncio
async def test_command_palette_opens_with_ctrl_k(page_with_data):
    """Ctrl+K must open the Command Palette."""
    page = page_with_data
    await page.keyboard.press('Control+k')
    await page.wait_for_timeout(400)
    await expect(page.locator('#cmd-palette')).to_be_visible(timeout=3000)


@pytest.mark.asyncio
async def test_command_palette_input_focused_on_open(page_with_data):
    """#cmd-input must receive focus when palette opens."""
    page = page_with_data
    await page.keyboard.press('Control+k')
    await page.wait_for_timeout(400)
    focused = await page.evaluate("() => document.activeElement.id === 'cmd-input'")
    assert focused, '#cmd-input should be focused when palette opens'


@pytest.mark.asyncio
async def test_command_palette_search_filters_items(page_with_data):
    """Typing 'stats' must surface the Stats view command at the top."""
    page = page_with_data
    await page.keyboard.press('Control+k')
    await page.wait_for_timeout(300)
    await page.type('#cmd-input', 'stats')
    await page.wait_for_timeout(300)

    active_item = page.locator('.cmd-item.cmd-active')
    item_text = await active_item.locator('.cmd-item-name').text_content()
    assert 'Stats' in item_text, f'Expected Stats at top of results, got: {item_text}'


@pytest.mark.asyncio
async def test_command_palette_enter_navigates_and_closes(page_with_data):
    """Pressing Enter on a filtered result must navigate and close the palette."""
    page = page_with_data
    await page.keyboard.press('Control+k')
    await page.wait_for_timeout(300)
    await page.type('#cmd-input', 'stats')
    await page.wait_for_timeout(300)
    await page.keyboard.press('Enter')
    await page.wait_for_timeout(400)

    # Palette must be closed
    assert not await page.locator('#cmd-palette').is_visible(), \
        'Palette should close after Enter'

    # Active view must be stats
    active_tab = page.locator('.vt.active')
    tab_v = await active_tab.evaluate("el => el.dataset.v")
    assert tab_v == 'stats', f'Expected stats view, got {tab_v}'


@pytest.mark.asyncio
async def test_command_palette_escape_closes(page_with_data):
    """Escape must close the Command Palette."""
    page = page_with_data
    await page.keyboard.press('Control+k')
    await page.wait_for_timeout(300)
    await page.keyboard.press('Escape')
    await page.wait_for_timeout(300)
    assert not await page.locator('#cmd-palette').is_visible(), \
        'Palette should close after Escape'


@pytest.mark.asyncio
async def test_command_palette_recent_history(page_with_data):
    """Executing a command should store it in Recent history."""
    page = page_with_data
    # Execute Stats via palette
    await page.keyboard.press('Control+k')
    await page.wait_for_timeout(300)
    await page.type('#cmd-input', 'stats')
    await page.wait_for_timeout(300)
    await page.keyboard.press('Enter')
    await page.wait_for_timeout(400)

    # Re-open and check recent
    await page.keyboard.press('Control+k')
    await page.wait_for_timeout(300)
    first = page.locator('.cmd-item').first
    cat = await first.locator('.cmd-item-cat').text_content()
    name = await first.locator('.cmd-item-name').text_content()
    assert 'Recent' in cat and 'Stats' in name, \
        f'Expected Recent → Stats at top, got cat={cat} name={name}'
