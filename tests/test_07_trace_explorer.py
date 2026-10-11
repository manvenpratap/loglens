"""
test_07_trace_explorer.py — LogLens Regression Suite
Tests: Trace Explorer view (Alt+7), metric cards, row listing, search filter,
       active-trace selection, Event Inspector auto-open, filter clear.
Covers Phase 6 (Trace Explorer).
Consolidated for high-speed regression verification.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors

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
