"""
test_22_two_tier_navigation.py — LogLens Regression Suite
Tests: 2-Tier Navigation Architecture:
- Core Forensic Views (Split, Timeline, Tree, Traces) with hotkey badges (⌥1..⌥4)
- Analysis Dropdown ([ Analysis ▾ ]) housing Stats, Graph, Query, 3D, Diff
- macOS Toolbar Utility icon buttons (Settings ⚙, Help ?) on the right side of the header
- Keyboard shortcut mappings (Alt+1..4)
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_core_forensic_pills_and_hotkeys(page_with_data):
    """Core forensic views group must contain Split, Timeline, Tree, Traces with ⌥1..⌥4 hotkeys."""
    page = page_with_data

    core_group = page.locator('.vt-core-group')
    await expect(core_group).to_be_visible()

    # Split
    split_pill = page.locator('.vt-core-group .vt[data-v="split"]')
    await expect(split_pill).to_be_visible()
    await expect(split_pill.locator('.vt-hotkey')).to_have_text('⌥1')

    # Timeline (gantt)
    timeline_pill = page.locator('.vt-core-group .vt[data-v="gantt"]')
    await expect(timeline_pill).to_be_visible()
    await expect(timeline_pill.locator('.vt-hotkey')).to_have_text('⌥2')

    # Tree
    tree_pill = page.locator('.vt-core-group .vt[data-v="tree"]')
    await expect(tree_pill).to_be_visible()
    await expect(tree_pill.locator('.vt-hotkey')).to_have_text('⌥3')

    # Traces
    traces_pill = page.locator('.vt-core-group .vt[data-v="trace"]')
    await expect(traces_pill).to_be_visible()
    await expect(traces_pill.locator('.vt-hotkey')).to_have_text('⌥4')

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_analysis_dropdown_toggle_and_items(page_with_data):
    """Analysis dropdown button must toggle menu housing Stats, Graph, Query, 3D, Diff."""
    page = page_with_data

    dropdown_btn = page.locator('#btn-analysis')
    await expect(dropdown_btn).to_be_visible()

    menu = page.locator('#analysis-menu')
    # Initially closed
    assert not await menu.is_visible()

    # Click to open
    await dropdown_btn.click()
    await expect(menu).to_be_visible()

    # Verify menu items exist
    stats_item = menu.locator('.vt[data-v="stats"]')
    graph_item = menu.locator('.vt[data-v="graph"]')
    query_item = menu.locator('.vt[data-v="query"]')
    three_d_item = menu.locator('.vt[data-v="3d"]')

    await expect(stats_item).to_be_visible()
    await expect(graph_item).to_be_visible()
    await expect(query_item).to_be_visible()
    await expect(three_d_item).to_be_visible()

    # Selecting Stats switches view and updates dropdown state
    await stats_item.click()
    await page.wait_for_timeout(300)

    # Menu closes on selection
    assert not await menu.is_visible()

    # Active view is stats
    active_tab = page.locator('.vt.active')
    tab_v = await active_tab.evaluate("el => el.dataset.v")
    assert tab_v == 'stats', f'Expected active view stats, got {tab_v}'

    # Button indicates active analysis mode
    has_active = await dropdown_btn.evaluate("el => el.classList.contains('has-active')")
    assert has_active, 'Expected #btn-analysis to have has-active class'

    btn_text = await dropdown_btn.locator('.analysis-btn-text').text_content()
    assert 'Stats' in btn_text, f'Expected Stats in button text, got {btn_text}'

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_macos_toolbar_utility_icons(page_with_data):
    """Settings (⚙) and Help (?) must be compact toolbar icon buttons in header utility group."""
    page = page_with_data

    util_group = page.locator('.hdr-util-group')
    await expect(util_group).to_be_visible()

    cfg_btn = page.locator('#btn-hdr-cfg')
    hlp_btn = page.locator('#btn-hdr-hlp')

    await expect(cfg_btn).to_be_visible()
    await expect(hlp_btn).to_be_visible()

    # Check compact dimensions (approx 28px)
    cfg_box = await cfg_btn.bounding_box()
    assert cfg_box is not None
    assert 24 <= cfg_box['width'] <= 34, f'Expected ~28px width, got {cfg_box["width"]}'
    assert 24 <= cfg_box['height'] <= 34, f'Expected ~28px height, got {cfg_box["height"]}'

    # Clicking Settings opens #p-cfg
    await cfg_btn.click()
    await page.wait_for_timeout(300)
    await expect(page.locator('#p-cfg')).to_be_visible()

    # Clicking Help opens #p-hlp
    await hlp_btn.click()
    await page.wait_for_timeout(300)
    await expect(page.locator('#p-hlp')).to_be_visible()

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_keyboard_shortcuts_alt_1_to_4(page_with_data):
    """Alt+1..4 keyboard shortcuts must cleanly switch between core forensic views."""
    page = page_with_data

    # Alt+1 -> Split
    await page.keyboard.press('Alt+1')
    await page.wait_for_timeout(200)
    mode = await page.evaluate("() => S.viewMode")
    assert mode == 'split', f'Expected split mode on Alt+1, got {mode}'

    # Alt+2 -> Timeline (gantt)
    await page.keyboard.press('Alt+2')
    await page.wait_for_timeout(200)
    mode = await page.evaluate("() => S.viewMode")
    assert mode == 'gantt', f'Expected gantt mode on Alt+2, got {mode}'

    # Alt+3 -> Tree
    await page.keyboard.press('Alt+3')
    await page.wait_for_timeout(200)
    mode = await page.evaluate("() => S.viewMode")
    assert mode == 'tree', f'Expected tree mode on Alt+3, got {mode}'

    # Alt+4 -> Traces
    await page.keyboard.press('Alt+4')
    await page.wait_for_timeout(200)
    mode = await page.evaluate("() => S.viewMode")
    assert mode == 'trace', f'Expected trace mode on Alt+4, got {mode}'

    assert_no_critical_errors(page)
