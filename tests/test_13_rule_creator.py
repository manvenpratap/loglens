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
    await page.click('.vt[data-v="cfg"]')
    await page.wait_for_timeout(500)


@pytest.mark.asyncio
async def test_rule_creator_unified_modal(page_with_data):
    """Rule creator modal must not have mode tabs, and must show steps and advanced accordion."""
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

    # 3. Assert mode tabs (.m-tog, mb-g, mb-a) do NOT exist on the modal
    mb_g = page.locator('#mb-g')
    mb_a = page.locator('#mb-a')
    await expect(mb_g).not_to_be_visible()
    await expect(mb_a).not_to_be_visible()

    # 4. Check unified layout steps are visible
    step_1 = page.locator('.ws-step >> text=Select Log Format')
    step_2 = page.locator('.ws-step >> text=Keywords / Markers')
    step_3 = page.locator('.ws-step >> text=Live Match Preview & Test')
    await expect(step_1).to_be_visible()
    await expect(step_2).to_be_visible()
    await expect(step_3).to_be_visible()

    # 5. Check collapsible advanced section header is visible
    adv_hdr = page.locator('#adv-hdr')
    await expect(adv_hdr).to_be_visible()

    # Check that advanced body starts collapsed/hidden
    adv_body = page.locator('#adv-body')
    await expect(adv_body).to_have_class("adv-section-body hidden")

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
    """Advanced accordion must expand/collapse, toggle custom regex checkbox, and update field states."""
    page = page_with_data
    await _load_settings(page)

    await page.click('#btn-ar')
    await page.wait_for_timeout(400)

    adv_hdr = page.locator('#adv-hdr')
    adv_body = page.locator('#adv-body')
    chk_custom = page.locator('#e-use-custom-rx')
    inp_rx = page.locator('#e-rx')

    # 1. Expand accordion
    await adv_hdr.click()
    await page.wait_for_timeout(300)
    await expect(adv_body).not_to_have_class("adv-section-body hidden")
    await expect(chk_custom).to_be_visible()

    # By default, custom regex is unchecked, and e-rx is disabled
    is_checked = await chk_custom.is_checked()
    assert not is_checked, "Custom regex checkbox should be unchecked by default"
    await expect(inp_rx).to_be_disabled()

    # 2. Check Custom Regex Checkbox -> Enables the inputs
    await chk_custom.click()
    await page.wait_for_timeout(300)
    assert await chk_custom.is_checked()
    await expect(inp_rx).not_to_be_disabled()

    # 3. Mappings inputs must also be enabled
    await expect(page.locator('#cm-ts')).not_to_be_disabled()
    await expect(page.locator('#cm-th')).not_to_be_disabled()
    await expect(page.locator('#cm-el')).not_to_be_disabled()

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

    # Select Java Standard format (default)
    await page.select_option('#wf-sel', 'java_std')

    # Add keyword
    await page.fill('#kw-inp', 'GET')
    await page.click('#btn-kw')
    await page.wait_for_timeout(300)

    # Verify chip exists
    await expect(page.locator('#kw-chips')).to_contain_text("GET")

    # Fill sample log line
    test_line = "2026-07-03 08:30:15,123 INFO  [http-nio-8080-exec-1] com.example.Controller - GET /items"
    await page.fill('#e-tl', test_line)
    await page.wait_for_timeout(300)

    # Check that rx-pre highlights the matched tokens.
    # Because java_std defines capture group 1 (timestamp) and group 2 (thread).
    # Group 1 should capture '2026-07-03 08:30:15,123'
    # Group 2 should capture 'http-nio-8080-exec-1'
    # Group 3 is not defined by default, but let's check that group 1 and 2 highlight buttons exist
    grp_1 = page.locator('.rx-ln span.rx-grp-btn[data-gi="1"]')
    grp_2 = page.locator('.rx-ln span.rx-grp-btn[data-gi="2"]')
    await expect(grp_1).to_be_visible()
    await expect(grp_2).to_be_visible()

    # Assert no critical errors
    assert_no_critical_errors(page)
