"""
test_13_rule_creator.py — LogLens Regression Suite
Tests: Unified Elements Rule Creator modal and contextual helper tooltip popovers.
Covers: single-view merger, custom regex check state, collapsible advanced accordion,
and tooltip helpers.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


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
