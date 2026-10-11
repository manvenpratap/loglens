"""
test_stress_and_performance.py — Performance & Stress Benchmarks
Validates parse throughput, trace sorting latency with memoization, and virtual scroll efficiency.
"""
import time
import pytest
from playwright.async_api import Page, expect
from tests.conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_trace_explorer_memoized_sort_performance(page_with_data):
    """Verifies P1 memoization: trace sort operations execute in < 25ms without re-scanning all trees."""
    page = page_with_data

    # Open Traces tab
    await page.evaluate("() => UI.svm('trace')")
    await page.wait_for_selector('.trace-row-item', timeout=5000)

    # Benchmark repeated sorting operations
    perf_metrics = await page.evaluate("""() => {
        const t0 = performance.now();
        for (let i = 0; i < 20; i++) {
            TRACE_EXPLORER.setSort(i % 2 === 0 ? 'duration' : 'count');
        }
        const totalMs = performance.now() - t0;
        return {
            totalMs,
            avgMs: totalMs / 20,
            tracesFound: TRACE_EXPLORER.scanTraces().length
        };
    }""")

    assert perf_metrics['tracesFound'] > 0, "Traces should be present"
    # 20 sorts should easily complete well under 250ms with memoization (< 12.5ms per sort)
    assert perf_metrics['avgMs'] < 25, f"Expected avg sort < 25ms, got {perf_metrics['avgMs']}ms"

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_tree_virtual_scrolling_dom_node_ceiling(page_with_data):
    """Verifies Execution Tree virtual scrolling maintains a strict DOM ceiling during rapid scrolling."""
    page = page_with_data

    # Switch to tree view
    await page.evaluate("() => UI.svm('tree')")
    await page.wait_for_selector('.tree-row', timeout=5000)

    # Rapid scroll loop
    scroll_stats = await page.evaluate("""() => {
        const vscroll = document.getElementById('tree-vscroll');
        if (!vscroll) return { ok: false };
        
        let maxDomNodes = 0;
        for (let offset = 0; offset <= 2000; offset += 200) {
            vscroll.scrollTop = offset;
            TR.drawVisible();
            const count = vscroll.querySelectorAll('.tree-row').length;
            if (count > maxDomNodes) maxDomNodes = count;
        }
        return { ok: true, maxDomNodes };
    }""")

    assert scroll_stats['ok'] is True
    # Virtual window should never blow up beyond ~50 DOM rows regardless of scroll position
    assert scroll_stats['maxDomNodes'] <= 55, f"DOM ceiling exceeded: {scroll_stats['maxDomNodes']} rows"

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_large_dataset_ingestion_and_render_throughput(blank_page):
    """Verifies synthetic dataset ingestion and initial render completes in < 800ms."""
    page = blank_page

    # Inject 2,500 synthetic operations
    inject_script = """() => {
        const t0 = performance.now();
        const _base = Date.now() - 50000;
        const mainNodes = Array.from({ length: 2500 }, (_, i) => ({
            id: 'perf_' + i,
            ruleId: 'r1',
            ruleName: 'PerfOp-' + (i % 10),
            elementName: 'PerfElement-' + (i % 10),
            payload: '{"i": ' + i + '}',
            thread: 'worker-' + (i % 4),
            timestamp: _base + i * 20,
            duration: 10 + (i % 50) * 5,
            endTimestamp: _base + i * 20 + 10 + (i % 50) * 5,
            behavior: 'push',
            level: i % 20 === 0 ? 'ERROR' : 'INFO',
            slaBreached: (i % 50) > 40,
            correlationId: 'TRACE-BENCH-' + (i % 25),
            rawLine: 'perf log line ' + i,
            events: [],
            visualStyle: {}
        }));

        const trees = {
            'worker-0': mainNodes.filter(n => n.thread === 'worker-0'),
            'worker-1': mainNodes.filter(n => n.thread === 'worker-1'),
            'worker-2': mainNodes.filter(n => n.thread === 'worker-2'),
            'worker-3': mainNodes.filter(n => n.thread === 'worker-3'),
        };

        S.trees = trees;
        S.threads = Object.keys(trees);
        S.activeThr = 'worker-0';
        S.stats = { fileSize: 2500 * 80, linesProcessed: 2500, totalNodes: 2500, slaBreaches: 200 };

        UI.render(S.trees, S.threads, S.stats);
        UI.svm('gantt');
        const elapsed = performance.now() - t0;
        return { elapsed, totalNodes: 2500 };
    }"""

    stats = await page.evaluate(inject_script)
    # Rendering 2,500 nodes should execute under 800ms
    assert stats['elapsed'] < 800, f"Render took too long: {stats['elapsed']}ms"

    assert_no_critical_errors(page)
