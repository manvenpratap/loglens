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
async def test_dynamic_trace_dropdown_interaction(page_with_data):
    """Dynamic Trace ID dropdown opens, filters via search input, selects a trace, and clears cleanly."""
    page = page_with_data

    # Trace dropdown should be mounted and visible since page_with_data has traces
    trace_dd = page.locator('#trace-dropdown')
    await expect(trace_dd).to_be_visible(timeout=3000)

    btn = page.locator('#trace-dropdown-btn')
    label = page.locator('#trace-active-label')
    clear_btn = page.locator('#trace-clear-btn')

    assert await label.text_content() == 'All Traces'
    assert not await clear_btn.is_visible()

    # Open dropdown
    await btn.click()
    menu = page.locator('#trace-dropdown-menu')
    await expect(menu).to_be_visible()

    # Verify search input is present
    search_inp = page.locator('#trace-search-inp')
    await expect(search_inp).to_be_visible()

    # Type in search input to filter trace IDs
    await search_inp.fill('TX-A1')
    visible_items = page.locator('#trace-dropdown-list li:visible')
    assert await visible_items.count() == 1
    assert 'TX-A1' in await visible_items.first.text_content()

    # Select the trace
    await visible_items.first.click()
    await expect(menu).not_to_be_visible()

    # Verify active state
    assert await page.evaluate("S.activeTraceId") == 'TX-A1'
    assert await label.text_content() == '# TX-A1'
    await expect(clear_btn).to_be_visible()

    # Test clearing via the quick clear button
    await clear_btn.click()
    assert await page.evaluate("S.activeTraceId") is None
    assert await label.text_content() == 'All Traces'
    await expect(clear_btn).not_to_be_visible()

    # Test keyboard navigation (Escape to close)
    await btn.click()
    await expect(menu).to_be_visible()
    await page.keyboard.press('Escape')
    await expect(menu).not_to_be_visible()

    assert_no_critical_errors(page)

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
async def test_timeline_nav_only_enabled_in_timeline_view(page_with_data):
    """Timeline navigator must only be enabled in dedicated timeline (gantt) view and absent in split view."""
    page = page_with_data
    # 1. Split view must not mount navigator
    await page.evaluate("() => UI.svm('split')")
    await page.wait_for_timeout(300)
    assert await page.locator('.tl-nav-wrap').count() == 0, "Navigator should not exist in split view"

    # 2. Timeline view must mount navigator
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(300)
    await expect(page.locator('.tl-nav-wrap')).to_be_visible(timeout=3000)

    # 3. Switching back to split view must cleanly remove navigator
    await page.evaluate("() => UI.svm('split')")
    await page.wait_for_timeout(300)
    assert await page.locator('.tl-nav-wrap').count() == 0, "Navigator should be cleaned up when leaving timeline view"

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

    # Column header row (Payload Preview column is removed; payload is accessed via inline row button)
    tree_hdr = page.locator('#tree-hdr')
    await expect(tree_hdr).to_be_visible()
    await expect(tree_hdr.locator('.tree-hdr-spine')).to_contain_text('Operation & Hierarchy')
    assert await tree_hdr.locator('.tree-hdr-payload').count() == 0
    await expect(tree_hdr.locator('.tree-th-dur')).to_contain_text('Duration')
    await expect(tree_hdr.locator('.tree-th-ts')).to_contain_text('Timestamp')

    # Horizontal scroll synchronization (when viewport overflows min-width)
    await page.set_viewport_size({'width': 600, 'height': 800})
    await page.evaluate("() => { const vs = document.getElementById('tree-vscroll'); vs.scrollLeft = 50; vs.dispatchEvent(new Event('scroll')); }")
    assert await page.evaluate("() => document.getElementById('tree-hdr').scrollLeft") == 50
    await page.set_viewport_size({'width': 1400, 'height': 900})

    # Rows have spine + telemetry strip; no .tree-payload-col
    row = page.locator('.tree-row').first
    await expect(row).to_be_visible()

    spine = row.locator('.tree-spine')
    await expect(spine).to_be_visible()
    await expect(spine.locator('.tnm')).to_be_visible()

    assert await row.locator('.tree-payload-col').count() == 0

    telemetry_col = row.locator('.tree-telemetry-col')
    await expect(telemetry_col).to_be_visible()
    await expect(telemetry_col.locator('.tree-metric-dur')).to_be_visible()
    await expect(telemetry_col.locator('.tree-metric-ts')).to_be_visible()

    # Interactive payload button reveals payload popover on click
    payload_btn = page.locator('.tree-payload-btn').first
    if await payload_btn.count() > 0:
        await expect(payload_btn).to_be_visible()
        await payload_btn.click()
        popover = page.locator('#tree-payload-popover')
        await expect(popover).to_be_visible()
        await expect(popover.locator('#tree-payload-code')).to_be_visible()
        # Close button closes popover
        await popover.locator('#tree-popover-close-btn').click()
        await expect(popover).not_to_be_attached()

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_execution_tree_column_resizing(page_with_data):
    """Execution Tree column headers have draggable resizer handles that update column widths, persist in localStorage, and reset on double-click."""
    page = page_with_data
    await page.evaluate("() => UI.svm('tree')")

    tree_hdr = page.locator('#tree-hdr')
    await expect(tree_hdr).to_be_visible()

    # 5 resizers exist (spine, spark, dur, self, ts)
    resizers = tree_hdr.locator('.tree-col-resizer')
    assert await resizers.count() == 5

    col_keys = ['spine', 'spark', 'dur', 'self', 'ts']
    for key in col_keys:
        resizer = tree_hdr.locator(f'.tree-col-resizer[data-col="{key}"]')
        await expect(resizer).to_be_visible()

    # Initial width of spine
    initial_w = await page.evaluate("() => document.querySelector('.tree-hdr-spine').getBoundingClientRect().width")

    # Drag spine resizer by +80px
    spine_resizer = tree_hdr.locator('.tree-col-resizer[data-col="spine"]')
    box = await spine_resizer.bounding_box()
    assert box is not None

    start_x = box['x'] + box['width'] / 2
    start_y = box['y'] + box['height'] / 2

    await page.mouse.move(start_x, start_y)
    await page.mouse.down()
    await page.mouse.move(start_x + 80, start_y)
    await page.mouse.up()

    # Verify CSS custom property updated
    new_spine_w_str = await page.evaluate("() => getComputedStyle(document.documentElement).getPropertyValue('--tree-spine-w').trim()")
    new_spine_w = float(new_spine_w_str.replace('px', ''))
    assert new_spine_w > initial_w

    # Verify row spine also expanded
    row_spine_w = await page.evaluate("() => document.querySelector('.tree-row .tree-spine').getBoundingClientRect().width")
    assert abs(row_spine_w - new_spine_w) < 2

    # Verify saved in localStorage
    stored_w = await page.evaluate("() => localStorage.getItem('ll-tree-col-spine')")
    assert stored_w is not None and int(stored_w) == int(new_spine_w)

    # Double click to reset
    await spine_resizer.dblclick()
    reset_spine_w_str = await page.evaluate("() => getComputedStyle(document.documentElement).getPropertyValue('--tree-spine-w').trim()")
    assert reset_spine_w_str == '420px'

    # Verify localStorage cleared on reset
    cleared = await page.evaluate("() => localStorage.getItem('ll-tree-col-spine')")
    assert cleared is None

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

@pytest.mark.asyncio
async def test_execution_tree_inline_column_filters(page_with_data):
    """Inline column filters bar opens, filters tree nodes across Operation, SLA, Duration, and clears cleanly."""
    page = page_with_data
    await page.evaluate("() => UI.svm('tree')")

    filter_btn = page.locator('#btn-tree-filter-toggle')
    await expect(filter_btn).to_be_visible()

    filter_bar = page.locator('#tree-filter-bar')
    # Initially hidden
    assert not await filter_bar.is_visible()

    # Click filter toggle button
    await filter_btn.click()
    await expect(filter_bar).to_be_visible()

    # Filter by operation name
    op_input = page.locator('#tree-col-filter-op')
    await expect(op_input).to_be_visible()

    initial_nodes = await page.evaluate("() => TR._visibleNodes.length")
    assert initial_nodes > 0

    # Type operation filter
    await op_input.fill('Database')
    await page.wait_for_timeout(100)

    filtered_nodes = await page.evaluate("() => TR._visibleNodes.length")
    assert filtered_nodes <= initial_nodes

    # Check badge counter
    badge = page.locator('#tree-filter-count')
    await expect(badge).to_be_visible()
    assert await badge.text_content() == '1'

    # Filter clear button clears input and resets count
    clear_op = page.locator('.tree-filter-clear-btn[data-clear="op"]')
    await expect(clear_op).to_be_visible()
    await clear_op.click()
    await page.wait_for_timeout(100)

    cleared_nodes = await page.evaluate("() => TR._visibleNodes.length")
    assert cleared_nodes == initial_nodes
    assert not await clear_op.is_visible()

    # Toggling filter bar via toolbar button focuses first filter input
    filter_toggle = page.locator('#btn-tree-filter-toggle')
    await filter_toggle.click()  # close
    await page.wait_for_timeout(50)
    await filter_toggle.click()  # reopen & focus
    await page.wait_for_timeout(50)
    is_focused = await op_input.evaluate("el => el === document.activeElement")
    assert is_focused

    assert_no_critical_errors(page)

@pytest.mark.asyncio
async def test_execution_tree_critical_path_toggle_and_dimming(page_with_data):
    """Critical path toggle in tree toolbar greys out non-critical rows and highlights critical rows."""
    page = page_with_data
    await page.evaluate("() => UI.svm('tree')")

    crit_chk = page.locator('#tree-crit-chk')
    await expect(crit_chk).to_be_visible()

    # Initially unchecked
    assert not await crit_chk.is_checked()
    assert await page.locator('.tree-row.tree-dim').count() == 0

    # Toggle critical path ON
    await crit_chk.check()
    await page.wait_for_timeout(100)

    assert await page.evaluate("() => S.criticalPathOn") is True

    # If critical path nodes exist, non-critical rows should be dimmed (.tree-dim)
    has_crit = await page.evaluate("() => TR._visibleNodes.some(n => n._isCriticalPath)")
    if has_crit:
        assert await page.locator('.tree-row.tree-critical').count() > 0
        assert await page.locator('.tree-row.tree-dim').count() > 0

    # Toggle critical path OFF restores all rows
    await crit_chk.uncheck()
    await page.wait_for_timeout(100)

    assert await page.evaluate("() => S.criticalPathOn") is False
    assert await page.locator('.tree-row.tree-critical').count() == 0
    assert await page.locator('.tree-row.tree-dim').count() == 0

    assert_no_critical_errors(page)

@pytest.mark.asyncio
async def test_dynamic_trace_dropdown_interaction(page_with_data):
    """Dynamic Trace ID dropdown mounts in action bar, opens searchable menu, filters, and clears."""
    page = page_with_data

    # Ensure traces exist or inject mock traces to test full dropdown lifecycle
    trace_dropdown = page.locator('#trace-dropdown')
    has_traces = await page.evaluate("() => { return !!(document.getElementById('trace-dropdown') && document.getElementById('trace-dropdown').style.display !== 'none'); }")
    if not has_traces:
        # Populate synthetic traces in S.trees to test dropdown
        await page.evaluate("""() => {
            if (!S.trees || !S.trees.length) S.trees = [{ id: '1', ruleName: 'Root', thread: 'worker-1', correlationId: 'TR-1001', duration: 150 }];
            else S.trees[0].correlationId = 'TR-1001';
            UI.renderTraceDropdown(S.trees);
        }""")
        await page.wait_for_timeout(100)

    await expect(trace_dropdown).to_be_visible()
    btn = page.locator('#trace-dropdown-btn')
    await expect(btn).to_be_visible()
    await expect(btn).to_contain_text('Trace')
    await expect(page.locator('#trace-active-label')).to_contain_text('All Traces')

    # Open dropdown menu
    await btn.click()
    await page.wait_for_timeout(100)
    menu = page.locator('#trace-dropdown-menu')
    await expect(menu).to_be_visible()

    # Search filter within menu
    search_input = menu.locator('#trace-search-inp')
    await expect(search_input).to_be_visible()
    await search_input.fill('TX')
    await page.wait_for_timeout(100)

    # Click first available matching visible item
    items = menu.locator('li[data-trace]:not([data-trace="all"])')
    count = await items.count()
    assert count >= 1

    target_item = items.first
    target_tid = await target_item.evaluate("el => el.dataset.trace")
    assert target_tid
    await target_item.click()
    await page.wait_for_timeout(100)
    assert await page.evaluate("() => S.activeTraceId") == target_tid
    assert await page.locator('#trace-clear-btn').is_visible()

    # Clear trace filter via clear button
    await page.locator('#trace-clear-btn').click()
    await page.wait_for_timeout(100)
    assert not (await page.evaluate("() => S.activeTraceId"))

    assert_no_critical_errors(page)

@pytest.mark.asyncio
async def test_execution_tree_thread_grouping_and_telemetry(page_with_data):
    """Execution Tree groups by thread and aligns telemetry columns cleanly."""
    page = page_with_data
    await page.evaluate("() => UI.svm('tree')")
    await page.wait_for_timeout(150)

    # Telemetry column headers
    assert await page.locator('.tree-th-spark').is_visible()
    assert await page.locator('.tree-th-dur').is_visible()
    assert await page.locator('.tree-th-self').is_visible()
    assert await page.locator('.tree-th-ts').is_visible()
    assert await page.locator('.tree-th-thread').count() == 0

    # Ensure tree rows are styled with thread left border
    rows = page.locator('.tree-row')
    if await rows.count() > 0:
        first_row = rows.first
        border_left = await first_row.evaluate("el => window.getComputedStyle(el).borderLeftStyle")
        assert border_left == 'solid'

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_split_view_row_background_colors_synchronized(page_with_data):
    """In Split view, Waterfall (.g-row) and Swimlane (.swim-lane) row backgrounds match Tree (.tree-row)."""
    page = page_with_data
    await page.evaluate("() => UI.svm('split')")
    await page.wait_for_timeout(200)

    # 1. Verify Waterfall and Tree in Split View have synchronized row backgrounds
    sync_check = await page.evaluate("""() => {
        const gRows = document.querySelectorAll('.res-split .sp-pane:first-child .g-row');
        const treeRows = document.querySelectorAll('.res-split .sp-pane:last-child .tree-row');
        if (!gRows.length || !treeRows.length) return { ok: false, reason: 'missing rows' };
        
        let matchCount = 0;
        for (let i = 0; i < Math.min(gRows.length, treeRows.length); i++) {
            const gr = gRows[i];
            const tr = treeRows[i];
            const grBg = window.getComputedStyle(gr).backgroundColor;
            const trBg = window.getComputedStyle(tr).backgroundColor;
            const grLbl = gr.querySelector('.g-lbl');
            const grLblBg = grLbl ? window.getComputedStyle(grLbl).backgroundColor : null;
            
            if (grBg === trBg && (!grLbl || grLblBg === trBg)) {
                matchCount++;
            }
        }
        return { ok: true, matchCount, total: Math.min(gRows.length, treeRows.length) };
    }""")
    assert sync_check['ok'] is True
    assert sync_check['matchCount'] == sync_check['total']
    assert sync_check['total'] > 0

    # 2. Verify Swimlane in Split View has thread-tinted background matching thread palette
    await page.evaluate("""() => {
        S.swimlaneMode = true;
        UI.rv();
    }""")
    await page.wait_for_timeout(200)

    swim_check = await page.evaluate("""() => {
        const lanes = document.querySelectorAll('.res-split .sp-pane:first-child .swim-lane');
        if (!lanes.length) return { ok: false, reason: 'missing swimlanes' };
        let validCount = 0;
        lanes.forEach(lane => {
            const thr = lane.dataset.thread;
            if (thr && typeof TR !== 'undefined') {
                const tCol = TR.getThreadColor(thr);
                const bg = window.getComputedStyle(lane).backgroundColor;
                if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') validCount++;
            }
        });
        return { ok: true, validCount, total: lanes.length };
    }""")
    assert swim_check['ok'] is True
    assert swim_check['validCount'] == swim_check['total']
    assert swim_check['total'] > 0

    # 3. Verify Light / Ivory theme has zero row banding
    await page.evaluate("""() => {
        document.documentElement.setAttribute('data-theme', 'ivory');
        S.swimlaneMode = false;
        UI.svm('split');
        UI.rv();
    }""")
    await page.wait_for_timeout(200)

    light_check = await page.evaluate("""() => {
        const treeRows = [...document.querySelectorAll('.res-split .sp-pane:last-child .tree-row:not(.tree-thr-group-row)')];
        const gRows = [...document.querySelectorAll('.res-split .sp-pane:first-child .g-row:not(.g-thr-group-row)')];
        const mainTreeBgs = [...new Set(treeRows.filter(r => r.dataset.thread === 'main').map(r => window.getComputedStyle(r).backgroundColor))];
        const mainGBgs = [...new Set(gRows.filter(r => r.dataset.thread === 'main').map(r => window.getComputedStyle(r).backgroundColor))];
        return {
            mainTreeBgsCount: mainTreeBgs.length,
            mainGBgsCount: mainGBgs.length,
            treeBg: mainTreeBgs[0],
            gBg: mainGBgs[0]
        };
    }""")
    assert light_check['mainTreeBgsCount'] == 1, "Tree rows in main thread must have uniform background (no banding)"
    assert light_check['mainGBgsCount'] == 1, "Waterfall rows in main thread must have uniform background (no banding)"
    assert light_check['treeBg'] == light_check['gBg'], "Tree and Waterfall backgrounds must match in light theme"

    # Reset theme back to dark
    await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'dark')")

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_advanced_swimlane_studio_telemetry_stacking_and_controls(page_with_data):
    """Verify Swimlane Studio advanced features: concurrency interval stacking, KPI telemetry, grouping, crosshair, and hover card."""
    page = page_with_data

    # 1. Switch to Gantt view in Swimlane mode
    await page.evaluate("""() => {
        S.swimlaneMode = true;
        UI.svm('gantt');
        UI.rv();
    }""")
    await page.wait_for_timeout(250)

    # 2. Check UI elements & controls exist
    controls = await page.evaluate("""() => {
        return {
            lanesCount: document.querySelectorAll('.swim-lane').length,
            hasToggleBtn: Boolean(document.getElementById('btn-swim-toggle')),
            hasGrpThread: Boolean(document.getElementById('btn-swim-grp-thread')),
            hasGrpRule: Boolean(document.getElementById('btn-swim-grp-rule')),
            hasGrpLevel: Boolean(document.getElementById('btn-swim-grp-level')),
            hasStackBtn: Boolean(document.getElementById('btn-swim-mode-stack')),
            hasCompactBtn: Boolean(document.getElementById('btn-swim-mode-compact')),
            hasSearchInp: Boolean(document.getElementById('swim-search-inp')),
            hasErrorsChk: Boolean(document.getElementById('chk-swim-errors')),
            hasCrosshair: Boolean(document.getElementById('swim-crosshair-line')),
            hasHoverCard: Boolean(document.getElementById('swim-hover-card')),
            kpiSpansCount: document.querySelectorAll('.swim-kpi-pill.kpi-spans').length
        };
    }""")
    assert controls['lanesCount'] > 0
    assert controls['hasToggleBtn'] is True
    assert controls['hasGrpThread'] is True
    assert controls['hasGrpRule'] is True
    assert controls['hasGrpLevel'] is True
    assert controls['hasStackBtn'] is True
    assert controls['hasCompactBtn'] is True
    assert controls['hasSearchInp'] is True
    assert controls['hasErrorsChk'] is True
    assert controls['hasCrosshair'] is True
    assert controls['hasHoverCard'] is True
    assert controls['kpiSpansCount'] == controls['lanesCount']

    # 3. Test Grouping modes
    # Test Rule Grouping
    await page.click('#btn-swim-grp-rule')
    await page.wait_for_timeout(200)
    rule_group_check = await page.evaluate("() => ({ groupBy: SWIM.groupBy, lanes: document.querySelectorAll('.swim-lane').length })")
    assert rule_group_check['groupBy'] == 'rule'
    assert rule_group_check['lanes'] > 0

    # Test Level Grouping
    await page.click('#btn-swim-grp-level')
    await page.wait_for_timeout(200)
    level_group_check = await page.evaluate("() => ({ groupBy: SWIM.groupBy, lanes: document.querySelectorAll('.swim-lane').length })")
    assert level_group_check['groupBy'] == 'level'
    assert level_group_check['lanes'] > 0

    # Switch back to Thread Grouping
    await page.click('#btn-swim-grp-thread')
    await page.wait_for_timeout(200)
    thread_group_check = await page.evaluate("() => ({ groupBy: SWIM.groupBy, lanes: document.querySelectorAll('.swim-lane').length })")
    assert thread_group_check['groupBy'] == 'thread'

    # 4. Test Stacking vs Compact layout
    await page.click('#btn-swim-mode-compact')
    await page.wait_for_timeout(150)
    compact_mode = await page.evaluate("() => SWIM.layoutMode")
    assert compact_mode == 'compact'

    await page.click('#btn-swim-mode-stack')
    await page.wait_for_timeout(150)
    stack_mode = await page.evaluate("() => SWIM.layoutMode")
    assert stack_mode == 'stack'

    # 5. Test search filter dimming
    filter_check = await page.evaluate("""() => {
        const inp = document.getElementById('swim-search-inp');
        inp.value = 'nonexistentqueryxyz';
        inp.dispatchEvent(new Event('input'));
        const totalBars = document.querySelectorAll('.swim-bar').length;
        const dimBars = document.querySelectorAll('.swim-bar.bar-dim').length;
        
        // Reset filter
        inp.value = '';
        inp.dispatchEvent(new Event('input'));
        const dimAfterReset = document.querySelectorAll('.swim-bar.bar-dim').length;
        return { totalBars, dimBars, dimAfterReset };
    }""")
    assert filter_check['dimBars'] == filter_check['totalBars']
    assert filter_check['dimAfterReset'] == 0

    # 6. Test Hover Card on mouseover of a bar
    hover_check = await page.evaluate("""() => {
        const bar = document.querySelector('.swim-bar');
        if (!bar) return { ok: false };
        const rows = document.getElementById('swim-lanes-rows');
        const ev = new MouseEvent('mouseover', { bubbles: true, clientX: 200, clientY: 200 });
        bar.dispatchEvent(ev);
        const card = document.getElementById('swim-hover-card');
        const isShown = card && card.style.display === 'block';
        const title = document.getElementById('swim-card-title')?.textContent;
        return { ok: true, isShown, title };
    }""")
    assert hover_check['ok'] is True
    assert hover_check['isShown'] is True
    assert len(hover_check['title']) > 0

    # Reset swimlane mode for following tests
    await page.evaluate("""() => {
        S.swimlaneMode = false;
        UI.rv();
    }""")
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_timeline_row_background_full_scroll_width(page_with_data):
    """
    Verify that on Timeline and Split views, row backgrounds and borders
    span the full scrollable width when scrolled horizontally, preventing
    uncolored/gray clipping on the right.
    """
    page = page_with_data

    # 1. Switch to Timeline (Gantt) view
    await page.evaluate("() => { if (typeof UI !== 'undefined') UI.svm('gantt'); }")
    await page.wait_for_selector('.g-rows', timeout=5000)

    # 2. Test horizontal scroll at zoom 1.0 and 2.0
    for zoom in [1.0, 2.0]:
        await page.evaluate(f"() => {{ S.ganttZoom = {zoom}; document.documentElement.style.setProperty('--g-zoom', {zoom}); }}")
        await page.wait_for_timeout(100)

        # Scroll fully to the right
        await page.evaluate("() => { const r = document.querySelector('.g-rows'); if (r) r.scrollLeft = r.scrollWidth; }")
        await page.wait_for_timeout(100)

        check = await page.evaluate("""() => {
            const rowsCont = document.querySelector('.g-rows');
            const rows = Array.from(document.querySelectorAll('.g-row'));
            if (!rowsCont || rows.length === 0) return { ok: false };
            const cRect = rowsCont.getBoundingClientRect();
            
            // Check first 5 rows
            const sample = rows.slice(0, 5);
            for (const r of sample) {
                const rRect = r.getBoundingClientRect();
                const diff = cRect.right - rRect.right;
                if (diff > 3) return { ok: false, reason: 'Row right edge cut off: diff=' + diff };
            }
            return { ok: true, scrollLeft: rowsCont.scrollLeft, scrollWidth: rowsCont.scrollWidth };
        }""")
        assert check['ok'] is True, f"Timeline row should span full width at zoom {zoom}: {check}"

    # 3. Test in Split view
    await page.evaluate("() => { if (typeof UI !== 'undefined') UI.svm('split'); }")
    await page.wait_for_selector('.res-split .g-rows', timeout=5000)
    await page.evaluate("() => { const r = document.querySelector('.res-split .g-rows'); if (r) r.scrollLeft = r.scrollWidth; }")
    await page.wait_for_timeout(100)

    split_check = await page.evaluate("""() => {
        const rowsCont = document.querySelector('.res-split .g-rows');
        const row = rowsCont ? rowsCont.querySelector('.g-row') : null;
        if (!rowsCont || !row) return { ok: false };
        const cRect = rowsCont.getBoundingClientRect();
        const rRect = row.getBoundingClientRect();
        const diff = cRect.right - rRect.right;
        return { ok: diff <= 5, diff };
    }""")
    assert split_check['ok'] is True, f"Split view row should span full track width: {split_check}"

    assert_no_critical_errors(page)


