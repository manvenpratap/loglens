"""
test_19_multiline_block_payload.py — LogLens Regression Suite
Tests: Multiline block payload parsing (classes, objects, stack traces, JSON).
Covers:
  1. Multiline printed class captured as a single payload with indentation preserved.
  2. Exception stack traces and Caused by blocks accumulated into payload.
  3. Multiline JSON / object payload accumulation.
  4. Global setting toggle (multilinePayloads: false) opts out of accumulation.
  5. UI Tree and Event Inspector preserve pre-wrapped multiline payload formatting.
  6. Interleaved lines and subsequent headers cleanly close multiline blocks.
"""
import json
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors, DISMISS_ONBOARDING_JS


SAMPLE_CLASS_LOG = (
    "2026-10-10 10:00:00.100 [main] INFO - Processing OrderRequest payload:\n"
    "class OrderRequest {\n"
    "    private Long orderId = 98765L;\n"
    "    private String customer = \"Acme Corp\";\n"
    "    private Double amount = 1450.50;\n"
    "    private List<Item> items = [\n"
    "        Item(sku=\"SKU-1\", qty=2),\n"
    "        Item(sku=\"SKU-2\", qty=5)\n"
    "    ];\n"
    "    public String toString() { return ...; }\n"
    "}\n"
    "2026-10-10 10:00:01.200 [main] INFO - OrderRequest validated successfully\n"
)

SAMPLE_STACKTRACE_LOG = (
    "2026-10-10 10:05:00.000 [worker-1] ERROR - Database query failed\n"
    "java.sql.SQLException: Connection timed out\n"
    "\tat com.example.db.Pool.getConnection(Pool.java:42)\n"
    "\tat com.example.service.OrderService.save(OrderService.java:115)\n"
    "Caused by: java.net.ConnectException: Connection refused\n"
    "\tat java.net.PlainSocketImpl.socketConnect(Native Method)\n"
    "2026-10-10 10:05:01.000 [worker-1] INFO - Retrying database query\n"
)

SAMPLE_JSON_LOG = (
    "2026-10-10 10:10:00.000 [http-nio-8080] INFO - Received webhook payload:\n"
    "{\n"
    '  "event": "charge.success",\n'
    '  "data": {\n'
    '    "id": "ch_3MvY8",\n'
    '    "amount": 2500\n'
    "  }\n"
    "}\n"
    "2026-10-10 10:10:01.000 [http-nio-8080] INFO - Webhook dispatched\n"
)

TEST_CFG = {
    "id": "test-multiline-cfg",
    "name": "Test Multiline Configuration",
    "globalSettings": {
        "multilinePayloads": True
    },
    "elementRules": [
        {
            "id": "r-info", "name": "Log Entry",
            "regexPattern": r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[([^\]]+)\] (INFO|ERROR) - (.*)$",
            "captureMapping": {"1": "timestamp", "2": "thread", "3": "level", "4": "elementName"},
            "stackBehavior": "inline", "enabled": True
        }
    ]
}


@pytest.mark.asyncio
async def test_multiline_class_parsed_as_single_payload(blank_page):
    """Printed class with multiple lines is captured as a single payload in the parent event."""
    page = blank_page

    result = await page.evaluate("""
        async (args) => {
            const file = new File([args.log], 'order.log', {type:'text/plain'});
            return await WM.parse(file, args.cfg, '');
        }
    """, {"log": SAMPLE_CLASS_LOG, "cfg": TEST_CFG})

    stats = result['stats']
    assert stats['linesProcessed'] == 12
    assert stats['matchedLines'] == 12
    assert len(stats['unparsedSample']) == 0

    tree = result.get('trees', {}).get('main', [])
    assert len(tree) == 2, f"Expected 2 nodes, got {len(tree)}"

    first_node = tree[0]
    assert first_node['elementName'] == "Processing OrderRequest payload:"
    assert first_node['payload'] is not None

    payload = first_node['payload']
    assert "class OrderRequest {" in payload
    assert "private Long orderId = 98765L;" in payload
    assert "Item(sku=\"SKU-1\", qty=2)" in payload
    assert payload.rstrip().endswith("}")

    second_node = tree[1]
    assert second_node['elementName'] == "OrderRequest validated successfully"
    assert second_node['payload'] is None or second_node['payload'] == ""

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_multiline_stack_trace_payload(blank_page):
    """Exception stack trace with Caused by is accumulated into error node payload."""
    page = blank_page

    result = await page.evaluate("""
        async (args) => {
            const file = new File([args.log], 'error.log', {type:'text/plain'});
            return await WM.parse(file, args.cfg, '');
        }
    """, {"log": SAMPLE_STACKTRACE_LOG, "cfg": TEST_CFG})

    stats = result['stats']
    assert stats['matchedLines'] == 7
    assert len(stats['unparsedSample']) == 0

    tree = result.get('trees', {}).get('worker-1', [])
    assert len(tree) == 2

    err_node = tree[0]
    assert err_node['elementName'] == "Database query failed"
    payload = err_node['payload']
    assert "java.sql.SQLException: Connection timed out" in payload
    assert "Caused by: java.net.ConnectException: Connection refused" in payload

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_multiline_json_payload(blank_page):
    """Multiline JSON payload block is captured as a single formatted block."""
    page = blank_page

    result = await page.evaluate("""
        async (args) => {
            const file = new File([args.log], 'webhook.log', {type:'text/plain'});
            return await WM.parse(file, args.cfg, '');
        }
    """, {"log": SAMPLE_JSON_LOG, "cfg": TEST_CFG})

    tree = result.get('trees', {}).get('http-nio-8080', [])
    assert len(tree) == 2

    json_node = tree[0]
    payload = json_node['payload']
    assert '"event": "charge.success"' in payload
    assert '"id": "ch_3MvY8"' in payload

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_multiline_opt_out_setting(blank_page):
    """When multilinePayloads is false, continuation lines are not accumulated into payload."""
    page = blank_page

    opt_out_cfg = dict(TEST_CFG)
    opt_out_cfg["globalSettings"] = {"multilinePayloads": False}

    result = await page.evaluate("""
        async (args) => {
            const file = new File([args.log], 'order.log', {type:'text/plain'});
            return await WM.parse(file, args.cfg, '');
        }
    """, {"log": SAMPLE_CLASS_LOG, "cfg": opt_out_cfg})

    # Only 2 header lines match, 10 continuation lines remain unparsed
    stats = result['stats']
    assert stats['matchedLines'] == 2
    assert len(stats['unparsedSample']) > 0

    tree = result.get('trees', {}).get('main', [])
    first_node = tree[0]
    assert first_node['payload'] is None or first_node['payload'] == ""

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_event_inspector_renders_multiline_payload(blank_page):
    """UI Tree view and Event Inspector render multiline payload with preserved line breaks."""
    page = blank_page

    await page.evaluate(DISMISS_ONBOARDING_JS)

    # Ingest sample class log directly into LogLens
    await page.evaluate("""
        async (args) => {
            const file = new File([args.log], 'order.log', {type:'text/plain'});
            const res = await WM.parse(file, args.cfg, '');
            UI.render(res.trees, res.threads, res.stats);
            UI.svm('tree');
        }
    """, {"log": SAMPLE_CLASS_LOG, "cfg": TEST_CFG})
    await page.wait_for_timeout(300)

    # Verify tree item renders with .tpy payload element
    tree_payload = page.locator('.tpy')
    await expect(tree_payload.first).to_be_visible()
    payload_text = await tree_payload.first.inner_text()
    assert "class OrderRequest" in payload_text
    assert "private Long orderId" in payload_text

    # Verify CSS formatting preserves pre-wrap
    ws = await tree_payload.first.evaluate("el => window.getComputedStyle(el).whiteSpace")
    assert ws == "pre-wrap"

    # Click first tree row to open Event Inspector
    first_row = page.locator('.tree-row').first
    await first_row.click()
    await page.wait_for_timeout(300)

    inspector = page.locator('#event-inspector')
    await expect(inspector).to_be_visible()
    ins_body = await page.locator('#ins-body-content').text_content()
    assert "class OrderRequest" in ins_body
    assert "private Long orderId" in ins_body

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_multiline_interleaved_headers(blank_page):
    """When a new header arrives on any thread, the active multiline block closes cleanly."""
    page = blank_page

    interleaved_log = (
        "2026-10-10 10:20:00.000 [t1] INFO - Start Block 1\n"
        "Line 1 of block 1\n"
        "Line 2 of block 1\n"
        "2026-10-10 10:20:01.000 [t2] INFO - Interleaved event on t2\n"
        "2026-10-10 10:20:02.000 [t1] INFO - Start Block 2\n"
        "Line 1 of block 2\n"
    )

    result = await page.evaluate("""
        async (args) => {
            const file = new File([args.log], 'interleaved.log', {type:'text/plain'});
            return await WM.parse(file, args.cfg, '');
        }
    """, {"log": interleaved_log, "cfg": TEST_CFG})

    stats = result['stats']
    assert stats['matchedLines'] == 6
    assert len(stats['unparsedSample']) == 0

    t1_tree = result.get('trees', {}).get('t1', [])
    assert len(t1_tree) == 2
    assert "Line 1 of block 1" in t1_tree[0]['payload']
    assert "Line 2 of block 1" in t1_tree[0]['payload']
    assert "Line 1 of block 2" in t1_tree[1]['payload']

    t2_tree = result.get('trees', {}).get('t2', [])
    assert len(t2_tree) == 1
    assert t2_tree[0]['elementName'] == "Interleaved event on t2"

    assert_no_critical_errors(page)
