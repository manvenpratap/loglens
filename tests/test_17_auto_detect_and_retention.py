"""
test_17_auto_detect_and_retention.py — LogLens Regression Suite
Tests: Automatic log pattern sniffing, format detection, rule synthesis,
saving rules to a file (File System Access API live sync & export),
and the adaptive rescue banner.
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
async def test_save_to_file_with_connected_handle(blank_page):
    """Saving configuration should write JSON directly to connected file handle with live sync."""
    page = blank_page

    result = await page.evaluate("""async () => {
        let writtenData = null;
        const mockHandle = {
            name: 'connected-rules.json',
            requestPermission: async () => 'granted',
            createWritable: async () => ({
                write: async (content) => { writtenData = content; },
                close: async () => {}
            })
        };

        const testCfg = {
            globalSettings: { appName: "File Persisted App" },
            elementRules: [
                {
                    id: "r_file_1",
                    name: "File Saved Rule",
                    regexPattern: "^(.*)$",
                    captureMapping: { "1": "payload" },
                    stackBehavior: "inline",
                    enabled: true
                }
            ]
        };

        CFG.load(testCfg);
        S.cfgHandle = mockHandle;
        await CFG.saveToFile();

        return {
            writtenData,
            cfgDotClass: document.getElementById('cfg-dot').className,
            cfgTxt: document.getElementById('cfg-txt').textContent,
            hdrCfgText: document.getElementById('hdr-cfg').textContent
        };
    }""")

    assert result['writtenData'] is not None
    parsed = json.loads(result['writtenData'])
    assert parsed['globalSettings']['appName'] == 'File Persisted App'
    assert len(parsed['elementRules']) == 1
    assert parsed['elementRules'][0]['name'] == 'File Saved Rule'
    assert 'live' in result['cfgDotClass']
    assert result['cfgTxt'] == 'connected-rules.json'
    assert 'Config ✓' in result['hdrCfgText']
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_live_sync_persists_rule_changes_to_file(blank_page):
    """When a file is connected, rule additions and edits via CFG.up() automatically write to the file."""
    page = blank_page

    result = await page.evaluate("""async () => {
        let lastWritten = null;
        const mockHandle = {
            name: 'auto-sync.json',
            requestPermission: async () => 'granted',
            createWritable: async () => ({
                write: async (content) => { lastWritten = content; },
                close: async () => {}
            })
        };

        CFG.load(JSON.parse(JSON.stringify(DEF_CFG)));
        S.cfgHandle = mockHandle;

        // Add a new rule
        const newRule = {
            id: 'r_live_test',
            name: 'Live Synced Rule',
            regexPattern: '^LIVE: (.*)$',
            captureMapping: { '1': 'payload' },
            stackBehavior: 'inline',
            enabled: true
        };
        CFG.up(newRule);
        await CFG.pers();

        return {
            lastWritten,
            ruleExistsInState: S.cfg.elementRules.some(r => r.id === 'r_live_test')
        };
    }""")

    assert result['ruleExistsInState'] is True
    assert result['lastWritten'] is not None
    parsed = json.loads(result['lastWritten'])
    assert any(r['id'] == 'r_live_test' for r in parsed['elementRules'])
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_reset_defaults(blank_page):
    """Clicking Reset Defaults resets configuration to defaults and disconnects active file handle."""
    page = blank_page

    await page.evaluate("""() => {
        S.cfgHandle = { name: 'old-file.json' };
        CFG.load({ globalSettings: {}, elementRules: [{ id: 'temp', name: 'Temp' }] });
    }""")

    # Accept the confirm dialog automatically
    page.on("dialog", lambda dialog: dialog.accept())

    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(300)

    btn_reset = page.locator('#btn-reset-defaults')
    await expect(btn_reset).to_be_visible()
    await btn_reset.click()
    await page.wait_for_timeout(400)

    res = await page.evaluate("() => ({ handle: S.cfgHandle, rulesCount: S.cfg?.elementRules?.length })")
    assert res['handle'] is None
    assert res['rulesCount'] > 1
    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_adaptive_rescue_banner_and_save_to_file(page_with_data):
    """Adaptive rescue banner should display when unparsed lines exceed threshold and save rule to file."""
    page = page_with_data

    # Ensure active config and mock file handle exist
    await page.evaluate("""() => {
        if (!S.cfg) CFG.load(JSON.parse(JSON.stringify(DEF_CFG)));
        let written = null;
        S.cfgHandle = {
            name: 'production-rules.json',
            requestPermission: async () => 'granted',
            createWritable: async () => ({
                write: async (content) => { written = content; S._lastWrittenContent = content; },
                close: async () => {}
            })
        };
    }""")

    # Simulate parse output with high unparsed lines
    await page.evaluate("""() => {
        const dummyStats = {
            fileSize: 5000,
            linesProcessed: 100,
            matchedLines: 40, // 60% unparsed
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
    await expect(auto_add_btn).to_contain_text('Save to File')

    # Click + Auto-Add Rule & Save to File
    initial_rule_count = await page.evaluate("() => S.cfg?.elementRules?.length || 0")
    await auto_add_btn.click()
    await page.wait_for_timeout(300)

    # Verify rule was added, banner dismissed, and written to connected file
    new_rule_count = await page.evaluate("() => S.cfg?.elementRules?.length || 0")
    assert new_rule_count == initial_rule_count + 1
    await expect(dock).to_be_hidden()

    written_content = await page.evaluate("() => S._lastWrittenContent")
    assert written_content is not None
    assert_no_critical_errors(page)
