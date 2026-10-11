"""
test_consolidated_visualizations_and_telemetry.py — Consolidated Regression Test Suite
Merges and deduplicates tests from: test_05_event_inspector.py, test_07_trace_explorer.py, test_08_timeline_nav.py, test_24_waterfall_scrolling.py, test_25_execution_tree_telemetry.py
"""
import os
import re
import json
import tempfile
import pytest
import asyncio
from playwright.async_api import expect, Page
from conftest import APP_URL, DISMISS_ONBOARDING_JS, DEMO_TREES_JS, assert_no_critical_errors

TRACE_TREES = {
    "thread-1": [
        {
            "id": "n1", "ruleId": "r1", "ruleName": "Request",
            "elementName": "Get User", "payload": '{"userId": 42}',
            "thread": "thread-1",
            "timestamp": 1782880200000, "endTimestamp": 1782880205000,
            "duration": 5000, "behavior": "push",
            "correlationId": "TX-998877", "level": "INFO",
            "slaThresholdMs": 3000,
            "events": [
                {
                    "id": "n2", "ruleId": "r2", "ruleName": "SQL",
                    "elementName": "SELECT * FROM users", "payload": "",
                    "thread": "thread-1",
                    "timestamp": 1782880201000, "endTimestamp": 1782880203000,
                    "duration": 2000, "behavior": "inline",
                    "correlationId": "TX-998877", "level": "DEBUG",
                    "events": []
                }
            ]
        },
        {
            "id": "n3", "ruleId": "r1", "ruleName": "Request",
            "elementName": "Update Cart", "payload": '{"cartId": 12}',
            "thread": "thread-1",
            "timestamp": 1782880210000, "endTimestamp": 1782880211000,
            "duration": 1000, "behavior": "push",
            "correlationId": "TX-112233", "level": "INFO",
            "slaThresholdMs": 3000, "events": []
        }
    ]
}
INJECT_TRACE_JS = """(trees) => {
    S.trees = trees;
    S.threads = ['thread-1'];
    S.stats = { fileSize: 1024, linesProcessed: 10, totalNodes: 3, slaBreaches: 1 };
    S.activeThr = 'thread-1';
    S.cfg = {
        globalSettings: { appName: 'Test App' },
        elementRules: [
            { id: 'r1', name: 'Request', slaThresholdMs: 3000 },
            { id: 'r2', name: 'SQL' }
        ]
    };
    UI.render(S.trees, S.threads, S.stats);
    if (typeof ONBOARD !== 'undefined') ONBOARD.dismiss();
    const ob = document.getElementById('ob-ov');
    if (ob) ob.style.display = 'none';
}"""

@pytest.mark.asyncio
async def test_event_inspector_lifecycle_and_metadata(page_with_data):
    """Event Inspector opens on row click, displays metadata, and closes via button or Escape key."""
    page = page_with_data
    inspector = page.locator('#event-inspector')
    assert not await inspector.is_visible(), 'Inspector should be hidden on load'

    # Open via row click
    await page.evaluate("() => UI.svm('tree')")
    first_row = page.locator('.tree-row').first
    await first_row.wait_for(state='visible', timeout=5000)
    await first_row.click()
    await expect(inspector).to_be_visible(timeout=3000)

    # Verify metadata fields
    body = await page.locator('#ins-body-content').text_content()
    assert 'Rule Name' in body, 'Inspector body should show Rule Name field'
    assert 'Thread' in body, 'Inspector body should show Thread field'

    # Close via button
    await page.click('#btn-ins-close')
    await expect(inspector).not_to_be_visible(timeout=2000)

    # Re-open and close via Escape
    await first_row.click()
    await expect(inspector).to_be_visible(timeout=2000)
    await page.keyboard.press('Escape')
    await expect(inspector).not_to_be_visible(timeout=2000)

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_event_inspector_auto_close_conditions(page_with_data):
    """Event Inspector auto-closes on view navigation, thread switch, and empty canvas click."""
    page = page_with_data
    inspector = page.locator('#event-inspector')

    # 1. Navigating to non-event view (settings)
    await page.evaluate("() => UI.svm('tree')")
    first_row = page.locator('.tree-row').first
    await first_row.wait_for(state='visible', timeout=5000)
    await first_row.click()
    await expect(inspector).to_be_visible(timeout=3000)

    await page.evaluate("() => UI.svm('cfg')")
    await expect(inspector).not_to_be_visible(timeout=2000)

    # 2. Thread switch
    await page.evaluate("() => { UI.svm('tree'); UI.sw('main'); }")
    await first_row.click()
    await expect(inspector).to_be_visible(timeout=2000)

    await page.evaluate("() => UI.sw('worker')")
    await expect(inspector).not_to_be_visible(timeout=2000)

    # 3. Empty canvas click
    await page.evaluate("() => UI.svm('tree')")
    await first_row.click()
    await expect(inspector).to_be_visible(timeout=2000)
    await expect(first_row).to_have_class(re.compile(r'kb-focus'))

    await page.evaluate("""() => {
        const vscroll = document.getElementById('tree-vscroll');
        if (vscroll) {
            vscroll.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
        }
    }""")
    await expect(inspector).not_to_be_visible(timeout=2000)
    assert await page.locator('.tree-row.kb-focus').count() == 0

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_trace_explorer_navigation_metrics_and_search(blank_page):
    """Alt+7 navigates to Trace view, renders 3 metric cards and 2 trace rows, and filters via search."""
    page = blank_page
    await page.evaluate(INJECT_TRACE_JS, TRACE_TREES)
    await page.keyboard.press('Alt+7')

    active = page.locator('.vt.active')
    await expect(active).to_have_attribute('data-v', 'trace')

    # Metric cards
    assert await page.locator('.trace-metric-card').count() == 3

    # Row items
    assert await page.locator('.trace-row-item').count() == 2

    # Search filter
    search_input = page.locator('#trace-search-input')
    await search_input.fill('TX-998877')
    assert await page.locator('.trace-row-item').count() == 1

    await search_input.fill('')
    assert await page.locator('.trace-row-item').count() == 2

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_trace_explorer_selection_inspector_and_clear(blank_page):
    """Selecting a trace row marks it active, auto-opens Event Inspector with slowest event, and clears cleanly."""
    page = blank_page
    await page.evaluate(INJECT_TRACE_JS, TRACE_TREES)
    await page.keyboard.press('Alt+7')

    row = page.locator('.trace-row-item:has-text("TX-998877")')
    await row.click()

    assert await row.evaluate("el => el.classList.contains('active-trace')")
    assert await page.evaluate("S.activeTraceId") == 'TX-998877'

    # Inspector auto opens
    inspector = page.locator('#event-inspector')
    await expect(inspector).to_be_visible(timeout=3000)
    body = await page.locator('#ins-body-content').text_content()
    assert 'Get User' in body

    # Clear active filter
    await page.click('button:has-text("Clear Active Filter")')
    assert await page.evaluate("S.activeTraceId") is None

    assert_no_critical_errors(page)
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
@pytest.mark.asyncio
async def test_waterfall_container_dimensions_and_overflow(page_with_data):
    """Waterfall view must constrain .gw within viewport, keeping header/toolbar/nav visible and .g-rows scrollable."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(400)

    # 1. Outer container #res must have overflow-y: hidden to isolate view scrolling
    res_overflow = await page.evaluate("() => document.getElementById('res').style.overflowY")
    assert res_overflow == 'hidden', f"Expected #res style.overflowY to be 'hidden', got '{res_overflow}'"

    # 2. .gw must be bounded within viewport (not expanding to thousands of pixels)
    gw_height, res_height = await page.evaluate("""() => [
        document.querySelector('.gw').clientHeight,
        document.getElementById('res').clientHeight
    ]""")
    assert gw_height <= res_height, f".gw height ({gw_height}px) must be bounded by #res ({res_height}px)"

    # 3. .g-rows must have scrollable content (scrollHeight > clientHeight)
    can_scroll, client_h, scroll_h = await page.evaluate("""() => {
        const rows = document.querySelector('.g-rows');
        return [rows.scrollHeight > rows.clientHeight, rows.clientHeight, rows.scrollHeight];
    }""")
    assert can_scroll is True, f".g-rows must have scrollable content: clientHeight={client_h}, scrollHeight={scroll_h}"

    # 4. Toolbar and Timeline Navigator must be attached and visible
    await expect(page.locator('.g-toolbar')).to_be_visible()
    await expect(page.locator('.g-hdr')).to_be_visible()
    await expect(page.locator('.tl-nav-wrap')).to_be_visible()

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_waterfall_vertical_wheel_scrolling(page_with_data):
    """Mouse wheel scrolling over .g-rows must increase scrollTop while keeping #res at scrollTop 0."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(400)

    # Move mouse over .g-rows
    box = await page.locator('.g-rows').bounding_box()
    assert box is not None, ".g-rows bounding box should exist"
    await page.mouse.move(box['x'] + 120, box['y'] + 120)

    # Dispatch mouse wheel scroll
    await page.mouse.wheel(0, 300)
    await page.wait_for_timeout(300)

    rows_scroll_top, res_scroll_top = await page.evaluate("""() => [
        document.querySelector('.g-rows').scrollTop,
        document.getElementById('res').scrollTop
    ]""")
    assert rows_scroll_top > 0, f"Expected .g-rows scrollTop > 0 after wheel, got {rows_scroll_top}"
    assert res_scroll_top == 0, f"#res scrollTop must remain 0 to prevent toolbar displacement, got {res_scroll_top}"

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_waterfall_horizontal_scrolling_and_header_sync(page_with_data):
    """Horizontal scrolling on .g-rows must automatically sync the time axis header (.g-hdr) scroll position."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(400)

    # 1. Zoom in 2x to create horizontal overflow
    await page.evaluate("() => GANTT_ZOOM_PAN.applyZoom(2)")
    await page.wait_for_timeout(250)

    # 2. Scroll .g-rows horizontally
    target_left = 180
    await page.evaluate(f"() => {{ document.querySelector('.g-rows').scrollLeft = {target_left}; }}")
    await page.wait_for_timeout(250)

    rows_left, hdr_left = await page.evaluate("""() => [
        document.querySelector('.g-rows').scrollLeft,
        document.querySelector('.g-hdr').scrollLeft
    ]""")
    assert rows_left == target_left, f"Expected rows scrollLeft == {target_left}, got {rows_left}"
    assert hdr_left == rows_left, f"Header scrollLeft ({hdr_left}) must match rows scrollLeft ({rows_left})"

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_waterfall_keyboard_scrolling(page_with_data):
    """Focusing .g-rows and pressing ArrowDown must scroll the waterfall rows vertically."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(400)

    # 1. Verify tabindex and focus
    tabindex = await page.locator('.g-rows').get_attribute('tabindex')
    assert tabindex == '0', f"Expected .g-rows tabindex='0', got {tabindex}"

    await page.evaluate("() => document.querySelector('.g-rows').focus()")
    await page.wait_for_timeout(100)

    # 2. Press ArrowDown multiple times
    for _ in range(4):
        await page.keyboard.press('ArrowDown')
        await page.wait_for_timeout(60)

    scroll_top = await page.evaluate("() => document.querySelector('.g-rows').scrollTop")
    assert scroll_top > 0, f"Expected keyboard ArrowDown to scroll rows (scrollTop > 0), got {scroll_top}"

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_waterfall_rapid_tab_switching_scroll_stability(page_with_data):
    """Switching between Split, Tree, Waterfall, and Trace views retains correct scrollability in Waterfall mode."""
    page = page_with_data

    views = ['split', 'tree', 'gantt', 'trace', 'gantt']
    for v in views:
        await page.evaluate(f"() => UI.svm('{v}')")
        await page.wait_for_timeout(150)

    # Final verification on Waterfall mode
    state = await page.evaluate("""() => {
        const rows = document.querySelector('.g-rows');
        const res = document.getElementById('res');
        return {
            resOverflowY: res.style.overflowY,
            canScroll: rows ? rows.scrollHeight > rows.clientHeight : false,
            hasHdr: document.querySelector('.g-hdr') !== null
        };
    }""")
    assert state['resOverflowY'] == 'hidden'
    assert state['canScroll'] is True
    assert state['hasHdr'] is True

    assert_no_critical_errors(page)
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
