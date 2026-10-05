"""
test_17_auto_detect_and_retention.py — LogLens Regression Suite
Tests: Automatic log pattern sniffing, format detection, rule synthesis,
auto-retention in localStorage, factory reset, and adaptive rescue banner.
"""
import json
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_format_sniff_and_synthesis(blank_page):
    """SNIFFER should detect format patterns and synthesize rules with proper capture mappings and stack behaviors."""
    page = blank_page

    res = await page.evaluate("""() => {
        const sampleLines = [
            '2026-07-01 10:00:00.123 INFO  [main] com.example.OrderService - TX-BEGIN orderId=42',
            '2026-07-01 10:00:01.456 INFO  [main] com.example.OrderService - Processing step',
            '2026-07-01 10:00:02.789 ERROR [main] com.example.OrderService - DB Connection Failed',
            '2026-07-01 10:00:03.012 INFO  [main] com.example.OrderService - TX-END orderId=42'
        ];
        const matchPreset = SNIFFER.detectPreset(sampleLines);
        const synth = SNIFFER.synthesizeRules(sampleLines, 'my-service.log');
        return {
            presetKey: matchPreset?.key,
            presetName: matchPreset?.name,
            rulesCount: synth.config.elementRules.length,
            behaviors: synth.config.elementRules.map(r => r.stackBehavior),
            hasPush: synth.config.elementRules.some(r => r.stackBehavior === 'push'),
            hasPop: synth.config.elementRules.some(r => r.stackBehavior === 'pop'),
            hasInline: synth.config.elementRules.some(r => r.stackBehavior === 'inline')
        };
    }""")

    assert res['presetKey'] == 'java_std'
    assert res['rulesCount'] >= 3
    assert res['hasPush'] is True
    assert res['hasPop'] is True
    assert res['hasInline'] is True
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_rule_auto_retention_in_local_storage(blank_page):
    """Adding or modifying rules should automatically persist the active configuration to localStorage."""
    page = blank_page

    persisted_json = await page.evaluate("""async () => {
        const dummyConfig = {
            globalSettings: { appName: "Retained App" },
            elementRules: [
                {
                    id: "r_custom_1",
                    name: "Custom Retained Rule",
                    regexPattern: "^(.*)$",
                    captureMapping: { "1": "payload" },
                    stackBehavior: "inline",
                    enabled: true
                }
            ]
        };
        CFG.load(dummyConfig, true);
        await CFG.pers();
        return localStorage.getItem('ll-active-cfg');
    }""")

    assert persisted_json is not None
    parsed = json.loads(persisted_json)
    assert parsed['globalSettings']['appName'] == 'Retained App'
    assert len(parsed['elementRules']) == 1
    assert parsed['elementRules'][0]['id'] == 'r_custom_1'

    # Status indicator should show auto-retained
    cfg_txt = page.locator('#cfg-txt')
    await expect(cfg_txt).to_have_text('Auto-retained in browser')
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_retained_config_boot_restoration(blank_page):
    """When the page reloads with a retained configuration in localStorage, it should auto-load without user intervention."""
    page = blank_page

    test_cfg = {
        "globalSettings": { "appName": "Boot Restored App" },
        "elementRules": [
            {
                "id": "r_boot_1",
                "name": "Restored Rule 1",
                "regexPattern": r"^(.*)$",
                "captureMapping": { "1": "payload" },
                "stackBehavior": "inline",
                "enabled": True
            }
        ]
    }

    # Store in localStorage and reload page
    await page.evaluate(f"() => localStorage.setItem('ll-active-cfg', JSON.stringify({json.dumps(test_cfg)}))")
    await page.reload()
    await page.wait_for_timeout(500)

    # Verify that S.cfg is populated and rules list contains the restored rule
    restored_app = await page.evaluate("() => S.cfg?.globalSettings?.appName")
    assert restored_app == "Boot Restored App"

    # Go to settings view and verify rule name is visible
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(300)
    rule_name = page.locator('.rn', has_text='Restored Rule 1')
    await expect(rule_name).to_be_visible()

    cfg_txt = page.locator('#cfg-txt')
    await expect(cfg_txt).to_have_text('Auto-retained in browser')
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_reset_defaults_clears_retention(blank_page):
    """Clicking Reset Defaults in Settings clears retained storage and resets to clean factory defaults."""
    page = blank_page

    # Setup retained config
    await page.evaluate("""async () => {
        const dummyConfig = {
            globalSettings: { appName: "To Be Cleared" },
            elementRules: [{ id: "r_temp", name: "Temp Rule", regexPattern: "^.*$", stackBehavior: "inline" }]
        };
        CFG.load(dummyConfig, true);
        await CFG.pers();
    }""")

    # Accept the confirm dialog automatically
    page.on("dialog", lambda dialog: dialog.accept())

    # Switch to settings and click Reset Defaults
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(300)

    btn_reset = page.locator('#btn-reset-defaults')
    await expect(btn_reset).to_be_visible()
    await btn_reset.click()
    await page.wait_for_timeout(400)

    # Verify localStorage is cleared
    storage_val = await page.evaluate("() => localStorage.getItem('ll-active-cfg')")
    assert storage_val is None

    # Verify rules are reset to defaults
    rules_count = await page.evaluate("() => S.cfg?.elementRules?.length")
    assert rules_count is not None and rules_count > 1
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_adaptive_rescue_banner_and_auto_add(page_with_data):
    """Adaptive rescue banner should display when unparsed lines exceed threshold and allow 1-click rule learning."""
    page = page_with_data

    # Ensure active config exists
    await page.evaluate("() => { if (!S.cfg) CFG.load(JSON.parse(JSON.stringify(DEF_CFG))); }")

    # Simulate parse output with high unparsed lines and unparsed clusters
    await page.evaluate("""() => {
        const dummyStats = {
            fileSize: 5000,
            linesProcessed: 100,
            matchedLines: 40, // 60% unparsed > 15% threshold
            unparsedSample: [
                '2026-07-01 12:00:00 [worker-1] WARN - Queue backlog reached 500 items',
                '2026-07-01 12:00:01 [worker-1] WARN - Queue backlog reached 510 items',
                '2026-07-01 12:00:02 [worker-1] WARN - Queue backlog reached 520 items'
            ]
        };
        SNIFFER.checkUnparsedRescue(dummyStats);
    }""")

    dock = page.locator('#res-top-dock')
    await expect(dock).to_be_visible()

    banner = page.locator('#rescue-banner')
    await expect(banner).to_be_visible()
    await expect(banner).to_contain_text('60% unparsed')
    await expect(banner).to_contain_text('Adaptive Rescue: Unmatched Log Pattern Detected')

    auto_add_btn = page.locator('#btn-rescue-auto')
    await expect(auto_add_btn).to_be_visible()

    # Click + Auto-Add Rule & Retain
    initial_rule_count = await page.evaluate("() => S.cfg?.elementRules?.length || 0")
    await auto_add_btn.click()
    await page.wait_for_timeout(300)

    # Verify rule was added and banner dismissed
    new_rule_count = await page.evaluate("() => S.cfg?.elementRules?.length || 0")
    assert new_rule_count == initial_rule_count + 1

    # Banner should be hidden
    await expect(dock).to_be_hidden()

    # Rule must be retained in localStorage
    saved = await page.evaluate("() => localStorage.getItem('ll-active-cfg')")
    assert saved is not None
    assert_no_critical_errors(page)
