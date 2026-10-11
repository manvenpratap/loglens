"""
test_09_ai_insights.py — LogLens Regression Suite
Tests: AI Insights card rendering, severity items, ARIA, finding count, empty state.
Covers Phase 8 (AI_INSIGHTS heuristic engine).
Consolidated for high-speed regression verification.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors, DISMISS_ONBOARDING_JS


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
