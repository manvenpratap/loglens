"""
test_07_trace_explorer.py — LogLens Regression Suite
Tests: Trace Explorer view (Alt+7), metric cards, row listing, search filter,
       active-trace selection, Event Inspector auto-open, filter clear.
Covers Phase 6 (Trace Explorer).
"""
import pytest
from playwright.async_api import expect

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
async def test_traces_view_opens_via_alt7(blank_page):
    """Alt+7 must switch the active view to 'trace'."""
    page = blank_page
    await page.evaluate(INJECT_TRACE_JS, TRACE_TREES)
    await page.wait_for_timeout(500)

    await page.keyboard.press('Alt+7')
    await page.wait_for_timeout(400)

    active = page.locator('.vt.active')
    tab_v = await active.evaluate("el => el.dataset.v")
    assert tab_v == 'trace', f'Expected trace view, got {tab_v}'


@pytest.mark.asyncio
async def test_traces_metric_cards_rendered(blank_page):
    """Exactly 3 .trace-metric-card elements must render."""
    page = blank_page
    await page.evaluate(INJECT_TRACE_JS, TRACE_TREES)
    await page.wait_for_timeout(500)
    await page.keyboard.press('Alt+7')
    await page.wait_for_timeout(400)

    count = await page.locator('.trace-metric-card').count()
    assert count == 3, f'Expected 3 metric cards, got {count}'


@pytest.mark.asyncio
async def test_traces_row_count(blank_page):
    """Exactly 2 trace rows must render (one per unique correlationId)."""
    page = blank_page
    await page.evaluate(INJECT_TRACE_JS, TRACE_TREES)
    await page.wait_for_timeout(500)
    await page.keyboard.press('Alt+7')
    await page.wait_for_timeout(400)

    count = await page.locator('.trace-row-item').count()
    assert count == 2, f'Expected 2 trace rows, got {count}'


@pytest.mark.asyncio
async def test_traces_search_filters_rows(blank_page):
    """Typing 'TX-998877' into trace search must filter to 1 row."""
    page = blank_page
    await page.evaluate(INJECT_TRACE_JS, TRACE_TREES)
    await page.wait_for_timeout(500)
    await page.keyboard.press('Alt+7')
    await page.wait_for_timeout(400)

    await page.locator('#trace-search-input').fill('TX-998877')
    await page.wait_for_timeout(300)
    count = await page.locator('.trace-row-item').count()
    assert count == 1, f'Expected 1 filtered row, got {count}'


@pytest.mark.asyncio
async def test_traces_row_click_marks_active(blank_page):
    """Clicking a trace row must add .active-trace class and update S.activeTraceId."""
    page = blank_page
    await page.evaluate(INJECT_TRACE_JS, TRACE_TREES)
    await page.wait_for_timeout(500)
    await page.keyboard.press('Alt+7')
    await page.wait_for_timeout(400)

    row = page.locator('.trace-row-item:has-text("TX-998877")')
    await row.click()
    await page.wait_for_timeout(400)

    is_active = await row.evaluate("el => el.classList.contains('active-trace')")
    assert is_active, 'Clicked row should have .active-trace class'

    active_id = await page.evaluate("S.activeTraceId")
    assert active_id == 'TX-998877', f'S.activeTraceId should be TX-998877, got {active_id}'


@pytest.mark.asyncio
async def test_traces_row_click_opens_inspector(blank_page):
    """Clicking a trace row must auto-open the Event Inspector."""
    page = blank_page
    await page.evaluate(INJECT_TRACE_JS, TRACE_TREES)
    await page.wait_for_timeout(500)
    await page.keyboard.press('Alt+7')
    await page.wait_for_timeout(400)

    await page.locator('.trace-row-item:has-text("TX-998877")').click()
    await page.wait_for_timeout(400)

    await expect(page.locator('#event-inspector')).to_be_visible(timeout=3000)


@pytest.mark.asyncio
async def test_traces_inspector_shows_slowest_event(blank_page):
    """Inspector body must mention the trace's slowest event (Get User)."""
    page = blank_page
    await page.evaluate(INJECT_TRACE_JS, TRACE_TREES)
    await page.wait_for_timeout(500)
    await page.keyboard.press('Alt+7')
    await page.wait_for_timeout(400)

    await page.locator('.trace-row-item:has-text("TX-998877")').click()
    await page.wait_for_timeout(400)

    body = await page.locator('#ins-body-content').text_content()
    assert 'Get User' in body, f'Inspector should mention "Get User", got: {body[:200]}'


@pytest.mark.asyncio
async def test_traces_clear_filter_button(blank_page):
    """Clicking 'Clear Active Filter' must reset S.activeTraceId to null."""
    page = blank_page
    await page.evaluate(INJECT_TRACE_JS, TRACE_TREES)
    await page.wait_for_timeout(500)
    await page.keyboard.press('Alt+7')
    await page.wait_for_timeout(400)

    await page.locator('.trace-row-item:has-text("TX-998877")').click()
    await page.wait_for_timeout(300)

    await page.click('button:has-text("Clear Active Filter")')
    await page.wait_for_timeout(300)

    active_id = await page.evaluate("S.activeTraceId")
    assert active_id is None, f'S.activeTraceId should be null after clear, got {active_id}'
