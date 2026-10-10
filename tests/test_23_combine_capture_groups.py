"""
test_23_combine_capture_groups.py — LogLens Regression Suite
Tests: Combining multiple capture groups into a single log element (e.g. date + | + time -> timestamp)
Covers:
- Interactive Regex Builder: Select multiple tokens, combine into single capture group, auto-map to log element, and split back.
- Manual Capture Group Mapping: Comma-separated group indices (e.g. "1, 2") in mapping inputs.
- Parse Engine: Correctly combining captured values and parsing non-standard delimiters (like "|") in timestamps.
- Context Menu: "+ Combine" action on live highlighted groups.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


async def _load_settings_and_open_modal(page):
    """Helper: open the Settings tab and click Add Rule."""
    await page.evaluate("() => { if (S.cfg === null) CFG.load(JSON.parse(JSON.stringify(DEF_CFG))); }")
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(400)
    await page.click('#btn-ar')
    await page.wait_for_timeout(400)


@pytest.mark.asyncio
async def test_interactive_regex_builder_combine_groups(page_with_data):
    """Selecting multiple tokens in Interactive Regex Builder and clicking Combine Groups merges them into one capture group mapped to timestamp."""
    page = page_with_data
    await _load_settings_and_open_modal(page)

    # 1. Enter a sample log line with date separated by pipe and time
    e_tl = page.locator('#e-tl')
    await e_tl.focus()
    await e_tl.fill("2026-10-10 | 14:23:45.123 [main] INFO Starting transaction")
    await page.evaluate("() => document.getElementById('e-tl').dispatchEvent(new Event('input', { bubbles: true }))")
    await page.wait_for_timeout(450)

    # 2. Click Date badge in the tracks container
    await page.evaluate("""() => {
        const btn = [...document.querySelectorAll('#rg-tracks-container .rg-match-badge')]
            .find(b => b.textContent.trim() === 'Date');
        if (btn) btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    }""")
    await page.wait_for_timeout(400)

    # 3. Click Time badge in the tracks container
    await page.evaluate("""() => {
        const btn = [...document.querySelectorAll('#rg-tracks-container .rg-match-badge')]
            .find(b => b.textContent.trim() === 'Time');
        if (btn) btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    }""")
    await page.wait_for_timeout(400)

    # 4. Verify Combine Bar is visible with at least 2 active selections
    combine_bar = page.locator('#rg-combine-bar')
    await expect(combine_bar).to_be_visible()

    # 5. Ensure combine target is timestamp
    target_sel = page.locator('#rg-combine-target')
    await expect(target_sel).to_have_value('timestamp')

    # 6. Click Combine All button
    btn_combine_all = page.locator('#btn-rg-combine-all')
    await btn_combine_all.click()
    await page.wait_for_timeout(400)

    # 7. Active selections must now show the combined chip
    selections = page.locator('#rg-active-selections')
    await expect(selections).to_contain_text('Timestamp (Combined):')

    # 8. Regex pattern must contain a unified capture group covering both date, gap with pipe, and time
    e_rx = page.locator('#e-rx')
    rx_val = await e_rx.input_value()
    assert "\\|" in rx_val or "|" in rx_val
    assert "^(" in rx_val

    # 9. Group #1 should be mapped to timestamp in cm-ts
    cm_ts = page.locator('#cm-ts')
    await expect(cm_ts).to_have_value("1")

    # 10. Click Split button on the combined chip
    split_btn = selections.locator('button', has_text='Split')
    await expect(split_btn).to_be_visible()
    await split_btn.click()
    await page.wait_for_timeout(400)

    # 11. Selections should revert to separate tokens
    await expect(selections).to_contain_text('Date:')
    await expect(selections).to_contain_text('Time:')

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_manual_combine_multiple_groups_mapping(page_with_data):
    """Users can enter comma-separated group numbers (e.g. '1, 2') in capture mapping inputs to combine them into one element."""
    page = page_with_data
    await _load_settings_and_open_modal(page)

    # 1. Enable custom regex
    adv_hdr = page.locator('#adv-hdr')
    await adv_hdr.click()
    await page.wait_for_timeout(200)

    chk_custom = page.locator('#e-use-custom-rx')
    await chk_custom.check()
    await page.wait_for_timeout(200)

    # 2. Enter regex with 4 groups
    e_rx = page.locator('#e-rx')
    await e_rx.fill(r"^(\d{4}-\d{2}-\d{2})\s*\|\s*(\d{2}:\d{2}:\d{2})\s+\[([^\]]+)\]\s+(.*)$")
    await page.evaluate("() => document.getElementById('e-rx').dispatchEvent(new Event('input', { bubbles: true }))")

    # 3. Enter comma-separated groups for timestamp ("1, 2")
    cm_ts = page.locator('#cm-ts')
    await cm_ts.fill("1, 2")
    await page.evaluate("() => document.getElementById('cm-ts').dispatchEvent(new Event('input', { bubbles: true }))")

    # 4. Map thread to group 3
    cm_th = page.locator('#cm-th')
    await cm_th.fill("3")
    await page.evaluate("() => document.getElementById('cm-th').dispatchEvent(new Event('input', { bubbles: true }))")

    # 5. Check capture diagram pills display combined group
    pills = page.locator('#cap-diagram-pills')
    await expect(pills).to_contain_text('Groups 1+2: timestamp')
    await expect(pills).to_contain_text('Group 3: thread')

    # 6. Verify internal _cm() returns proper mapping dictionary
    cm_dict = await page.evaluate("() => RXB._cm()")
    assert cm_dict.get('1') == 'timestamp'
    assert cm_dict.get('2') == 'timestamp'
    assert cm_dict.get('3') == 'thread'

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_parser_executes_combined_groups_timestamp(page_with_data):
    """PARSER.parseLine correctly concatenates multi-mapped groups and pts cleanly parses timestamps with pipe delimiters."""
    page = page_with_data

    # Test parser behavior in browser context
    result = await page.evaluate(r"""() => {
        const line = "2026-10-10 | 14:23:45.123 [worker-1] Starting batch";
        const ruleMulti = {
            id: 'r_multi_test',
            name: 'Pipe Timestamp Test',
            regexPattern: '^(\\d{4}-\\d{2}-\\d{2})\\s*\\|\\s*(\\d{2}:\\d{2}:\\d{2}\\.\\d{3})\\s+\\[([^\\]]+)\\]\\s+(.*)$',
            captureMapping: { '1': 'timestamp', '2': 'timestamp', '3': 'thread', '4': 'payload' },
            stackBehavior: 'inline'
        };

        const ruleCombined = {
            id: 'r_comb_test',
            name: 'Combined Pattern Test',
            regexPattern: '^(\\d{4}-\\d{2}-\\d{2}\\s*\\|\\s*\\d{2}:\\d{2}:\\d{2}\\.\\d{3})\\s+\\[([^\\]]+)\\]\\s+(.*)$',
            captureMapping: { '1': 'timestamp', '2': 'thread', '3': 'payload' },
            stackBehavior: 'inline'
        };

        const m1 = new RegExp(ruleMulti.regexPattern).exec(line);
        const c1 = STREAM_PARSER.caps(m1, ruleMulti.captureMapping);
        const ts1 = STREAM_PARSER.pts(c1.timestamp);

        const m2 = new RegExp(ruleCombined.regexPattern).exec(line);
        const c2 = STREAM_PARSER.caps(m2, ruleCombined.captureMapping);
        const ts2 = STREAM_PARSER.pts(c2.timestamp);

        return {
            c1_ts_str: c1.timestamp,
            ts1_val: ts1,
            c2_ts_str: c2.timestamp,
            ts2_val: ts2
        };
    }""")

    # Verify both approaches parse to valid millisecond timestamps
    assert result['ts1_val'] is not None and result['ts1_val'] > 1700000000000
    assert result['ts2_val'] is not None and result['ts2_val'] > 1700000000000
    assert result['ts1_val'] == result['ts2_val']

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_context_menu_combine_action(page_with_data):
    """Clicking + Combine in the live match context menu merges the clicked group into the existing field mapping."""
    page = page_with_data
    await _load_settings_and_open_modal(page)

    # 1. Fill sample line and regex pattern
    e_tl = page.locator('#e-tl')
    await e_tl.fill("2026-10-10 | 14:23:45.123 [worker] Starting")
    await page.evaluate("() => document.getElementById('e-tl').dispatchEvent(new Event('input', { bubbles: true }))")

    adv_hdr = page.locator('#adv-hdr')
    await adv_hdr.click()
    await page.wait_for_timeout(200)
    await page.locator('#e-use-custom-rx').check()

    e_rx = page.locator('#e-rx')
    await e_rx.fill(r"^(\d{4}-\d{2}-\d{2})\s*\|\s*(\d{2}:\d{2}:\d{2}(?:\.\d+)?)\s+\[([^\]]+)\]\s+(.*)$")
    await page.evaluate("() => document.getElementById('e-rx').dispatchEvent(new Event('input', { bubbles: true }))")

    # 2. Set timestamp initially to group 1
    cm_ts = page.locator('#cm-ts')
    await cm_ts.fill("1")
    await page.evaluate("() => document.getElementById('cm-ts').dispatchEvent(new Event('input', { bubbles: true }))")
    await page.wait_for_timeout(300)

    # 3. Click Group 2 in rx-pre
    grp_btn_2 = page.locator('.rx-grp-btn[data-gi="2"]').first
    await grp_btn_2.click()
    await page.wait_for_timeout(300)

    # 4. Context menu appears; click + Combine next to timestamp
    vgb_menu = page.locator('#vgb-menu')
    await expect(vgb_menu).to_be_visible()

    combine_btn = vgb_menu.locator('.vgb-mi[data-fid="cm-ts"] .vgb-combine-btn')
    await expect(combine_btn).to_be_visible()
    await combine_btn.click()
    await page.wait_for_timeout(300)

    # 5. cm-ts must now be "1, 2"
    await expect(cm_ts).to_have_value("1, 2")

    assert_no_critical_errors(page)
