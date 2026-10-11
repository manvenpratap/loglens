"""
test_consolidated_rules_and_regex.py — Consolidated Regression Test Suite
Merges and deduplicates tests from: test_13_rule_creator.py, test_15_regex_undo_redo.py, test_16_interactive_regex_builder.py, test_17_auto_detect_and_retention.py, test_18_custom_log_pattern_journey.py, test_21_custom_log_setup_journey.py, test_23_combine_capture_groups.py
"""
import os
import re
import json
import tempfile
import pytest
import asyncio
from playwright.async_api import expect, Page
from conftest import APP_URL, DISMISS_ONBOARDING_JS, DEMO_TREES_JS, assert_no_critical_errors


async def _load_settings(page):
    """Helper: open the Settings tab after onboarding is dismissed and ensure configuration is loaded."""
    await page.evaluate("() => { if (S.cfg === null) CFG.load(JSON.parse(JSON.stringify(DEF_CFG))); }")
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(500)
@pytest.mark.asyncio
async def test_rule_creator_unified_modal(page_with_data):
    """Rule creator modal must not have mode tabs, and must show steps and accordion sections."""
    page = page_with_data
    await _load_settings(page)

    # 1. Open the "Add Rule" modal
    btn_ar = page.locator('#btn-ar')
    await expect(btn_ar).to_be_visible()
    await btn_ar.click()
    await page.wait_for_timeout(500)

    # 2. Check modal headers/titles
    m_ttl = page.locator('#m-ttl')
    await expect(m_ttl).to_contain_text("Add New Rule")

    # 3. Assert mode tabs do NOT exist
    mb_g = page.locator('#mb-g')
    mb_a = page.locator('#mb-a')
    await expect(mb_g).not_to_be_visible()
    await expect(mb_a).not_to_be_visible()

    # 4. Check unified layout Step 1 is visible
    step_1 = page.locator('.ws-step >> text=Paste Sample Log Line')
    await expect(step_1).to_be_visible()

    # 5. Check collapsible accordion headers are visible
    ovr_hdr = page.locator('#ovr-hdr')
    adv_hdr = page.locator('#adv-hdr')
    vis_hdr = page.locator('#vis-hdr')
    await expect(ovr_hdr).to_be_visible()
    await expect(adv_hdr).to_be_visible()
    await expect(vis_hdr).to_be_visible()

    # Check that bodies start collapsed/hidden
    await expect(page.locator('#ovr-body')).to_have_class("ovr-section-body hidden")
    await expect(page.locator('#adv-body')).to_have_class("adv-section-body hidden")
    await expect(page.locator('#vis-body')).to_have_class("vis-section-body hidden")

    # Check for critical console errors
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_rule_creator_tooltip_helpers(page_with_data):
    """Clicking helper '?' icons must open contextual tooltip popovers with correct descriptions."""
    page = page_with_data
    await _load_settings(page)

    # Open Add Rule modal
    await page.click('#btn-ar')
    await page.wait_for_timeout(400)

    # Expand manual override to make format/keyword help buttons visible
    await page.click('#ovr-hdr')
    await page.wait_for_timeout(300)

    # 1. Test format help tooltip
    btn_fmt_help = page.locator('button[data-htip="format"]')
    await expect(btn_fmt_help).to_be_visible()
    await btn_fmt_help.click()
    await page.wait_for_timeout(300)

    # Assert popover is visible and contains correct content
    htip_pop = page.locator('#htip-pop')
    await expect(htip_pop).to_be_visible()
    await expect(page.locator('#htip-pop-ttl-text')).to_contain_text("Log Format Presets")
    await expect(page.locator('#htip-pop-body')).to_contain_text("Java Standard")

    # Click modal title to close help popover
    await page.click('#m-ttl')
    await page.wait_for_timeout(300)
    await expect(htip_pop).not_to_be_visible()

    # 2. Test keywords help tooltip
    btn_kw_help = page.locator('button[data-htip="keywords"]')
    await expect(btn_kw_help).to_be_visible()
    await btn_kw_help.click()
    await page.wait_for_timeout(300)

    await expect(htip_pop).to_be_visible()
    await expect(page.locator('#htip-pop-ttl-text')).to_contain_text("Keywords / Markers Help")
    await expect(page.locator('#htip-pop-body')).to_contain_text("Match Mode")

    # Click body to close
    await page.click('#m-ttl')
    await page.wait_for_timeout(300)
    await expect(htip_pop).not_to_be_visible()

    # Assert no critical errors
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_rule_creator_advanced_accordion_interaction(page_with_data):
    """Accordion sections must expand/collapse, toggle custom regex checkbox, and update field states."""
    page = page_with_data
    await _load_settings(page)

    await page.click('#btn-ar')
    await page.wait_for_timeout(400)

    ovr_hdr = page.locator('#ovr-hdr')
    ovr_body = page.locator('#ovr-body')
    adv_hdr = page.locator('#adv-hdr')
    adv_body = page.locator('#adv-body')
    vis_hdr = page.locator('#vis-hdr')
    vis_body = page.locator('#vis-body')
    chk_custom = page.locator('#e-use-custom-rx')
    inp_rx = page.locator('#e-rx')

    # 1. Test Manual Override Accordion collapse toggling
    await expect(ovr_body).to_have_class("ovr-section-body hidden")
    await ovr_hdr.click()
    await page.wait_for_timeout(300)
    await expect(ovr_body).not_to_have_class("ovr-section-body hidden")
    await ovr_hdr.click()
    await page.wait_for_timeout(300)
    await expect(ovr_body).to_have_class("ovr-section-body hidden")

    # 2. Test Appearance & SLA Accordion collapse toggling
    await expect(vis_body).to_have_class("vis-section-body hidden")
    await vis_hdr.click()
    await page.wait_for_timeout(300)
    await expect(vis_body).not_to_have_class("vis-section-body hidden")
    await vis_hdr.click()
    await page.wait_for_timeout(300)
    await expect(vis_body).to_have_class("vis-section-body hidden")

    # 3. Test Advanced Accordion
    await expect(adv_body).to_have_class("adv-section-body hidden")
    await adv_hdr.click()
    await page.wait_for_timeout(300)
    await expect(adv_body).not_to_have_class("adv-section-body hidden")
    await expect(chk_custom).to_be_visible()

    # By default, custom regex is unchecked, and e-rx is disabled
    is_checked = await chk_custom.is_checked()
    assert not is_checked, "Custom regex checkbox should be unchecked by default"
    await expect(inp_rx).to_be_disabled()

    # Check Custom Regex Checkbox -> Enables the inputs
    await chk_custom.click()
    await page.wait_for_timeout(300)
    assert await chk_custom.is_checked()
    await expect(inp_rx).not_to_be_disabled()

    # Mappings inputs must also be enabled
    await expect(page.locator('#cm-ts')).not_to_be_disabled()
    await expect(page.locator('#cm-th')).not_to_be_disabled()
    await expect(page.locator('#cm-el')).not_to_be_disabled()

    # Test Capture Group Mapping accordion collapse toggling
    map_hdr = page.locator('#map-hdr')
    map_body = page.locator('#map-body')
    await expect(map_body).not_to_have_class("map-section-body hidden")
    await map_hdr.click()
    await page.wait_for_timeout(300)
    await expect(map_body).to_have_class("map-section-body hidden")
    await map_hdr.click()
    await page.wait_for_timeout(300)
    await expect(map_body).not_to_have_class("map-section-body hidden")

    # Uncheck custom regex -> Disables inputs again
    await chk_custom.click()
    await page.wait_for_timeout(300)
    await expect(inp_rx).to_be_disabled()
    await expect(page.locator('#cm-ts')).to_be_disabled()

    # Assert no critical errors
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_rule_creator_live_match_highlighting(page_with_data):
    """Typing keywords and pasting test lines must produce colorized match previews and allow mapping."""
    page = page_with_data
    await _load_settings(page)

    await page.click('#btn-ar')
    await page.wait_for_timeout(400)

    # 1. Verify format selector starts as 'auto'
    sel_format = page.locator('#wf-sel')
    await expect(sel_format).to_have_value('auto')

    # Expand manual override accordion to expose keyword inputs
    await page.click('#ovr-hdr')
    await page.wait_for_timeout(300)

    # Add keyword
    await page.fill('#kw-inp', 'GET')
    await page.click('#btn-kw')
    await page.wait_for_timeout(300)

    # Verify chip exists
    await expect(page.locator('#kw-chips')).to_contain_text("GET")

    # 2. Fill sample log line (Spring Boot format)
    test_line = "2026-07-03 08:30:15,123  INFO  12345 --- [nio-8080-exec-1] c.e.s.Svc   : GET /items"
    await page.fill('#e-tl', test_line)
    await page.wait_for_timeout(400)

    # 3. Assert format is auto-detected as 'spring'!
    await expect(sel_format).to_have_value('spring')

    # 4. Check that rx-pre highlights the matched tokens.
    # Group 1 (timestamp): 2026-07-03 08:30:15,123
    # Group 3 (thread): nio-8080-exec-1
    grp_1 = page.locator('.rx-ln span.rx-grp-btn[data-gi="1"]')
    grp_3 = page.locator('.rx-ln span.rx-grp-btn[data-gi="3"]')
    await expect(grp_1).to_be_visible()
    await expect(grp_3).to_be_visible()

    # 5. Customize mapping by clicking group 3 in the preview
    chk_custom = page.locator('#e-use-custom-rx')
    assert not await chk_custom.is_checked(), "Custom checkbox should start unchecked"

    await page.evaluate("() => document.querySelector('.rx-leg span.rx-grp-btn[data-gi=\"3\"]').click()")
    await page.wait_for_timeout(300)

    # Context menu vgb-menu should be open
    menu = page.locator('#vgb-menu')
    await expect(menu).to_be_visible()

    # Map to elementName (data-fid="cm-el")
    btn_map_el = menu.locator('[data-fid="cm-el"]')
    await btn_map_el.click()
    await page.wait_for_timeout(300)

    # 6. Verify custom checkbox is now automatically checked!
    assert await chk_custom.is_checked(), "Custom checkbox should be checked after visual mapping"
    # Verify cm-el mapping value is updated to 3
    val_el = await page.locator('#cm-el').input_value()
    assert val_el == "3"

    # Assert no critical errors
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_rule_creator_ar_button_enabled_on_blank_page(blank_page):
    """Add Rule button must be enabled even on a blank configuration state and auto-bootstrap on click."""
    page = blank_page
    
    # 0. Dismiss onboarding overlay
    await page.evaluate("() => ONBOARD.dismiss()")
    await page.wait_for_timeout(300)
    
    # 1. Switch to settings panel
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(500)
    
    # 2. Check S.cfg is null
    is_null = await page.evaluate("() => S.cfg === null")
    assert is_null, "S.cfg should start as null"
    
    # 3. Assert #btn-ar and #btn-rule-imp are enabled
    btn_ar = page.locator('#btn-ar')
    btn_imp = page.locator('#btn-rule-imp')
    await expect(btn_ar).to_be_visible()
    await expect(btn_ar).not_to_be_disabled()
    await expect(btn_imp).to_be_visible()
    await expect(btn_imp).not_to_be_disabled()
    
    # 4. Click #btn-ar
    await btn_ar.click()
    await page.wait_for_timeout(400)
    
    # 5. Assert S.cfg has been auto-bootstrapped (non-null) and modal is open
    is_non_null = await page.evaluate("() => S.cfg !== null")
    assert is_non_null, "S.cfg should be bootstrapped"
    
    await expect(page.locator('#m-ttl')).to_contain_text("Add New Rule")
    
    # Check that rules count badge has been updated to 0 (since it loaded an empty config)
    rules_count = await page.evaluate("() => S.cfg.elementRules.length")
    assert rules_count == 0, "Bootstrapped config should start with empty rules list"
    
    # Close modal
    await page.click('#btn-mx')
    await page.wait_for_timeout(200)
    
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_rule_creator_class_method_mapping_and_explainer(page_with_data):
    """Explainer must display capture group labels, class/method mapping inputs must exist and sync preview immediately."""
    page = page_with_data
    await _load_settings(page)

    await page.click('#btn-ar')
    await page.wait_for_timeout(400)

    # 1. Verify className (#cm-cl) and methodName (#cm-me) inputs exist and are visible in Advanced
    await page.click('#adv-hdr')
    await page.wait_for_timeout(300)
    
    cm_cl = page.locator('#cm-cl')
    cm_me = page.locator('#cm-me')
    await expect(cm_cl).to_be_visible()
    await expect(cm_me).to_be_visible()

    # 2. Enter Spring Boot log line
    test_line = "2026-07-03 08:30:15,123  INFO  12345 --- [nio-8080-exec-1] c.e.s.Svc   : GET /items"
    await page.fill('#e-tl', test_line)
    await page.wait_for_timeout(400)

    # 3. Verify auto-detected format is 'spring'
    await expect(page.locator('#wf-sel')).to_have_value('spring')

    # 4. Verify className (Group 4) is auto-mapped
    val_cl = await cm_cl.input_value()
    assert val_cl == "4", f"className should be auto-mapped to Group 4, got {val_cl}"

    # 5. Customize Regex (check custom checkbox to enable advanced modifications)
    chk_custom = page.locator('#e-use-custom-rx')
    await chk_custom.check()
    await page.wait_for_timeout(300)

    # 6. Click Explain Regex and verify group identifier labels (e.g. [G1], [G2]) inside tokens
    btn_explain = page.locator('#btn-rex-explain')
    await btn_explain.click()
    await page.wait_for_timeout(300)

    explain_results = page.locator('#rex-explain-results')
    await expect(explain_results).to_be_visible()
    await expect(explain_results).to_contain_text("[G1]")
    await expect(explain_results).to_contain_text("[G2]")
    await expect(explain_results).to_contain_text("[G3]")
    await expect(explain_results).to_contain_text("[G4]")

    # 7. Check match legend before change: Group 3 should be 'thread' (thr)
    leg_3 = page.locator('.rx-leg span.rx-grp-btn[data-gi="3"]')
    await expect(leg_3).to_contain_text("thr")

    # 8. Modify mapping input (change thread mapping #cm-th from 3 to 5) and verify instant preview update
    await page.fill('#cm-th', '5')
    # Trigger a change event just in case (though input event listener is also registered)
    await page.locator('#cm-th').evaluate("el => el.dispatchEvent(new Event('change'))")
    await page.wait_for_timeout(300)

    # Check match legend after change: Group 3 should now be generic 'group 3' and Group 5 should be 'thr'
    await expect(leg_3).to_contain_text("group 3")

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_rule_creator_help_tips(page_with_data):
    """Verify that help tooltips show correctly."""
    page = page_with_data
    await _load_settings(page)

    await page.click('#btn-ar')
    await page.wait_for_timeout(400)

    # Click a help tooltip icon (e.g. Stack Behavior help icon)
    btn_help = page.locator('button[data-htip="behavior"]')
    await btn_help.click()
    await page.wait_for_timeout(300)

    # Check help popover is visible and has correct contents
    pop = page.locator('#htip-pop')
    await expect(pop).to_be_visible()
    await expect(pop).to_contain_text("Stack Behavior")

    # Close help popover
    await page.click('#htip-pop-close')
    await page.wait_for_timeout(200)
    await expect(pop).not_to_be_visible()

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_rule_creator_icon_dropdown_and_auto_suggestion(page_with_data):
    """Verify that rule icon is a dropdown and suggested icons are prepopulated based on the rule name."""
    page = page_with_data
    await _load_settings(page)

    await page.click('#btn-ar')
    await page.wait_for_timeout(400)

    # 1. Expand visual / appearance accordion to expose icon select dropdown
    await page.click('#vis-hdr')
    await page.wait_for_timeout(300)

    # 2. Check that #e-ico is a select dropdown
    sel_ico = page.locator('#e-ico')
    await expect(sel_ico).to_be_visible()
    await expect(sel_ico).to_have_value('•')

    # 3. Enter a rule name containing "Database" -> should auto-suggest 🗄
    await page.fill('#e-name', 'My Database Rule')
    await page.wait_for_timeout(300)
    await expect(sel_ico).to_have_value('🗄')

    # 4. Enter a rule name containing "api network" -> should auto-suggest 🌐
    await sel_ico.select_option('•')
    await page.fill('#e-name', 'API Network controller')
    await page.wait_for_timeout(300)
    await expect(sel_ico).to_have_value('🌐')

    # 5. Check warning
    await sel_ico.select_option('•')
    await page.fill('#e-name', 'Warning breach alert')
    await page.wait_for_timeout(300)
    await expect(sel_ico).to_have_value('⚠')

    # 6. Check error
    await sel_ico.select_option('•')
    await page.fill('#e-name', 'Fatal Crash Exception')
    await page.wait_for_timeout(300)
    await expect(sel_ico).to_have_value('✕')

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_rule_creator_stack_behavior_human_friendly_labels(page_with_data):
    """Verify that Stack Behavior dropdown uses human-friendly labels with action context."""
    page = page_with_data
    await _load_settings(page)

    await page.click('#btn-ar')
    await page.wait_for_timeout(400)

    # Locate #e-beh select dropdown
    sel_beh = page.locator('#e-beh')
    await expect(sel_beh).to_be_visible()

    # Query all options and their text contents
    options = await page.evaluate("""() => {
        const sel = document.getElementById('e-beh');
        return Array.from(sel.options).map(o => ({ value: o.value, text: o.text.trim() }));
    }""")

    expected = [
        {"value": "push", "text": "Block Start — push"},
        {"value": "pop", "text": "Block End — pop"},
        {"value": "inline", "text": "Point Event — inline"},
        {"value": "swap", "text": "Transition — swap"},
        {"value": "popAll", "text": "Close All Blocks — popAll"},
    ]

    assert options == expected, f"Expected {expected}, got {options}"

    # Verify selecting options by value updates selection
    await sel_beh.select_option("pop")
    assert await sel_beh.input_value() == "pop"

    await sel_beh.select_option("inline")
    assert await sel_beh.input_value() == "inline"

    await sel_beh.select_option("push")
    assert await sel_beh.input_value() == "push"

    # Verify Stack Behavior tooltip includes the human-friendly labels
    btn_help = page.locator('button[data-htip="behavior"]')
    await btn_help.click()
    await page.wait_for_timeout(300)

    pop = page.locator('#htip-pop')
    await expect(pop).to_be_visible()
    pop_body = await page.locator('#htip-pop-body').inner_text()
    assert "Block Start — push" in pop_body
    assert "Block End — pop" in pop_body
    assert "Point Event — inline" in pop_body

    await page.click('#htip-pop-close')
    await page.wait_for_timeout(200)

    assert_no_critical_errors(page)
async def _load_settings_and_open_modal(page):
    """Helper: open the Settings tab and click Add Rule."""
    await page.evaluate("() => { if (S.cfg === null) CFG.load(JSON.parse(JSON.stringify(DEF_CFG))); }")
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(500)
    await page.click('#btn-ar')
    await page.wait_for_timeout(400)
@pytest.mark.asyncio
async def test_regex_undo_redo_functionality(page_with_data):
    """Undo and Redo buttons must change the regex pattern text value and follow history states."""
    page = page_with_data
    await _load_settings_and_open_modal(page)

    # 1. Expand advanced accordion to view the regex pattern textarea
    await page.click('#adv-hdr')
    await page.wait_for_timeout(300)

    # 2. Check that buttons exist
    btn_undo = page.locator('#btn-rx-undo')
    btn_redo = page.locator('#btn-rx-redo')
    e_rx = page.locator('#e-rx')
    chk_custom = page.locator('#e-use-custom-rx')

    # Initially both should be disabled
    await expect(btn_undo).to_be_disabled()
    await expect(btn_redo).to_be_disabled()

    # Enable custom regex pattern mode to unlock editing on e-rx
    await chk_custom.check()
    await page.wait_for_timeout(300)

    # Undo might be enabled here if checking custom auto-filled a wizard pattern.
    # Let's read the value after check.
    val_initial = await e_rx.input_value()

    # 3. Focus on regex input and type something different
    await e_rx.focus()
    await e_rx.fill("hello")
    # Dispatch manual input event
    await page.evaluate("() => document.getElementById('e-rx').dispatchEvent(new Event('input', { bubbles: true }))")
    await page.wait_for_timeout(300)

    # Undo should definitely be enabled now
    await expect(btn_undo).to_be_enabled()

    # 4. Perform Undo
    await btn_undo.click()
    await page.wait_for_timeout(300)

    # Value should go back to the state before "hello" (e.g. empty or auto-filled pattern)
    val_after_undo = await e_rx.input_value()
    assert val_after_undo == val_initial
    await expect(btn_redo).to_be_enabled()

    # 5. Perform Redo
    await btn_redo.click()
    await page.wait_for_timeout(300)

    # Value should restore to "hello"
    val_after_redo = await e_rx.input_value()
    assert val_after_redo == "hello"
    await expect(btn_redo).to_be_disabled()

    # Ensure no critical console errors occurred
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_interactive_regex_builder_flow(page_with_data):
    """Interactive regex builder must parse tracks, accept selections in input, suggest matches, and auto-populate capture mappings."""
    page = page_with_data
    await _load_settings_and_open_modal(page)

    # 1. Assert visual regex builder UI container is visible
    container = page.locator('#visual-regex-generator-step')
    await expect(container).to_be_visible()

    # 2. Enter a sample log line
    e_tl = page.locator('#e-tl')
    await e_tl.focus()
    await e_tl.fill("2026-07-05 10:00:00 [main] ERROR - connection timeout")
    await page.evaluate("() => document.getElementById('e-tl').dispatchEvent(new Event('input', { bubbles: true }))")
    await page.wait_for_timeout(450)

    # 3. Match badges should be rendered as options in the tracks container
    tracks_container = page.locator('#rg-tracks-container')
    # Use exact text to avoid matching "DateTime" when looking for "Date"
    date_badge = tracks_container.get_by_role('button', name='Date', exact=True)
    await expect(date_badge).to_be_visible()

    # 4. Click the Date option badge to select it (use JS dispatch since badge is position:absolute inside scroll container)
    await page.evaluate("""() => {
        const btn = [...document.querySelectorAll('#rg-tracks-container .rg-match-badge')]
            .find(b => b.textContent.trim() === 'Date');
        if (btn) btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    }""")
    await page.wait_for_timeout(600)

    # 5. Badge state should turn into selected — verify via active selections chip
    # (the badge re-renders with a checkmark; active-selections also shows the chip)
    selections = page.locator('#rg-active-selections')
    await expect(selections).to_contain_text('Date:')

    # 6. Active selections container should display the badge (already verified above)


    # 7. Regex pattern input e-rx must be populated with a capture group matching the date pattern
    e_rx = page.locator('#e-rx')
    rx_val = await e_rx.input_value()
    assert len(rx_val) > 0
    assert "(\\d{4}-\\d{2}-\\d{2})" in rx_val

    # 8. Check auto-population of Timestamp custom mapping
    cm_ts = page.locator('#cm-ts')
    await expect(cm_ts).to_have_value("1")

    # 9. Test selecting an arbitrary range to get suggestions (e.g. select "ERROR" at index 28 to 33)
    # "2026-07-05 10:00:00 [main] ERROR - connection timeout"
    # Index of "ERROR" is 27 to 32.
    await page.evaluate("() => { const el = document.getElementById('e-tl'); el.focus(); el.setSelectionRange(27, 32); el.dispatchEvent(new Event('select')); }")
    await page.wait_for_timeout(400)

    # Suggestions container should become visible
    suggestions_container = page.locator('#rg-selection-suggestions')
    await expect(suggestions_container).to_be_visible()
    await expect(page.locator('#rg-selected-text-preview')).to_have_text("ERROR")

    # Click the Log Levels suggestion button (using .first to avoid strict mode violation on multiple pattern options)
    log_level_sug = page.locator('#rg-suggestions-list button', has_text="Log Levels:").first
    await log_level_sug.click()
    await page.wait_for_timeout(400)

    # Suggestions container should now be hidden
    await expect(suggestions_container).not_to_be_visible()

    # Custom mapping for Log Level (#cm-lv) should be auto-populated to 2 (since ERROR is the second capture group)
    cm_lv = page.locator('#cm-lv')
    await expect(cm_lv).to_have_value("2")

    # Ensure no critical console errors occurred during the flow
    assert_no_critical_errors(page)
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
@pytest.mark.asyncio
async def test_empty_state_custom_rule_builder_discovery(blank_page):
    """User on empty state can discover and immediately launch Custom Rule Builder."""
    page = blank_page

    # Dismiss onboarding welcome overlay and switch to empty state view
    await page.evaluate(DISMISS_ONBOARDING_JS)
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(300)

    # Empty state card actions must include the Custom Rule Builder CTA
    btn_custom = page.locator('#btn-emp-create-rule')
    await expect(btn_custom).to_be_visible()
    await expect(btn_custom).to_contain_text("Custom Rule Builder")

    # Clicking launches the Rule Creator modal
    await btn_custom.click()
    await page.wait_for_timeout(300)

    modal = page.locator('#mm')
    await expect(modal).to_be_visible()
    await expect(page.locator('#m-ttl')).to_contain_text("Add New Rule")

    # Verify rule modal inputs are active and configuration is initialized
    cfg_init = await page.evaluate("() => S.cfg !== null && Array.isArray(S.cfg.elementRules)")
    assert cfg_init is True

    # Close modal
    await page.locator('#btn-mx').click()
    await expect(modal).not_to_be_visible()

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_custom_log_pattern_interactive_builder_flow(blank_page):
    """User pastes a custom log line, selects pattern tokens, maps groups, and saves rule."""
    page = blank_page

    # Dismiss onboarding and show empty state view
    await page.evaluate(DISMISS_ONBOARDING_JS)
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(300)

    # Launch Rule Creator
    await page.locator('#btn-emp-create-rule').click()
    await page.wait_for_timeout(300)

    # Fill Rule Name and Stack Behavior
    await page.locator('#e-name').fill("Custom Auth Service")
    await page.locator('#e-beh').select_option("push")

    # Enter custom line of log
    sample_line = "2026-10-08 14:23:45.123 [worker-4] [auth-svc] INFO - User login ok user_id=42"
    tl_input = page.locator('#e-tl')
    await tl_input.fill(sample_line)
    await page.wait_for_timeout(300)

    # Check that format status badge recognizes custom pattern
    badge = page.locator('#preview-format-badge')
    await expect(badge).to_contain_text("Custom Pattern")

    # Badges must render in interactive builder tracks container
    tracks = page.locator('#rg-tracks-container')
    await expect(tracks).to_be_visible()
    badges = page.locator('.rg-match-badge')
    badge_count = await badges.count()
    assert badge_count > 0, "Expected match badges to be generated for custom line"

    # Click DateTime badge to select timestamp
    dt_badge = page.locator('.rg-match-badge', has_text="DateTime").first
    if await dt_badge.is_visible():
        await dt_badge.click()
        await page.wait_for_timeout(200)

    # Click Thread name badge
    thr_badge = page.locator('.rg-match-badge', has_text="Thread name").first
    if await thr_badge.is_visible():
        await thr_badge.click()
        await page.wait_for_timeout(200)

    # Click Log level badge
    lvl_badge = page.locator('.rg-match-badge', has_text="Log level").first
    if await lvl_badge.is_visible():
        await lvl_badge.click()
        await page.wait_for_timeout(200)

    # Verify generated regex and group mappings
    rx_val = await page.locator('#e-rx').input_value()
    assert len(rx_val) > 10, f"Expected valid regex in #e-rx, got: {rx_val}"
    assert rx_val.startswith('^'), "Regex should begin with anchor ^"

    # Verify timestamp mapping auto-populated
    ts_map = await page.locator('#cm-ts').input_value()
    assert ts_map == "1", f"Timestamp mapping expected 1, got {ts_map}"

    # Verify thread mapping auto-populated
    th_map = await page.locator('#cm-th').input_value()
    assert th_map == "2", f"Thread mapping expected 2, got {th_map}"

    # Verify level mapping auto-populated
    lv_map = await page.locator('#cm-lv').input_value()
    assert lv_map == "3", f"Level mapping expected 3, got {lv_map}"

    # Verify live preview in Step 1 rendered without error
    rx_pre = page.locator('#rx-pre')
    await expect(rx_pre).to_be_visible()
    await expect(rx_pre).not_to_contain_text("Error:")

    # Save rule
    await page.locator('#btn-ms').click()
    await page.wait_for_timeout(300)

    # Verify modal closed
    await expect(page.locator('#mm')).not_to_be_visible()

    # Verify rule was added to S.cfg.elementRules
    rules = await page.evaluate("() => S.cfg.elementRules")
    assert len(rules) == 1
    assert rules[0]["name"] == "Custom Auth Service"
    assert rules[0]["stackBehavior"] == "push"
    assert rules[0]["captureMapping"]["1"] == "timestamp"
    assert rules[0]["captureMapping"]["2"] == "thread"
    assert rules[0]["captureMapping"]["3"] == "level"

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_rule_test_suite_evaluates_custom_lines(page_with_data):
    """Rule Test Suite button is enabled and tests sample lines against rules without defects."""
    page = page_with_data

    # Ensure a rule set is active
    await page.evaluate("() => { if (!S.cfg || !S.cfg.elementRules?.length) CFG.load(JSON.parse(JSON.stringify(DEF_CFG))); }")

    # Open Settings tab
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(300)

    # Assert Rule Test button is enabled when rules are loaded
    btn_rts = page.locator('#btn-rule-test')
    await expect(btn_rts).to_be_visible()
    await expect(btn_rts).to_be_enabled()

    # Open Rule Test Suite
    await btn_rts.click()
    await page.wait_for_timeout(300)

    rts_modal = page.locator('#rts-mm')
    await expect(rts_modal).to_be_visible()

    # Paste sample lines into RTS textarea
    sample_text = (
        "2026-10-08 14:23:45.123 [main] INFO com.example.App - TX-BEGIN Order 100\n"
        "2026-10-08 14:23:46.456 [main] INFO com.example.App - TX-END Order 100\n"
        "2026-10-08 14:23:47.789 [main] ERROR com.example.App - Database connection timeout"
    )
    await page.locator('#rts-inp').fill(sample_text)

    # Run test
    btn_run = page.locator('#rts-mm button', has_text="Test All Rules")
    await btn_run.click()
    await page.wait_for_timeout(300)

    # Check results container
    out = page.locator('#rts-out')
    await expect(out).to_be_visible()
    out_text = await out.inner_text()
    assert "rules matched" in out_text
    assert "✓" in out_text

    # Close modal
    await page.locator('#rts-mm button[aria-label="Close rule test results"]').click()
    await expect(rts_modal).not_to_be_visible()

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_custom_log_file_parse_journey(blank_page):
    """End-to-end parse journey with custom rule and log line."""
    page = blank_page

    # Dismiss onboarding
    await page.evaluate(DISMISS_ONBOARDING_JS)
    await page.wait_for_timeout(300)

    # Define custom rule
    await page.evaluate("""() => {
        const customRule = {
            id: 'r_custom_op',
            name: 'ProcessOrder',
            regexPattern: '^(\\\\d{4}-\\\\d{2}-\\\\d{2} \\\\d{2}:\\\\d{2}:\\\\d{2}[.,]\\\\d{3})\\\\s+\\\\[([^\\\\]]+)\\\\]\\\\s+(INFO|ERROR)\\\\s+-\\\\s+(.+)$',
            captureMapping: { '1': 'timestamp', '2': 'thread', '3': 'level', '4': 'payload' },
            stackBehavior: 'inline',
            visualStyle: { accentColor: '#38bdf8', icon: '⚡' },
            enabled: true
        };
        CFG.load({
            globalSettings: { appName: 'CustomApp', defaultTimeZone: 'UTC' },
            elementRules: [customRule]
        });
    }""")

    # Parse custom log text
    log_content = (
        "2026-10-08 14:20:00.000 [worker-1] INFO - ProcessOrder starting id=A101\n"
        "2026-10-08 14:20:01.500 [worker-1] INFO - ProcessOrder validated id=A101\n"
        "2026-10-08 14:20:02.000 [worker-2] ERROR - ProcessOrder payment failed id=A102\n"
    )

    await page.evaluate(f"""async () => {{
        const blob = new Blob([`{log_content}`], {{ type: 'text/plain' }});
        const file = new File([blob], 'custom.log', {{ type: 'text/plain' }});
        S.logFile = file;
        const res = await WM.parse(file, S.cfg, '');
        UI.render(res.trees, res.threads, res.stats);
    }}""")

    # Wait for parser to complete
    await page.wait_for_timeout(500)

    # Verify trees exist for threads worker-1 and worker-2
    threads = await page.evaluate("() => Object.keys(S.trees)")
    assert "worker-1" in threads
    assert "worker-2" in threads

    # Verify node contents
    w1_nodes = await page.evaluate("() => S.trees['worker-1']")
    assert len(w1_nodes) == 2
    assert w1_nodes[0]["thread"] == "worker-1"
    assert "ProcessOrder starting" in w1_nodes[0]["payload"]

    w2_nodes = await page.evaluate("() => S.trees['worker-2']")
    assert len(w2_nodes) == 1
    assert w2_nodes[0]["level"] == "ERROR"

    # Switch views to verify rendering without JS errors
    await page.evaluate("() => UI.svm('tree')")
    await page.wait_for_timeout(300)
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(300)

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_unparsed_rescue_flow_for_custom_patterns(blank_page):
    """When custom log lines exceed unparsed threshold, Adaptive Rescue banner appears and launches Custom Regex editor."""
    page = blank_page

    # Dismiss onboarding
    await page.evaluate(DISMISS_ONBOARDING_JS)
    await page.wait_for_timeout(300)

    # Trigger Adaptive Rescue with unparsed sample lines
    await page.evaluate("""() => {
        const stats = {
            linesProcessed: 100,
            matchedLines: 10,
            unparsedSample: [
                "2026-10-08 14:23:45.123 [worker-4] [custom-mod] UNKNOWN_OP payload=foo",
                "2026-10-08 14:23:45.124 [worker-4] [custom-mod] UNKNOWN_OP payload=bar",
                "2026-10-08 14:23:45.125 [worker-4] [custom-mod] UNKNOWN_OP payload=baz"
            ]
        };
        S.stats = stats;
        SNIFFER.checkUnparsedRescue(stats);
    }""")

    await page.wait_for_timeout(300)

    # Verify rescue banner is visible
    banner = page.locator('#rescue-banner')
    await expect(banner).to_be_visible()
    await expect(banner).to_contain_text("Adaptive Rescue")

    # Click "Custom Regex" button
    btn_custom_rx = page.locator('#btn-rescue-custom')
    await expect(btn_custom_rx).to_be_visible()
    await btn_custom_rx.click()
    await page.wait_for_timeout(400)

    # Verify Rule Creator modal opens pre-populated
    modal = page.locator('#mm')
    await expect(modal).to_be_visible()

    tl_val = await page.locator('#e-tl').input_value()
    assert "UNKNOWN_OP" in tl_val

    rx_val = await page.locator('#e-rx').input_value()
    assert len(rx_val) > 5

    # Default name should be pre-populated
    name_val = await page.locator('#e-name').input_value()
    assert len(name_val) > 0

    # Dismiss modal
    await page.locator('#btn-mx').click()
    await expect(modal).not_to_be_visible()

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_onboarding_open_log_file_trigger(blank_page):
    """Clicking Open Log File in the welcome modal dismisses onboarding overlay."""
    page = blank_page
    ob = page.locator('#ob-ov')
    await expect(ob).to_be_visible(timeout=5000)

    btn_open = page.locator('#ob-btn-drop')
    await expect(btn_open).to_be_visible()
    await expect(btn_open).to_contain_text("Open Log File")

    # Clicking should dismiss onboarding overlay
    await btn_open.click()
    await expect(ob).to_be_hidden(timeout=5000)
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_custom_log_auto_sniff_and_synthesize_rules(blank_page):
    """Custom log lines with bracketed timestamp, thread, and level should synthesize accurate rules."""
    page = blank_page
    await page.evaluate(DISMISS_ONBOARDING_JS)

    res = await page.evaluate("""() => {
        const customLines = [
            '[2026-10-08 14:23:45.123] [worker-4] [auth-svc] INFO - User login ok user_id=42',
            '[2026-10-08 14:23:46.456] [worker-4] [auth-svc] INFO - Request started req=101',
            '[2026-10-08 14:23:47.789] [worker-4] [auth-svc] ERROR - DB connection timeout',
            '[2026-10-08 14:23:48.012] [worker-4] [auth-svc] INFO - Response finished req=101'
        ];
        const synth = SNIFFER.synthesizeRules(customLines, 'app-custom.log');
        const rules = synth.config.elementRules;
        const compiled = rules.map(r => new RegExp(r.regexPattern));
        const matchedCount = customLines.filter(l => compiled.some(rx => rx.test(l))).length;

        return {
            rulesCount: rules.length,
            matchedCount,
            totalLines: customLines.length,
            hasPush: rules.some(r => r.stackBehavior === 'push'),
            hasPop: rules.some(r => r.stackBehavior === 'pop'),
            hasInline: rules.some(r => r.stackBehavior === 'inline')
        };
    }""")

    assert res['rulesCount'] >= 4
    assert res['matchedCount'] == res['totalLines'], "All custom lines should match synthesized rules"
    assert res['hasPush'] is True
    assert res['hasPop'] is True
    assert res['hasInline'] is True
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_custom_log_end_to_end_parse_100_percent(blank_page):
    """A custom log file parsed end-to-end should produce structured trees and 100% coverage."""
    page = blank_page
    await page.evaluate(DISMISS_ONBOARDING_JS)

    log_content = (
        "[2026-10-08 14:23:45.123] [worker-4] [auth-svc] INFO - Request started id=101\n"
        "[2026-10-08 14:23:46.456] [worker-4] [auth-svc] INFO - Processing payload\n"
        "[2026-10-08 14:23:47.789] [worker-4] [auth-svc] ERROR - Query timeout\n"
        "[2026-10-08 14:23:48.012] [worker-4] [auth-svc] INFO - Response finished id=101\n"
    )

    res = await page.evaluate(f"""async () => {{
        const lines = `{log_content}`.trim().split('\\n');
        const synth = SNIFFER.synthesizeRules(lines, 'auth-worker.log');
        CFG.load(synth.config);

        const blob = new Blob([`{log_content}`], {{ type: 'text/plain' }});
        const file = new File([blob], 'auth-worker.log', {{ type: 'text/plain' }});
        S.logFile = file;

        const parseRes = await WM.parse(file, S.cfg, '');
        UI.render(parseRes.trees, parseRes.threads, parseRes.stats);
        SNIFFER.checkUnparsedRescue(parseRes.stats);

        return {{
            linesProcessed: parseRes.stats.linesProcessed,
            matchedLines: parseRes.stats.matchedLines,
            threads: parseRes.threads,
            treeNodes: (parseRes.trees['worker-4'] || []).length
        }};
    }}""")

    assert res['linesProcessed'] == 4
    assert res['matchedLines'] == 4, "Should achieve 100% parsing on custom log file"
    assert "worker-4" in res['threads']
    assert res['treeNodes'] > 0

    # Ensure views render without critical errors
    await page.evaluate("() => UI.svm('tree')")
    await page.wait_for_timeout(200)
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(200)
    await page.evaluate("() => UI.svm('split')")
    await page.wait_for_timeout(200)

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_adaptive_rescue_resolve_all_to_100_percent(blank_page):
    """When unparsed lines exist, clicking Resolve All to 100% creates fallback rules and drives coverage to 100%."""
    page = blank_page
    await page.evaluate(DISMISS_ONBOARDING_JS)

    # Simulate parse output with unparsed lines
    await page.evaluate("""() => {
        if (!S.cfg) CFG.load(JSON.parse(JSON.stringify(DEF_CFG)));
        const dummyStats = {
            fileSize: 4000,
            linesProcessed: 50,
            matchedLines: 30, // 40% unparsed
            unparsedSample: [
                '2026-10-08 15:00:00 [srv-1] CUSTOM_EVENT foo=1 bar=2',
                '2026-10-08 15:00:01 [srv-1] CUSTOM_EVENT foo=3 bar=4',
                '2026-10-08 15:00:02 [srv-2] ASYNC_NOTIF code=99'
            ]
        };
        S.stats = dummyStats;
        SNIFFER.checkUnparsedRescue(dummyStats);
    }""")

    # Verify rescue banner is visible with Resolve All button
    banner = page.locator('#rescue-banner')
    await expect(banner).to_be_visible()

    btn_resolve_all = page.locator('#btn-rescue-resolve-all')
    await expect(btn_resolve_all).to_be_visible()
    await expect(btn_resolve_all).to_contain_text("Resolve All to 100%")

    initial_rules_count = await page.evaluate("() => S.cfg.elementRules.length")

    # Click Resolve All to 100%
    await btn_resolve_all.click()
    await page.wait_for_timeout(300)

    # Banner should be dismissed and rules should be added
    await expect(page.locator('#rescue-banner')).not_to_be_visible()
    new_rules_count = await page.evaluate("() => S.cfg.elementRules.length")
    assert new_rules_count > initial_rules_count, "Rules should be added for unparsed clusters"

    # Simulate subsequent 100% parsed result triggering success notification
    await page.evaluate("""() => {
        const fullStats = {
            fileSize: 4000,
            linesProcessed: 50,
            matchedLines: 50,
            unparsedSample: []
        };
        S.stats = fullStats;
        SNIFFER.checkUnparsedRescue(fullStats);
    }""")

    success_banner = page.locator('#rescue-success-banner')
    await expect(success_banner).to_be_visible()
    await expect(success_banner).to_contain_text("100% Rule Coverage Achieved")

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_zero_matched_lines_guidance_card(blank_page):
    """When a custom log has 0 matched lines, UI renders clear setup guidance card instead of empty dead-end."""
    page = blank_page
    await page.evaluate(DISMISS_ONBOARDING_JS)

    # Set up state where lines were processed but 0 matched
    await page.evaluate("""() => {
        S.trees = {};
        S.threads = [];
        S.activeThr = null;
        S.stats = {
            fileSize: 1024,
            linesProcessed: 25,
            matchedLines: 0,
            unparsedSample: ['UNMATCHED 1', 'UNMATCHED 2']
        };
        UI.svm('split');
    }""")

    await page.wait_for_timeout(300)

    # Guidance card should be displayed in the result container
    guidance = page.locator('.emp >> text=Custom Log Format Detected')
    await expect(guidance).to_be_visible()

    btn_resolve = page.locator('#btn-zero-match-resolve')
    await expect(btn_resolve).to_be_visible()
    await expect(btn_resolve).to_contain_text("Auto-Configure Rules")

    btn_custom = page.locator('#btn-zero-match-custom')
    await expect(btn_custom).to_be_visible()

    assert_no_critical_errors(page)
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
