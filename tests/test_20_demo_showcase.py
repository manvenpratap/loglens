"""
test_20_demo_showcase.py — LogLens Regression Suite
Tests: Comprehensive demo showcase validation covering all core features:
- Distributed Tracing (Trace Explorer, cross-thread spans, correlationId)
- Multiline Block Payloads (printed class, JSON webhook, SQL exception with Caused by)
- SLA Thresholds & Breach Detection (#hdr-sla badge, node breach flags)
- Latency Outlier & Anomaly Detection (#hdr-outliers badge, IQR calculation)
- Sticky Notes / Annotations pre-seeding (S.annotations, tree note badges)
- Multi-thread execution (16 threads across microservices, all threads aggregation)
- Offline Graphify SVG fallback
Consolidated for high-speed regression verification.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_demo_showcase_data_integrity(blank_page):
    """Demo loads 16 threads with traces, multiline payloads, SLAs, outliers, and sticky notes."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#ob-ov')).to_be_hidden(timeout=15000)
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=15000)

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
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=15000)

    # All-thread tree aggregation
    assert await page.evaluate("() => S.activeThr") == 'all'
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
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=15000)

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
    assert_no_critical_errors(page)
