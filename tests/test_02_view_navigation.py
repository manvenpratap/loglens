"""
test_02_view_navigation.py — LogLens Regression Suite
Tests: Tab view switching, Settings/Help panel visibility, Split view.
Covers Phase 1 (view mode routing via UI.svm).
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_settings_tab_shows_panel(page_with_data):
    """Clicking Settings tab must show #p-cfg with display:flex."""
    page = page_with_data
    await page.click('.vt[data-v="cfg"]')
    await page.wait_for_timeout(400)

    p_cfg = page.locator('#p-cfg')
    await expect(p_cfg).to_be_visible(timeout=3000)
    display = await page.evaluate(
        "() => getComputedStyle(document.getElementById('p-cfg')).display"
    )
    assert display == 'flex', f'#p-cfg display should be flex, got {display}'


@pytest.mark.asyncio
async def test_help_tab_shows_panel(page_with_data):
    """Clicking Help tab must show #p-hlp."""
    page = page_with_data
    await page.click('.vt[data-v="hlp"]')
    await page.wait_for_timeout(400)
    await expect(page.locator('#p-hlp')).to_be_visible(timeout=3000)


@pytest.mark.asyncio
async def test_switching_tabs_hides_previous_panel(page_with_data):
    """Switching from Settings to Help must hide the Settings panel."""
    page = page_with_data
    await page.click('.vt[data-v="cfg"]')
    await page.wait_for_timeout(300)
    await page.click('.vt[data-v="hlp"]')
    await page.wait_for_timeout(300)

    # #p-cfg should be gone or hidden from #res
    cfg_in_res = page.locator('#res #p-cfg')
    if await cfg_in_res.count() > 0:
        assert not await cfg_in_res.is_visible(), '#p-cfg should be hidden when Help is active'


@pytest.mark.asyncio
async def test_split_view_activates_splitter(page_with_data):
    """Split view must render the #sp-hdl drag handle."""
    page = page_with_data
    await page.click('.vt[data-v="split"]')
    await page.wait_for_timeout(400)
    await expect(page.locator('#sp-hdl')).to_be_visible(timeout=3000)


@pytest.mark.asyncio
async def test_gantt_view_active_tab(page_with_data):
    """After switching to gantt, the .vt[data-v=gantt] must have .active class."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(300)
    active = page.locator('.vt.active')
    tab_v = await active.evaluate("el => el.dataset.v")
    assert tab_v == 'gantt', f'Expected active tab gantt, got {tab_v}'


@pytest.mark.asyncio
async def test_no_errors_during_view_transitions(page_with_data):
    """No critical JS errors should occur during rapid view mode changes."""
    page = page_with_data
    for view in ['gantt', 'tree', 'stats', 'cfg', 'hlp', 'gantt']:
        await page.evaluate(f"() => UI.svm('{view}')")
        await page.wait_for_timeout(150)
    assert_no_critical_errors(page)
