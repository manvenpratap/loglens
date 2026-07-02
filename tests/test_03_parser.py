"""
test_03_parser.py — LogLens Regression Suite
Tests: Stack behavior engine (push/inline/swap/popAll), multi-thread parsing.
Covers parser correctness — the core WM.parse pipeline.
"""
import json
import pytest
from playwright.async_api import expect

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
