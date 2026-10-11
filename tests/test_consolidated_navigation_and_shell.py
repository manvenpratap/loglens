"""
test_consolidated_navigation_and_shell.py — Consolidated Regression Test Suite
Merges and deduplicates tests from: test_01_onboarding.py, test_02_view_navigation.py, test_04_command_palette.py, test_20_demo_showcase.py, test_22_two_tier_navigation.py
"""
import os
import re
import json
import tempfile
import pytest
import asyncio
from playwright.async_api import expect, Page
from conftest import APP_URL, DISMISS_ONBOARDING_JS, DEMO_TREES_JS, assert_no_critical_errors


@pytest.mark.asyncio
async def test_onboarding_overlay_shown_on_load(blank_page):
    """Onboarding overlay must be visible before any interaction."""
    ob = blank_page.locator('#ob-ov')
    await expect(ob).to_be_visible(timeout=5000)
@pytest.mark.asyncio
async def test_demo_load_dismisses_onboarding_and_renders_results(blank_page):
    """Clicking Try Demo loads sample data, hides onboarding, and activates results container."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#ob-ov')).to_be_hidden(timeout=15000)
    await expect(page.locator('#res .res-split')).to_be_visible(timeout=15000)
    await expect(page.locator('#res')).to_be_visible()
@pytest.mark.asyncio
async def test_empty_state_guide_injected(blank_page):
    """
    With no data and onboarding dismissed, navigating to gantt should show
    the #emp empty state enriched with the 3-step guide (Phase 10).
    """
    page = blank_page
    # Dismiss onboarding without loading data
    await page.evaluate(DISMISS_ONBOARDING_JS)
    # Switch to gantt view (no data)
    await page.evaluate("() => { if (typeof UI !== 'undefined') UI.svm('gantt'); }")
    await page.wait_for_timeout(400)

    emp = page.locator('#emp')
    await expect(emp).to_be_visible(timeout=3000)

    # Guide should be injected by Phase 10 patch
    guide = page.locator('.emp-guide')
    await expect(guide).to_be_visible(timeout=3000)

    steps = page.locator('.emp-guide-step')
    assert await steps.count() == 3, 'Expect exactly 3 step cards in guide'
@pytest.mark.asyncio
async def test_empty_state_shortcuts_strip(blank_page):
    """Shortcut hint chips must render in the first-run guide."""
    page = blank_page
    await page.evaluate(DISMISS_ONBOARDING_JS)
    await page.evaluate("() => { if (typeof UI !== 'undefined') UI.svm('gantt'); }")
    await page.wait_for_timeout(400)

    shortcuts = page.locator('.emp-shortcut')
    count = await shortcuts.count()
    assert count >= 3, f'Expected at least 3 shortcut chips, got {count}'
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
async def test_split_view_auto_alignment_and_sync_scroll(page_with_data):
    """Split view rows must auto-align vertically and auto-scroll in sync on both sides."""
    page = page_with_data
    # Inject 40 rows to ensure both sides have ample scrollable overflow
    await page.evaluate("""() => {
        const _t0 = Date.now() - 10000;
        const _mk = (i, thr, lvl, dur, cid) => ({
            id: 'n' + i,
            ruleId: 'r1', ruleName: 'Op-' + i,
            elementName: 'Element-' + i, payload: '{}',
            thread: thr, timestamp: _t0 + i * 300, duration: dur,
            endTimestamp: _t0 + i * 300 + dur,
            behavior: 'push', level: lvl,
            slaBreached: (dur > 2000),
            correlationId: cid || 'trace-' + (i % 3 + 1),
            rawLine: 'line ' + i, events: [], visualStyle: {}
        });
        S.trees.main = Array.from({length: 40}, (_, i) => _mk(i, 'main', 'INFO', 200, 'TX-A' + (i % 3)));
        UI.render(S.trees, S.threads, S.stats);
        UI.svm('split');
    }""")
    await page.wait_for_timeout(400)

    g_row0 = page.locator('.g-row').first
    t_row0 = page.locator('.tree-row').first
    g_box = await g_row0.bounding_box()
    t_box = await t_row0.bounding_box()
    assert abs(g_box['y'] - t_box['y']) < 2, f"Y misalignment: Gantt={g_box['y']} vs Tree={t_box['y']}"
    assert abs(g_box['height'] - 32) < 2, f"Gantt row height not 32: {g_box['height']}"
    assert abs(t_box['height'] - 32) < 2, f"Tree row height not 32: {t_box['height']}"

    # Sync scroll Gantt -> Tree
    g_rows = page.locator('.g-rows')
    tree_vscroll = page.locator('#tree-vscroll')
    await g_rows.evaluate('el => { el.scrollTop = 100; el.dispatchEvent(new Event("scroll")); }')
    await page.wait_for_timeout(150)
    tree_top = await tree_vscroll.evaluate('el => el.scrollTop')
    assert abs(tree_top - 100) < 2, f"Scroll sync Gantt->Tree failed: {tree_top}"

    # Sync scroll Tree -> Gantt
    await tree_vscroll.evaluate('el => { el.scrollTop = 150; el.dispatchEvent(new Event("scroll")); }')
    await page.wait_for_timeout(150)
    gantt_top = await g_rows.evaluate('el => el.scrollTop')
    assert abs(gantt_top - 150) < 2, f"Scroll sync Tree->Gantt failed: {gantt_top}"

@pytest.mark.asyncio
async def test_split_view_responsive_column_reveal(page_with_data):
    """In 50/50 split only fitting columns display; dragging responsively reveals additional columns."""
    page = page_with_data
    await page.evaluate("() => UI.svm('split')")
    await page.wait_for_timeout(400)

    # In default 50/50 split, verify no horizontal overflow on Tree
    tree_vscroll = page.locator('#tree-vscroll')
    dims = await tree_vscroll.evaluate('el => ({ scrollWidth: el.scrollWidth, clientWidth: el.clientWidth })')
    assert dims['scrollWidth'] <= dims['clientWidth'], f"Horizontal overflow in 50/50 split: {dims}"

    # Drag splitter to widen right pane
    hdl = page.locator('#sp-hdl')
    hdl_box = await hdl.bounding_box()
    await page.mouse.move(hdl_box['x'] + hdl_box['width'] / 2, hdl_box['y'] + 100)
    await page.mouse.down()
    await page.mouse.move(360, hdl_box['y'] + 100)
    await page.mouse.up()
    await page.wait_for_timeout(300)

    ts_hdr = page.locator('.tree-th-ts')
    self_hdr = page.locator('.tree-th-self')
    thread_hdr = page.locator('.tree-th-thread')
    assert await ts_hdr.is_visible()
    assert await self_hdr.is_visible()
    assert await thread_hdr.is_visible()

    # Double click to reset to 50%
    await hdl.dblclick()
    await page.wait_for_timeout(300)
    assert await page.evaluate('S.splitRatio') == 50
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
@pytest.mark.asyncio
async def test_demo_showcase_data_integrity(blank_page):
    """Demo loads 16 threads with traces, multiline payloads, SLAs, outliers, and sticky notes."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#ob-ov')).to_be_hidden(timeout=15000)
    await expect(page.locator('#res .res-split')).to_be_visible(timeout=15000)

    # 1. Multi-thread & root trees
    threads_count = await page.evaluate("() => S.threads.length")
    assert threads_count >= 16, f"Expected at least 16 threads, got {threads_count}"
    w1_trees = await page.evaluate("() => S.trees['worker-1']?.length")
    assert w1_trees > 0, "worker-1 tree must have root nodes"

    # 2. Distributed Traces
    traces = await page.evaluate("() => TRACE_EXPLORER.scanTraces()")
    assert len(traces) >= 3, f"Expected at least 3 traces, got {len(traces)}"
    checkout_trace = next((t for t in traces if t.get('id') == 'trace-ord-8921'), None)
    assert checkout_trace is not None, "trace-ord-8921 must exist in demo"
    assert set(checkout_trace.get('threads', [])) == {'worker-1', 'worker-2', 'worker-3'}

    # 3. Multiline Payloads (Class header, formatted JSON, SQL exception with Caused by)
    w1_req_payload = await page.evaluate("""() => {
        const root = S.trees['worker-1'][0];
        const req = root.events.find(e => e.elementName === '/api/checkout');
        return req ? req.payload : null;
    }""")
    assert "class OrderCheckoutRequest {" in w1_req_payload
    assert 'customerId: "cust-9481"' in w1_req_payload

    w2_charge_payload = await page.evaluate("""() => {
        const root = S.trees['worker-2'][0];
        const req = root.events.find(e => e.elementName === '/api/payment/charge');
        return req ? req.payload : null;
    }""")
    assert '"event": "charge.initiated"' in w2_charge_payload

    w2_err_payload = await page.evaluate("""() => {
        const root = S.trees['worker-2'][1];
        function findErr(nodes) {
            for (const n of nodes) {
                if (n.ruleName === 'Error' || n.level === 'ERROR') return n;
                if (n.events?.length) {
                    const found = findErr(n.events);
                    if (found) return found;
                }
            }
            return null;
        }
        const err = findErr([root]);
        return err ? err.payload : null;
    }""")
    assert "java.sql.SQLException: Deadlock detected" in w2_err_payload
    assert "Caused by: com.mysql.cj.exceptions.DeadlockException" in w2_err_payload

    # 4. SLA & Outlier Detection
    sla_count = await page.evaluate("() => S.slaBreachCount")
    outlier_count = await page.evaluate("() => S.outlierCount")
    assert sla_count >= 2, f"Expected at least 2 SLA breaches, got {sla_count}"
    assert outlier_count >= 2, f"Expected at least 2 outliers, got {outlier_count}"
    await expect(page.locator('#hdr-sla')).to_be_visible()
    await expect(page.locator('#hdr-outliers')).to_be_visible()

    # 5. Pre-seeded sticky notes
    ann_keys = await page.evaluate("() => Object.keys(S.annotations || {})")
    assert len(ann_keys) >= 2, f"Expected at least 2 annotations, got {len(ann_keys)}"
    await page.evaluate("() => { UI.sw('worker-2'); UI.svm('tree'); }")
    note_badges = page.locator('.tnt')
    assert await note_badges.count() >= 1

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_demo_execution_tree_and_views_navigation(blank_page):
    """Demo displays all-thread aggregated tree, supports thread scoping, and switches through all 7 views seamlessly."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#res .res-split')).to_be_visible(timeout=15000)

    # All-thread tree aggregation & metrics check in stats view
    assert await page.evaluate("() => S.activeThr") == 'all'
    await page.evaluate("() => UI.svm('stats')")
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=5000)
    nodes_text = await page.locator('#s-nodes').inner_text()
    total_nodes = int(nodes_text.strip())
    assert total_nodes >= 40
    assert "All Threads" in await page.locator('#vt-active-label').inner_text()

    # Switch to tree view
    await page.evaluate("() => UI.svm('tree')")
    tree_badge = (await page.locator('#tree-badge-count').inner_text()).lower()
    assert "root node" in tree_badge and "all threads" in tree_badge
    visible_roots = await page.evaluate("() => SELECTORS.getActiveTree().length")
    assert visible_roots >= 16

    # Switch to worker-1
    await page.evaluate("() => UI.sw('worker-1')")
    assert await page.locator('#vt-active-label').inner_text() == 'worker-1'
    w1_nodes = await page.evaluate("() => SELECTORS.getActiveTree().length")
    assert w1_nodes == 1
    await page.evaluate("() => UI.svm('stats')")
    w1_total = await page.locator('#s-nodes').inner_text()
    assert int(w1_total) >= 7

    # Restore all threads
    await page.evaluate("() => UI.sw('all')")
    assert int(await page.locator('#s-nodes').inner_text()) == total_nodes

    # Navigate through all views
    views = ['split', 'gantt', 'tree', 'trace', 'stats', 'graph', '3d']
    for vm in views:
        await page.evaluate(f"() => UI.svm('{vm}')")

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_graphify_offline_fallback(blank_page):
    """When D3 CDN is blocked/offline, Graphify gracefully renders native SVG dependency graph and histogram without errors."""
    page = blank_page
    await page.route("**/cdn.jsdelivr.net/**", lambda route: route.abort())

    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#res .res-split')).to_be_visible(timeout=15000)

    # Graph tab SVG
    await page.evaluate("() => UI.svm('graph')")
    svg = page.locator('#d3-graph-canvas-container svg')
    await expect(svg).to_be_visible(timeout=5000)
    assert await page.locator('#d3-graph-canvas-container .graph-node').count() > 0

    # Histogram modal offline fallback
    await page.evaluate("""() => {
        GRAPHIFY.showHistogramModal({
            ruleName: 'HTTP Request',
            count: 7,
            p95: 850,
            durations: [50, 120, 150, 200, 310, 420, 850],
            color: '#f0883e'
        });
    }""")
    hist_modal = page.locator('#hist-large-modal')
    await expect(hist_modal).to_be_visible()
    hist_svg = page.locator('#large-hist-chart svg')
    await expect(hist_svg).to_be_visible()
    assert await hist_svg.locator('rect').count() > 0

    await hist_modal.locator('.m-hdr button').click()
    await page.unroute("**/cdn.jsdelivr.net/**")
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_core_forensic_pills_and_hotkeys(page_with_data):
    """Core forensic views group must contain Split, Timeline, Tree, Traces without option symbol badges."""
    page = page_with_data

    core_group = page.locator('.vt-core-group')
    await expect(core_group).to_be_visible()

    # Split
    split_pill = page.locator('.vt-core-group .vt[data-v="split"]')
    await expect(split_pill).to_be_visible()
    tip = (await split_pill.get_attribute('data-tip')) or (await split_pill.get_attribute('title')) or ''
    assert 'Alt+1' in tip or '1' in tip

    # Timeline (gantt)
    timeline_pill = page.locator('.vt-core-group .vt[data-v="gantt"]')
    await expect(timeline_pill).to_be_visible()
    tip = (await timeline_pill.get_attribute('data-tip')) or (await timeline_pill.get_attribute('title')) or ''
    assert 'Alt+2' in tip or '2' in tip

    # Tree
    tree_pill = page.locator('.vt-core-group .vt[data-v="tree"]')
    await expect(tree_pill).to_be_visible()
    tip = (await tree_pill.get_attribute('data-tip')) or (await tree_pill.get_attribute('title')) or ''
    assert 'Alt+3' in tip or '3' in tip

    # Traces
    traces_pill = page.locator('.vt-core-group .vt[data-v="trace"]')
    await expect(traces_pill).to_be_visible()
    tip = (await traces_pill.get_attribute('data-tip')) or (await traces_pill.get_attribute('title')) or ''
    assert 'Alt+4' in tip or '4' in tip

    # Ensure no option symbol badges are rendered in top bar navigation
    hotkeys = page.locator('.vt-core-group .vt-hotkey')
    count = await hotkeys.count()
    assert count == 0, f'Expected 0 .vt-hotkey elements on top bar, found {count}'

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

    # Ensure no duplicate inner box or border: button has transparent background and zero border width
    btn_styles = await dropdown_btn.evaluate("""el => {
        const style = window.getComputedStyle(el);
        return {
            bg: style.backgroundColor,
            borderWidth: style.borderWidth
        };
    }""")
    assert btn_styles['borderWidth'] == '0px', f"Expected zero border width (no inner box), got {btn_styles['borderWidth']}"
    assert btn_styles['bg'] in ('rgba(0, 0, 0, 0)', 'transparent'), f"Expected transparent background, got {btn_styles['bg']}"

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
    """Cross-platform keyboard shortcuts must cleanly switch views via Alt+keys, direct number keys, and Mac Option keys."""
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

    # Direct number keys (when not in an input)
    await page.keyboard.press('1')
    await page.wait_for_timeout(200)
    assert await page.evaluate("() => S.viewMode") == 'split'

    await page.keyboard.press('2')
    await page.wait_for_timeout(200)
    assert await page.evaluate("() => S.viewMode") == 'gantt'

    await page.keyboard.press('3')
    await page.wait_for_timeout(200)
    assert await page.evaluate("() => S.viewMode") == 'tree'

    await page.keyboard.press('4')
    await page.wait_for_timeout(200)
    assert await page.evaluate("() => S.viewMode") == 'trace'

    # Mac Option key simulation (Option+1 emits '¡', Option+2 emits '™')
    await page.evaluate("""() => {
        document.dispatchEvent(new KeyboardEvent('keydown', { key: '¡', code: 'Digit1', altKey: true, bubbles: true }));
    }""")
    await page.wait_for_timeout(200)
    assert await page.evaluate("() => S.viewMode") == 'split'

    await page.evaluate("""() => {
        document.dispatchEvent(new KeyboardEvent('keydown', { key: '™', code: 'Digit2', altKey: true, bubbles: true }));
    }""")
    await page.wait_for_timeout(200)
    assert await page.evaluate("() => S.viewMode") == 'gantt'

    # Verify Help & Documentation contains shortcuts section
    hlp_btn = page.locator('#btn-hdr-hlp')
    await hlp_btn.click()
    await page.wait_for_timeout(300)

    # Click shortcuts tab in Help
    shortcuts_tab = page.locator('.hlp-tab[data-hlp="shortcuts"]')
    await expect(shortcuts_tab).to_be_visible()
    await shortcuts_tab.click()
    await page.wait_for_timeout(200)

    hlp_shortcuts = page.locator('#hlp-shortcuts')
    await expect(hlp_shortcuts).to_be_visible()
    content = await hlp_shortcuts.text_content()
    assert 'Split view' in content
    assert 'Timeline view' in content
    assert 'Tree view' in content
    assert 'Traces view' in content
    assert 'Focus Mode' in content or 'focus mode' in content.lower()

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_stat_cards_exclusive_to_stats_view(page_with_data):
    """Stat cards (#stats-bar and #res-summary-cards) must only appear in Stats view, not across other views."""
    page = page_with_data
    for vm in ['split', 'gantt', 'tree', 'trace', 'graph']:
        await page.evaluate(f"() => UI.svm('{vm}')")
        await page.wait_for_timeout(100)
        assert not await page.evaluate("() => !!document.getElementById('stats-bar')"), f"#stats-bar should not be in {vm}"
        assert not await page.evaluate("() => !!document.getElementById('res-summary-cards')"), f"#res-summary-cards should not be in {vm}"

    # Stats view must show both
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(200)
    await expect(page.locator('#stats-bar')).to_be_visible()
    await expect(page.locator('#res-summary-cards')).to_be_visible()
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_stat_cards_reappear_when_returning_from_graph(page_with_data):
    """Switching from Graph view back to Stats view must reliably re-render stat cards without disappearing."""
    page = page_with_data
    # 1. Start in stats view
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(200)
    await expect(page.locator('#stats-bar')).to_be_visible()

    # 2. Go to graph view
    await page.evaluate("() => UI.svm('graph')")
    await page.wait_for_timeout(200)
    assert not await page.evaluate("() => !!document.getElementById('stats-bar')")

    # 3. Return to stats view
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(200)
    await expect(page.locator('#stats-bar')).to_be_visible()
    await expect(page.locator('#res-summary-cards')).to_be_visible()
    assert_no_critical_errors(page)
