"""
test_20_demo_showcase.py — LogLens Regression Suite
Tests: Comprehensive demo showcase validation covering all core features:
- Distributed Tracing (Trace Explorer, cross-thread spans, correlationId)
- Multiline Block Payloads (printed class, JSON webhook, SQL exception with Caused by)
- SLA Thresholds & Breach Detection (#hdr-sla badge, node breach flags)
- Latency Outlier & Anomaly Detection (#hdr-outliers badge, IQR calculation)
- Sticky Notes / Annotations pre-seeding (S.annotations, tree note badges)
- Multi-thread execution (16 threads across microservices)
"""
import pytest
from playwright.async_api import expect
from conftest import APP_URL, assert_no_critical_errors


@pytest.mark.asyncio
async def test_demo_load_multi_thread_and_trees(blank_page):
    """Clicking Try Demo populates trees across 16 threads and renders stats bar."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#ob-ov')).to_be_hidden(timeout=15000)
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=15000)

    # Check threads and trees in global state
    threads_count = await page.evaluate("() => S.threads.length")
    assert threads_count >= 16, f"Expected at least 16 threads, got {threads_count}"

    w1_trees = await page.evaluate("() => S.trees['worker-1']?.length")
    assert w1_trees > 0, "worker-1 tree must have root nodes"

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_demo_distributed_tracing(blank_page):
    """Demo includes distributed traces linking multiple threads with correlationId."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=15000)

    # Scan traces via TRACE_EXPLORER
    traces = await page.evaluate("() => TRACE_EXPLORER.scanTraces()")
    assert len(traces) >= 3, f"Expected at least 3 traces, got {len(traces)}"

    # Find checkout trace
    checkout_trace = next((t for t in traces if t.get('id') == 'trace-ord-8921'), None)
    assert checkout_trace is not None, "trace-ord-8921 must exist in demo"
    assert len(checkout_trace.get('threads', [])) == 3, "trace-ord-8921 must span worker-1, worker-2, and worker-3"
    assert set(checkout_trace.get('threads', [])) == {'worker-1', 'worker-2', 'worker-3'}

    # Switch to trace view and verify list rendered
    await page.evaluate("() => UI.svm('trace')")
    await page.wait_for_timeout(300)
    trace_items = page.locator('.trace-row-item')
    count = await trace_items.count()
    assert count >= 3, f"Expected at least 3 trace row items in Trace Explorer, got {count}"

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_demo_multiline_block_payloads(blank_page):
    """Demo includes printed classes, formatted JSON, and SQL exception stack traces with Caused by."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=15000)

    # 1. Printed Class Block on worker-1 /api/checkout
    w1_req_payload = await page.evaluate("""() => {
        const root = S.trees['worker-1'][0];
        const req = root.events.find(e => e.elementName === '/api/checkout');
        return req ? req.payload : null;
    }""")
    assert w1_req_payload is not None, "Expected /api/checkout node in worker-1"
    assert "class OrderCheckoutRequest {" in w1_req_payload, "Payload must contain printed class header"
    assert 'customerId: "cust-9481"' in w1_req_payload, "Payload must contain class properties"
    assert 'paymentMethod: "CREDIT_CARD"' in w1_req_payload, "Payload must contain enum value"

    # 2. Formatted JSON Webhook on worker-2 /api/payment/charge
    w2_charge_payload = await page.evaluate("""() => {
        const root = S.trees['worker-2'][0];
        const req = root.events.find(e => e.elementName === '/api/payment/charge');
        return req ? req.payload : null;
    }""")
    assert w2_charge_payload is not None, "Expected /api/payment/charge node in worker-2"
    assert '"event": "charge.initiated"' in w2_charge_payload, "Payload must contain formatted JSON keys"
    assert '"gateway": "stripe"' in w2_charge_payload, "Payload must contain stripe gateway"

    # 3. Multiline SQL Exception Stack Trace with Caused by on worker-2 OrderService Error
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
    assert w2_err_payload is not None, "Expected Error node in worker-2 RefundOrder"
    assert "java.sql.SQLException: Deadlock detected" in w2_err_payload, "Payload must contain SQL exception"
    assert "Caused by: com.mysql.cj.exceptions.DeadlockException" in w2_err_payload, "Payload must preserve Caused by chain"

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_demo_sla_and_outliers_detection(blank_page):
    """Demo triggers SLA breach detection and IQR latency outlier detection with header badges."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=15000)

    # Check SLA breach count and outlier count in state
    sla_count = await page.evaluate("() => S.slaBreachCount")
    outlier_count = await page.evaluate("() => S.outlierCount")
    assert sla_count >= 2, f"Expected at least 2 SLA breaches, got {sla_count}"
    assert outlier_count >= 2, f"Expected at least 2 outliers, got {outlier_count}"

    # Verify header badges are visible
    sla_badge = page.locator('#hdr-sla')
    await expect(sla_badge).to_be_visible()
    sla_text = await sla_badge.locator('.txt').inner_text()
    assert "SLA" in sla_text

    outlier_badge = page.locator('#hdr-outliers')
    await expect(outlier_badge).to_be_visible()
    outlier_text = await outlier_badge.locator('.txt').inner_text()
    assert "outlier" in outlier_text.lower()

    # Verify slow database lock node breached SLA (>150ms limit)
    is_breach = await page.evaluate("""() => {
        const root = S.trees['worker-2'][1];
        function findNode(nodes, name) {
            for (const n of nodes) {
                if (n.elementName === name) return n;
                if (n.events?.length) {
                    const found = findNode(n.events, name);
                    if (found) return found;
                }
            }
            return null;
        }
        const db = findNode([root], 'order.lock');
        return db ? { dur: db.duration, breach: db._isSlaBreach, outlier: db._isOutlier } : null;
    }""")
    assert is_breach is not None
    assert is_breach['dur'] == 850
    assert is_breach['breach'] is True
    assert is_breach['outlier'] is True

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_demo_sticky_notes_seeded(blank_page):
    """Demo pre-seeds sticky notes / annotations on critical events."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=15000)

    # Verify S.annotations has pre-seeded entries
    ann_keys = await page.evaluate("() => Object.keys(S.annotations || {})")
    assert len(ann_keys) >= 2, f"Expected at least 2 pre-seeded annotations, got {len(ann_keys)}"

    # Switch to tree view on worker-2 where annotated error is located
    await page.evaluate("() => { UI.sw('worker-2'); UI.svm('tree'); }")
    await page.wait_for_timeout(300)

    # Verify sticky note badge is rendered
    note_badges = page.locator('.tnt')
    count = await note_badges.count()
    assert count >= 1, f"Expected at least 1 note badge in worker-2 tree view, got {count}"

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_demo_views_navigation_and_graphify(blank_page):
    """User can navigate through Split, Gantt, Tree, Trace, Stats, Graph, and 3D views without errors."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=15000)

    views = ['split', 'gantt', 'tree', 'trace', 'stats', 'graph', '3d']
    for vm in views:
        await page.evaluate(f"() => UI.svm('{vm}')")
        await page.wait_for_timeout(200)

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_graphify_offline_fallback(blank_page):
    """When D3 CDN is blocked/offline, Graphify gracefully renders native SVG dependency graph and histogram without errors."""
    page = blank_page

    # Block external CDN requests to simulate offline air-gapped environment
    await page.route("**/cdn.jsdelivr.net/**", lambda route: route.abort())

    # Load demo
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=15000)

    # Navigate to Graph tab
    await page.evaluate("() => UI.svm('graph')")
    await page.wait_for_timeout(500)

    # Verify native SVG graph rendered
    svg = page.locator('#d3-graph-canvas-container svg')
    await expect(svg).to_be_visible(timeout=5000)

    node_count = await page.locator('#d3-graph-canvas-container .graph-node').count()
    assert node_count > 0, f"Expected native SVG graph nodes rendered, got {node_count}"

    # Verify histogram modal offline fallback
    await page.evaluate("""() => {
        GRAPHIFY.showHistogramModal({
            ruleName: 'HTTP Request',
            count: 7,
            p95: 850,
            durations: [50, 120, 150, 200, 310, 420, 850],
            color: '#f0883e'
        });
    }""")
    await page.wait_for_timeout(300)
    hist_modal = page.locator('#hist-large-modal')
    await expect(hist_modal).to_be_visible()
    hist_svg = page.locator('#large-hist-chart svg')
    await expect(hist_svg).to_be_visible()
    hist_rects = await hist_svg.locator('rect').count()
    assert hist_rects > 0, "Expected histogram bucket rects rendered in offline mode"

    # Close modal
    await hist_modal.locator('.m-hdr button').click()

    # Assert no critical runtime or console errors occurred
    assert_no_critical_errors(page)

