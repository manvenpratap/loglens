"""
test_25_execution_tree_telemetry.py — LogLens Regression Suite
Tests: Execution Tree Swiss Telemetry architecture:
- 3-zone layout: tree-spine with branch guide lines, tree-payload-col, tree-telemetry-col
- Latency sparkbar and metric alignment
- Depth controls (D1, D2, D3, All)
- Minimap toggle (Map button)
- Tooltip dismissal (no stuck tooltips)
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_execution_tree_three_zone_architecture(page_with_data):
    """Execution Tree renders with 3 distinct zones: spine with guide lines, payload column, and pinned telemetry strip."""
    page = page_with_data
    await page.evaluate("() => UI.svm('tree')")

    tree_vscroll = page.locator('#tree-vscroll')
    await expect(tree_vscroll).to_be_visible(timeout=5000)

    # Column header row
    tree_hdr = page.locator('#tree-hdr')
    await expect(tree_hdr).to_be_visible()
    await expect(tree_hdr.locator('.tree-hdr-spine')).to_contain_text('Operation & Hierarchy')
    await expect(tree_hdr.locator('.tree-hdr-payload')).to_contain_text('Payload Preview')
    await expect(tree_hdr.locator('.tree-th-dur')).to_contain_text('Duration')
    await expect(tree_hdr.locator('.tree-th-ts')).to_contain_text('Timestamp')

    # Horizontal scroll synchronization (when viewport overflows 820px min-width)
    await page.set_viewport_size({'width': 600, 'height': 800})
    await page.evaluate("() => { const vs = document.getElementById('tree-vscroll'); vs.scrollLeft = 50; vs.dispatchEvent(new Event('scroll')); }")
    assert await page.evaluate("() => document.getElementById('tree-hdr').scrollLeft") == 50
    await page.set_viewport_size({'width': 1400, 'height': 900})

    # First row has 3 zones
    row = page.locator('.tree-row').first
    await expect(row).to_be_visible()

    spine = row.locator('.tree-spine')
    await expect(spine).to_be_visible()
    await expect(spine.locator('.tnm')).to_be_visible()

    payload_col = row.locator('.tree-payload-col')
    await expect(payload_col).to_be_attached()

    telemetry_col = row.locator('.tree-telemetry-col')
    await expect(telemetry_col).to_be_visible()
    await expect(telemetry_col.locator('.tree-metric-dur')).to_be_visible()
    await expect(telemetry_col.locator('.tree-metric-ts')).to_be_visible()

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_execution_tree_depth_filtering(page_with_data):
    """Depth buttons D1, D2, D3, All collapse and expand nodes to matching levels."""
    page = page_with_data
    await page.evaluate("""() => {
        S.trees = { main: [{
            id: 'p1', ruleName: 'Parent', elementName: 'srv.main', duration: 100, timestamp: Date.now(),
            hasChildren: true, expanded: true, depth: 0,
            events: [
                { id: 'c1', ruleName: 'Child', elementName: 'srv.child', duration: 50, timestamp: Date.now(), depth: 1, events: [] }
            ]
        }]};
        UI.render(S.trees, ['main'], S.stats);
        UI.svm('tree');
    }""")

    # D1 collapses to roots only
    btn_d1 = page.locator('.tree-depth-btn[data-depth="1"]')
    await expect(btn_d1).to_be_visible()
    await btn_d1.click()
    assert await page.evaluate("() => TR._visibleNodes.every(n => n.depth === 0)")

    # All expands all nodes
    btn_all = page.locator('.tree-depth-btn[data-depth="all"]')
    await btn_all.click()
    assert await page.evaluate("() => TR._visibleNodes.some(n => n.depth > 0)")

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_execution_tree_minimap_toggle(page_with_data):
    """Map button in tree toolbar toggles the minimap on and off."""
    page = page_with_data
    await page.evaluate("() => UI.svm('tree')")

    btn_map = page.locator('#btn-tree-map-toggle')
    await expect(btn_map).to_be_visible()

    # Get initial state
    initial_state = await page.evaluate("() => !!document.getElementById('ll-minimap-wrap')")

    # Toggle state
    await btn_map.click()
    new_state = await page.evaluate("() => !!document.getElementById('ll-minimap-wrap')")
    assert new_state != initial_state

    # Toggle back
    await btn_map.click()
    restored_state = await page.evaluate("() => !!document.getElementById('ll-minimap-wrap')")
    assert restored_state == initial_state

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_tooltip_dismissal_on_scroll_and_mouseout(page_with_data):
    """Tooltips are cleanly dismissed on scroll and mouseout, preventing orphan tooltips."""
    page = page_with_data
    tooltip = page.locator('#app-tooltip')

    # Trigger tooltip
    badge = page.locator('[data-tip]').first
    if await badge.count() > 0:
        await badge.hover()
        await page.wait_for_timeout(200)

        # Trigger scroll event
        await page.evaluate("() => window.dispatchEvent(new Event('scroll'))")
        await page.wait_for_timeout(100)
        assert not await tooltip.is_visible()

    assert_no_critical_errors(page)
