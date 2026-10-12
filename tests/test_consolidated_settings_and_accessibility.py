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

@pytest.mark.asyncio
async def test_settings_appearance_and_sla_guardrails_configuration(page_with_data):
    """Appearance options (mono font, rounded bars, contrast) and SLA guardrails (presets, recalc) configure state and DOM."""
    page = page_with_data
    await page.click('.vt[data-v="cfg"]')

    # 1. Appearance options
    appear_hdr = page.locator('#ss-appear-hdr')
    await expect(appear_hdr).to_be_visible(timeout=3000)
    await appear_hdr.click()

    # Monospace font
    mono_select = page.locator('#pref-mono-font')
    await expect(mono_select).to_be_visible()
    await mono_select.select_option('jetbrains')
    mono_val = await page.evaluate("() => document.documentElement.style.getPropertyValue('--mono')")
    assert 'JetBrains Mono' in mono_val

    # Rounded gantt bars
    rounded_toggle = page.locator('#pref-gantt-rounded')
    await rounded_toggle.evaluate("el => { el.checked = true; el.dispatchEvent(new Event('change')); }")
    has_rounded = await page.evaluate("() => document.body.classList.contains('g-rounded-bars')")
    assert has_rounded, 'document.body should have g-rounded-bars class'

    # High contrast borders
    contrast_toggle = page.locator('#pref-high-contrast')
    await contrast_toggle.evaluate("el => { el.checked = true; el.dispatchEvent(new Event('change')); }")
    has_contrast = await page.evaluate("() => document.body.classList.contains('high-contrast-mode')")
    assert has_contrast, 'document.body should have high-contrast-mode class'

    # 2. SLA & Latency Guardrails
    sla_hdr = page.locator('#ss-sla-hdr')
    await expect(sla_hdr).to_be_visible(timeout=3000)
    await sla_hdr.scroll_into_view_if_needed()
    await sla_hdr.click()

    sla_body = page.locator('#ss-sla-body')
    await expect(sla_body).to_be_visible(timeout=3000)

    # Click 500ms preset button
    preset_500 = page.locator('.sla-preset-btn[data-sla="500"]')
    await preset_500.scroll_into_view_if_needed()
    await preset_500.click()

    # Verify input updated to 500
    sla_input = page.locator('#pref-global-sla')
    assert await sla_input.input_value() == '500'
    assert await page.evaluate("() => S.globalSlaThresholdMs") == 500

    # Click Recalculate button
    recalc_btn = page.locator('#btn-sla-recalc')
    await recalc_btn.scroll_into_view_if_needed()
    await recalc_btn.click()

    # Verify summary text updated
    summary = page.locator('#sla-recalc-summary')
    await expect(summary).to_be_visible()
    summary_text = await summary.inner_text()
    assert 'Active breaches' in summary_text

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_theme_studio_drawer_filtering_and_theme_switching(page_with_data):
    """Theme Studio opens, renders 10 themes, tabs filter by All/Dark/Light, and all themes apply cleanly."""
    page = page_with_data
    # 1. Open Theme Studio
    await page.evaluate("() => Theme.openPicker()")
    picker = page.locator('#theme-picker-menu')
    await expect(picker).to_have_class(re.compile(r'tp-open'))

    # 2. Check total swatch count under 'All' tab
    swatches = page.locator('.th-swatch')
    assert await swatches.count() == 10

    # 3. Check filter tabs
    tab_dark = page.locator('.tp-tab-btn:has-text("Dark")')
    await tab_dark.click()
    dark_swatches = page.locator('.th-swatch')
    assert await dark_swatches.count() == 5

    tab_light = page.locator('.tp-tab-btn:has-text("Light")')
    await tab_light.click()
    light_swatches = page.locator('.th-swatch')
    assert await light_swatches.count() == 5

    # 4. Apply a light theme (nordic)
    await page.evaluate("() => Theme.apply('nordic')")
    theme_val = await page.evaluate("() => document.documentElement.dataset.theme")
    theme_type = await page.evaluate("() => document.documentElement.dataset.themeType")
    assert theme_val == 'nordic'
    assert theme_type == 'light'

    # 5. Apply another light theme (blueprint)
    await page.evaluate("() => Theme.apply('blueprint')")
    theme_val = await page.evaluate("() => document.documentElement.dataset.theme")
    assert theme_val == 'blueprint'

    # 6. Apply dark theme (obsidian / dark)
    await page.evaluate("() => Theme.apply('dark')")
    theme_val = await page.evaluate("() => document.documentElement.dataset.theme")
    theme_type = await page.evaluate("() => document.documentElement.dataset.themeType")
    assert theme_val == 'dark'
    assert theme_type == 'dark'

    # 7. Apply midnight theme and verify calibrated high-contrast borders
    await page.evaluate("() => Theme.apply('midnight')")
    assert await page.evaluate("() => document.documentElement.dataset.theme") == 'midnight'
    bdr_val = await page.evaluate("() => getComputedStyle(document.documentElement).getPropertyValue('--bdr').trim()")
    assert '29%' in bdr_val or 'oklch' in bdr_val

    # Close picker
    await page.evaluate("() => Theme.closePicker()")
    await expect(picker).not_to_have_class(re.compile(r'tp-open'))

    assert_no_critical_errors(page)


