"""
test_consolidated_parser_and_ingestion.py — Consolidated Regression Test Suite
Merges and deduplicates tests from: test_03_parser.py, test_12_log4j_import.py, test_14_unparsed_analyzer.py, test_19_multiline_block_payload.py
"""
import os
import re
import json
import tempfile
import pytest
import asyncio
from playwright.async_api import expect, Page
from conftest import APP_URL, DISMISS_ONBOARDING_JS, DEMO_TREES_JS, assert_no_critical_errors

LOG_CONTENT = (
    "2026-07-01 10:00:00.000 [thread-1] START - Tx1 start\n"
    "2026-07-01 10:00:01.000 [thread-1] STEP - Step 1\n"
    "2026-07-01 10:00:02.000 [thread-1] SWAP - Tx2 start\n"
    "2026-07-01 10:00:03.000 [thread-1] STEP - Step 2\n"
    "2026-07-01 10:00:04.000 [thread-1] CLEAR - Reset all\n"
    "2026-07-01 10:00:05.000 [thread-1] STEP - Step 3\n"
)
CUSTOM_CFG = {
    "id": "test-config",
    "name": "Test Configuration",
    "elementRules": [
        {
            "id": "r-start", "name": "Start",
            "regexPattern": r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[([^\]]+)\] START - (.*)$",
            "captureMapping": {"1": "timestamp", "2": "thread", "3": "elementName"},
            "stackBehavior": "push", "enabled": True
        },
        {
            "id": "r-step", "name": "Step",
            "regexPattern": r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[([^\]]+)\] STEP - (.*)$",
            "captureMapping": {"1": "timestamp", "2": "thread", "3": "elementName"},
            "stackBehavior": "inline", "enabled": True
        },
        {
            "id": "r-swap", "name": "Swap",
            "regexPattern": r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[([^\]]+)\] SWAP - (.*)$",
            "captureMapping": {"1": "timestamp", "2": "thread", "3": "elementName"},
            "stackBehavior": "swap", "enabled": True
        },
        {
            "id": "r-clear", "name": "Clear",
            "regexPattern": r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[([^\]]+)\] CLEAR - (.*)$",
            "captureMapping": {"1": "timestamp", "2": "thread", "3": "elementName"},
            "stackBehavior": "popAll", "enabled": True
        }
    ]
}
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
async def test_parser_push_behavior(blank_page):
    """Push node must have correct name, duration, and child count."""
    page = blank_page
    result = await page.evaluate("""
        async (args) => {
            const file = new File([args.log], 'test.log', {type:'text/plain'});
            return await WM.parse(file, args.cfg, '');
        }
    """, {"log": LOG_CONTENT, "cfg": CUSTOM_CFG})

    tree = result.get('trees', {}).get('thread-1', [])
    assert len(tree) == 4, f'Expected 4 top-level nodes, got {len(tree)}'

    n1 = tree[0]
    assert n1['elementName'] == 'Tx1 start'
    assert n1['behavior'] == 'push'
    assert n1['duration'] == 2000, f'Expected 2000ms, got {n1["duration"]}'
    assert len(n1['events']) == 1
    assert n1['events'][0]['elementName'] == 'Step 1'
@pytest.mark.asyncio
async def test_parser_swap_behavior(blank_page):
    """Swap node must replace push node, inherit timing, and contain child."""
    page = blank_page
    result = await page.evaluate("""
        async (args) => {
            const file = new File([args.log], 'test.log', {type:'text/plain'});
            return await WM.parse(file, args.cfg, '');
        }
    """, {"log": LOG_CONTENT, "cfg": CUSTOM_CFG})

    tree = result.get('trees', {}).get('thread-1', [])
    n2 = tree[1]
    assert n2['elementName'] == 'Tx2 start'
    assert n2['behavior'] == 'swap'
    assert n2['duration'] == 2000
    assert len(n2['events']) == 1
    assert n2['events'][0]['elementName'] == 'Step 2'
@pytest.mark.asyncio
async def test_parser_popall_behavior(blank_page):
    """popAll node must have no duration (stack cleared immediately)."""
    page = blank_page
    result = await page.evaluate("""
        async (args) => {
            const file = new File([args.log], 'test.log', {type:'text/plain'});
            return await WM.parse(file, args.cfg, '');
        }
    """, {"log": LOG_CONTENT, "cfg": CUSTOM_CFG})

    tree = result.get('trees', {}).get('thread-1', [])
    n3 = tree[2]
    assert n3['elementName'] == 'Reset all'
    assert n3['behavior'] == 'popAll'
    assert n3['duration'] is None
@pytest.mark.asyncio
async def test_parser_inline_at_root(blank_page):
    """Inline node after popAll should appear at root level."""
    page = blank_page
    result = await page.evaluate("""
        async (args) => {
            const file = new File([args.log], 'test.log', {type:'text/plain'});
            return await WM.parse(file, args.cfg, '');
        }
    """, {"log": LOG_CONTENT, "cfg": CUSTOM_CFG})

    tree = result.get('trees', {}).get('thread-1', [])
    n4 = tree[3]
    assert n4['elementName'] == 'Step 3'
    assert n4['behavior'] == 'inline'
@pytest.mark.asyncio
async def test_log4j_import_inline_and_empty_config(blank_page):
    """
    Importing a log4j XML file in an empty configuration state must:
    1. Populate the inline `#lj-res` container under the import button.
    2. Auto-initialize S.cfg with defaults if currently null.
    3. Import the selected appenders successfully and update the rules view.
    """
    page = blank_page

    # 1. Dismiss onboarding via the skip button
    btn_skip = page.locator('#ob-skip')
    await expect(btn_skip).to_be_visible()
    await btn_skip.click()
    await page.wait_for_timeout(300)

    # Navigate to Settings view
    await page.click('.vt[data-v="cfg"]')
    await page.wait_for_timeout(300)

    # Verify that the Settings panel is visible
    p_cfg = page.locator('#p-cfg')
    await expect(p_cfg).to_be_visible()

    # Verify that S.cfg is indeed null initially on blank page
    cfg_val = await page.evaluate("() => S.cfg")
    assert cfg_val is None, "S.cfg should be null initially on a blank page"

    # Verify that the Add Rule button is enabled initially
    btn_ar = page.locator('#btn-ar')
    await expect(btn_ar).not_to_be_disabled()

    # 2. Create a temporary log4j XML file
    xml_content = """<log4j:configuration xmlns:log4j="http://jakarta.apache.org/log4j/">
    <appender name="my_console_appender" class="org.apache.log4j.ConsoleAppender">
        <layout class="org.apache.log4j.PatternLayout">
            <param name="ConversionPattern" value="%d{yyyy-MM-dd HH:mm:ss,SSS} %-5p [%t] %c - %m%n"/>
        </layout>
    </appender>
</log4j:configuration>"""

    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
        f.write(xml_content.encode('utf-8'))
        temp_xml_path = f.name

    try:
        # 3. Simulate clicking the "Import XML Config File" button and uploading the file
        async with page.expect_file_chooser() as fc_info:
            await page.click("#btn-lj-imp")
        file_chooser = await fc_info.value
        await file_chooser.set_files(temp_xml_path)

        # 4. Assert that `#lj-res` is visible and populated inline
        lj_res = page.locator('#lj-res')
        await expect(lj_res).to_be_visible(timeout=5000)

        # Check text content in inline result area
        text_content = await lj_res.text_content()
        assert "Found 1 appender" in text_content
        assert "my_console_appender" in text_content

        # 5. Click the "Preview & Import" button
        btn_show_sh = page.locator('#btn-show-sh')
        await expect(btn_show_sh).to_be_visible()
        await btn_show_sh.click()

        # 6. Verify that the sheet overlay modal `#sh-ov` opens (remove hidden class)
        sh_ov = page.locator('#sh-ov')
        await expect(sh_ov).to_have_class("sh-ov")

        # 7. Click the "Import Selected" button
        btn_shi = page.locator('#btn-shi')
        await expect(btn_shi).to_be_visible()
        await btn_shi.click()

        # 8. Assert that the sheet modal is closed/hidden
        await expect(sh_ov).to_have_class("sh-ov hidden")

        # 9. Verify S.cfg is now loaded and contains the new rule
        cfg_loaded = await page.evaluate("() => S.cfg !== null")
        assert cfg_loaded, "S.cfg should have been initialized from defaults"

        rules_count = await page.evaluate("() => S.cfg.elementRules.length")
        # Should contain default rules + 1 imported appender rule
        assert rules_count > 0, "Rules should be loaded into state"

        # Check that the custom appender rule name exists
        has_imported_rule = await page.evaluate(
            "() => S.cfg.elementRules.some(r => r.name.includes('my_console_appender'))"
        )
        assert has_imported_rule, "State should contain the imported appender rule"

        # 10. Verify that `#btn-ar` is now enabled
        await expect(btn_ar).not_to_be_disabled()

        # Check for any console/JS errors
        assert_no_critical_errors(page)

    finally:
        # Cleanup
        if os.path.exists(temp_xml_path):
            os.remove(temp_xml_path)
async def _load_settings_with_unparsed_data(page):
    """Helper: open the Settings tab and inject unparsed log samples."""
    await page.evaluate("() => { if (S.cfg === null) CFG.load(JSON.parse(JSON.stringify(DEF_CFG))); }")
    await page.evaluate("""() => {
        S.stats = {
            fileSize: 5000,
            linesProcessed: 10,
            matchedLines: 7,
            unparsedSample: [
                "2026-07-05 10:00:00 [main] ERROR - Database connection timeout",
                "2026-07-05 10:00:01 [main] ERROR - Database connection timeout",
                "2026-07-05 10:00:02 [main] ERROR - Database connection timeout"
            ]
        };
        stats = S.stats;
    }""")
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(500)
@pytest.mark.asyncio
async def test_unparsed_analyzer_create_rule_button(page_with_data):
    """Clicking + Create Rule on unparsed analyzer must populate the rule creator modal correctly."""
    page = page_with_data
    await _load_settings_with_unparsed_data(page)

    # 1. Click "Analyze Unparsed"
    btn_analyze = page.locator('#btn-analyze-unparsed')
    await expect(btn_analyze).to_be_visible()
    await btn_analyze.click()
    await page.wait_for_timeout(500)

    # 2. Check that pattern list is populated
    results = page.locator('#unparsed-results')
    await expect(results).to_contain_text("Top Unparsed Patterns:")
    
    # 3. Locate the "+ Create Rule" button
    btn_create_rule = page.locator('#unparsed-results >> text=+ Create Rule').first
    await expect(btn_create_rule).to_be_visible()

    # 4. Click "+ Create Rule"
    await btn_create_rule.click()
    await page.wait_for_timeout(500)

    # 5. Rule modal must be visible
    modal = page.locator('#mm')
    await expect(modal).not_to_have_class(r"hidden")

    # 6. Advanced option must be checked and e-rx value populated
    use_custom = page.locator('#e-use-custom-rx')
    await expect(use_custom).to_be_checked()

    e_rx = page.locator('#e-rx')
    rx_val = await e_rx.input_value()
    assert len(rx_val) > 0
    assert "^" in rx_val

    # 7. Sample log line (e-tl) must be pre-populated
    e_tl = page.locator('#e-tl')
    tl_val = await e_tl.input_value()
    assert tl_val == "2026-07-05 10:00:00 [main] ERROR - Database connection timeout"

    # Ensure no critical console errors occurred during the flow
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_unparsed_analyzer_100_percent_coverage(page_with_data):
    """When a log has 100% rule coverage (0 unparsed lines), Analyzer displays success rather than false error."""
    page = page_with_data
    # Set up 100% matched state with empty unparsedSample
    await page.evaluate("""() => {
        S.stats = {
            fileSize: 5000,
            linesProcessed: 35,
            matchedLines: 35,
            unparsedSample: []
        };
        UI.svm('cfg');
    }""")
    await page.wait_for_timeout(300)

    btn_analyze = page.locator('#btn-analyze-unparsed')
    await expect(btn_analyze).to_be_visible()
    await btn_analyze.click()
    await page.wait_for_timeout(300)

    results = page.locator('#unparsed-results')
    # Must celebrate 100% coverage and NOT display the error "No unparsed lines to analyze. Parse a log file first."
    await expect(results).to_contain_text("100% rule coverage")
    await expect(results).to_contain_text("Zero unparsed lines detected")
    results_text = await results.inner_text()
    assert "No unparsed lines to analyze. Parse a log file first." not in results_text

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_unparsed_analyzer_when_no_log_parsed(blank_page):
    """When no log file has been parsed yet, Analyzer shows actionable guidance instead of a dead error."""
    page = blank_page
    await page.evaluate("() => { if (typeof ONBOARD !== 'undefined') ONBOARD.dismiss(); UI.svm('cfg'); }")
    await page.wait_for_timeout(300)

    btn_analyze = page.locator('#btn-analyze-unparsed')
    await expect(btn_analyze).to_be_visible()
    await btn_analyze.click()
    await page.wait_for_timeout(300)

    results = page.locator('#unparsed-results')
    await expect(results).to_contain_text("No log file parsed yet")
    await expect(results.locator('button >> text=Select Log File')).to_be_visible()
    await expect(results.locator('button >> text=Load Demo Log')).to_be_visible()

    assert_no_critical_errors(page)
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

    # Verify tree item renders with .tree-payload-btn and clicking reveals the payload in popover
    tree_payload_btn = page.locator('.tree-payload-btn')
    await expect(tree_payload_btn.first).to_be_visible()

    await tree_payload_btn.first.click()
    popover = page.locator('#tree-payload-popover')
    await expect(popover).to_be_visible()
    popover_code = await popover.locator('#tree-payload-code').inner_text()
    assert "class OrderRequest" in popover_code
    assert "private Long orderId" in popover_code

    # Close popover
    await popover.locator('#tree-popover-close-btn').click()
    await expect(popover).not_to_be_attached()

    # Click first tree row to open Event Inspector
    first_row = page.locator('.tree-row').first
    await first_row.click()
    await page.wait_for_timeout(300)

    inspector = page.locator('#event-inspector')
    await expect(inspector).to_be_visible()
    ins_body = await page.locator('#ins-body-content').text_content()
    assert "class OrderRequest" in ins_body
    assert "private Long orderId" in ins_body

    # Verify Event Inspector preserves pre-wrap
    ins_ws = await page.locator('.ins-payload-pre').first.evaluate("el => window.getComputedStyle(el).whiteSpace")
    assert ins_ws == "pre-wrap"

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
