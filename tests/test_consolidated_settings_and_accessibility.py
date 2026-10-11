"""
test_consolidated_settings_and_accessibility.py — Consolidated Regression Test Suite
Merges and deduplicates tests from: test_06_settings_preferences.py, test_09_ai_insights.py, test_10_focus_mode.py, test_11_accessibility.py
"""
import os
import re
import json
import tempfile
import pytest
import asyncio
from playwright.async_api import expect, Page
from conftest import APP_URL, DISMISS_ONBOARDING_JS, DEMO_TREES_JS, assert_no_critical_errors

re_pattern = re.compile(r'focus-mode')

@pytest.mark.asyncio
async def test_settings_panel_and_preferences_accordions(page_with_data):
    """Settings panel renders as flex container, houses preferences card, and expands Performance/Appearance accordions."""
    page = page_with_data
    await page.click('.vt[data-v="cfg"]')

    # Panel visible and flex
    cfg_panel = page.locator('#p-cfg')
    await expect(cfg_panel).to_be_visible(timeout=3000)
    display = await page.evaluate("() => getComputedStyle(document.getElementById('p-cfg')).display")
    assert display == 'flex', f'Expected flex, got {display}'

    # Preferences card visible
    await expect(page.locator('#p-gs')).to_be_visible(timeout=3000)

    # Performance accordion expansion
    perf_hdr = page.locator('#ss-perf-hdr')
    await expect(perf_hdr).to_be_visible(timeout=3000)
    await perf_hdr.click()
    perf_body = page.locator('#ss-perf-body')
    await expect(perf_body).to_be_visible(timeout=3000)
    perf_disp = await page.evaluate("() => getComputedStyle(document.getElementById('ss-perf-body')).display")
    assert perf_disp == 'flex', f'Performance body should be flex, got {perf_disp}'

    # Appearance accordion expansion
    appear_hdr = page.locator('#ss-appear-hdr')
    await expect(appear_hdr).to_be_visible(timeout=3000)
    await appear_hdr.click()
    appear_body = page.locator('#ss-appear-body')
    await expect(appear_body).to_be_visible(timeout=3000)
    appear_disp = await page.evaluate("() => getComputedStyle(document.getElementById('ss-appear-body')).display")
    assert appear_disp == 'flex', f'Appearance body should be flex, got {appear_disp}'

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_ai_insights_card_rendering_and_metadata(page_with_data):
    """AI Insights card renders in Stats view with valid header, badge, items, ARIA, and severities."""
    page = page_with_data
    await page.evaluate("() => UI.svm('stats')")
    card = page.locator('.ai-insights-card')
    await expect(card).to_be_visible(timeout=4000)

    # Header and badge
    hdr = await page.locator('.ai-insights-hdr').inner_text()
    assert 'AI Insights' in hdr, f'Header text missing, got: {hdr}'

    badge = page.locator('.ai-badge')
    await expect(badge).to_be_visible(timeout=2000)
    badge_text = await badge.inner_text()
    assert 'heuristic' in badge_text.lower(), f'Badge should say Heuristic, got: {badge_text}'

    # Items and severity
    count = await page.locator('.ai-insight-item').count()
    assert count >= 2, f'Expected at least 2 insight items, got {count}'

    body_html = await page.locator('.ai-insights-body').inner_html()
    has_sev = any(cls in body_html for cls in ['sev-warn', 'sev-error', 'sev-ok', 'sev-info'])
    assert has_sev, 'No severity class found on insight items'

    # ARIA metadata
    assert await card.get_attribute('role') == 'region'
    label = await card.get_attribute('aria-label')
    assert label and 'Insights' in label

    # Findings count label
    spans = page.locator('.ai-insights-hdr span')
    last_text = await spans.last.inner_text()
    assert 'finding' in last_text.lower(), f'Finding count label missing, got: {last_text}'

    assert_no_critical_errors(page, keywords=['TypeError', 'ReferenceError', 'AI_INSIGHTS'])
@pytest.mark.asyncio
async def test_ai_insights_empty_when_no_data(blank_page):
    """With no data, card must show the empty-state message."""
    page = blank_page
    await page.evaluate(DISMISS_ONBOARDING_JS)
    await page.evaluate("() => { S.trees = null; if (typeof UI !== 'undefined') UI.svm('stats'); }")
    card = page.locator('.ai-insights-card')
    if await card.count() > 0:
        empty = page.locator('.ai-insights-empty')
        await expect(empty).to_be_visible(timeout=3000)
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_focus_mode_toggle_cycle_and_storage(page_with_data):
    """F-key toggle cycle activates focus mode, updates DOM/storage, and deactivates cleanly on second press."""
    page = page_with_data

    # 1. Inactive on load
    has_fm = await page.evaluate("() => document.body.classList.contains('focus-mode')")
    assert not has_fm, 'focus-mode should not be active on load'

    # 2. Press F to activate
    await page.keyboard.press('f')
    await page.wait_for_timeout(300)
    assert await page.evaluate("() => document.body.classList.contains('focus-mode')")

    # Toast validation
    toast = page.locator('#focus-mode-toast')
    await expect(toast).to_be_visible(timeout=2000)
    assert 'Focus Mode ON' in (await toast.inner_text())
    assert await toast.get_attribute('role') == 'status'

    # Sidebar hidden
    sidebar = page.locator('.sb')
    if await sidebar.count() > 0:
        display = await sidebar.evaluate("el => getComputedStyle(el).display")
        assert display == 'none', f'Sidebar should be none in focus mode, got {display}'

    # sessionStorage tracking
    assert await page.evaluate("() => sessionStorage.getItem('ll_focus_mode')") == '1'

    # 3. Press F second time to deactivate
    await page.keyboard.press('f')
    await page.wait_for_function("() => !document.body.classList.contains('focus-mode')")
    assert 'Focus Mode OFF' in (await toast.inner_text())
    assert await page.evaluate("() => sessionStorage.getItem('ll_focus_mode')") == '0'

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_focus_mode_input_isolation(page_with_data):
    """F key must NOT activate focus mode when typed into an input field."""
    page = page_with_data
    await page.focus('#hdr-search')
    await page.keyboard.type('f')
    await page.wait_for_timeout(100)

    has_fm = await page.evaluate("() => document.body.classList.contains('focus-mode')")
    assert not has_fm, 'Typing F into search input should not trigger focus mode'
    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_skip_link_and_live_regions(page_with_data):
    """Skip-to-content link, main target #res, and live region ARIA attributes are compliant."""
    page = page_with_data

    # Skip link
    skip = page.locator('#skip-link')
    await expect(skip).to_be_attached()
    assert await skip.get_attribute('href') == '#res'
    cls = await skip.get_attribute('class')
    assert 'skip-link' in (cls or '')

    # Main content target #res
    await expect(page.locator('#res')).to_be_attached()

    # Toast live region attributes
    toast = page.locator('#toast')
    if await toast.count() > 0:
        al = await toast.get_attribute('aria-live')
        assert al in ('polite', 'assertive'), f'#toast aria-live should be polite, got {al}'
        aa = await toast.get_attribute('aria-atomic')
        assert aa == 'true', f'#toast aria-atomic should be true, got {aa}'

    # Focus mode toast role=status
    await page.keyboard.press('f')
    fm_toast = page.locator('#focus-mode-toast')
    await expect(fm_toast).to_be_attached()
    assert await fm_toast.get_attribute('role') == 'status'
    await page.keyboard.press('f')

    assert_no_critical_errors(page)
@pytest.mark.asyncio
async def test_interactive_component_accessibility(page_with_data):
    """Timeline chips have role=switch and AI insight items have tabindex=0 for keyboard accessibility."""
    page = page_with_data

    # Timeline chips ARIA
    await page.evaluate("() => UI.svm('gantt')")
    chips = page.locator('.tl-overlay-chip')
    await chips.first.wait_for(state='attached', timeout=5000)
    assert await chips.first.get_attribute('role') == 'switch'
    assert (await chips.first.get_attribute('aria-checked')) in ('true', 'false')

    # AI Insight items tabindex=0
    await page.evaluate("() => UI.svm('stats')")
    items = page.locator('.ai-insight-item')
    await items.first.wait_for(state='attached', timeout=5000)
    assert await items.first.get_attribute('tabindex') == '0'

    assert_no_critical_errors(page)
