"""
test_09_ai_insights.py — LogLens Regression Suite
Tests: AI Insights card rendering, severity items, ARIA, finding count.
Covers Phase 8 (AI_INSIGHTS heuristic engine).
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_ai_insights_card_visible_in_stats(page_with_data):
    """AI Insights card must be visible when Stats view is rendered with data."""
    page = page_with_data
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(800)
    await expect(page.locator('.ai-insights-card')).to_be_visible(timeout=5000)


@pytest.mark.asyncio
async def test_ai_insights_header_text(page_with_data):
    """AI Insights card header must contain 'AI Insights'."""
    page = page_with_data
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(800)
    hdr = await page.locator('.ai-insights-hdr').inner_text()
    assert 'AI Insights' in hdr, f'Header text missing, got: {hdr}'


@pytest.mark.asyncio
async def test_ai_insights_badge_present(page_with_data):
    """Heuristic badge (.ai-badge) must be visible."""
    page = page_with_data
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(800)
    await expect(page.locator('.ai-badge')).to_be_visible(timeout=3000)
    text = await page.locator('.ai-badge').inner_text()
    assert 'heuristic' in text.lower(), f'Badge should say Heuristic, got: {text}'


@pytest.mark.asyncio
async def test_ai_insights_minimum_items(page_with_data):
    """At least 2 .ai-insight-item elements must be rendered with synthetic data."""
    page = page_with_data
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(800)
    count = await page.locator('.ai-insight-item').count()
    assert count >= 2, f'Expected at least 2 insight items, got {count}'


@pytest.mark.asyncio
async def test_ai_insights_severity_classes(page_with_data):
    """At least one severity class (sev-warn/sev-error/sev-ok/sev-info) must be present."""
    page = page_with_data
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(800)
    body_html = await page.locator('.ai-insights-body').inner_html()
    has_sev = any(cls in body_html for cls in ['sev-warn', 'sev-error', 'sev-ok', 'sev-info'])
    assert has_sev, 'No severity class found on insight items'


@pytest.mark.asyncio
async def test_ai_insights_aria_region(page_with_data):
    """AI Insights card must have role=region and aria-label."""
    page = page_with_data
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(800)
    card = page.locator('.ai-insights-card')
    assert await card.get_attribute('role') == 'region'
    label = await card.get_attribute('aria-label')
    assert label and 'Insights' in label


@pytest.mark.asyncio
async def test_ai_insights_findings_count_label(page_with_data):
    """Header must show a 'N findings' count label."""
    page = page_with_data
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(800)
    # Last span in header holds the count
    spans = page.locator('.ai-insights-hdr span')
    last_text = await spans.last.inner_text()
    assert 'finding' in last_text.lower(), f'Finding count label missing, got: {last_text}'


@pytest.mark.asyncio
async def test_ai_insights_empty_when_no_data(blank_page):
    """With no data, card must show the empty-state message."""
    page = blank_page
    from conftest import DISMISS_ONBOARDING_JS
    await page.evaluate(DISMISS_ONBOARDING_JS)
    # Navigate to stats with no S.trees
    await page.evaluate("() => { S.trees = null; if (typeof UI !== 'undefined') UI.svm('stats'); }")
    await page.wait_for_timeout(800)
    card = page.locator('.ai-insights-card')
    if await card.count() > 0:
        empty = page.locator('.ai-insights-empty')
        await expect(empty).to_be_visible(timeout=3000)


@pytest.mark.asyncio
async def test_ai_insights_no_errors(page_with_data):
    """AI_INSIGHTS module must emit no critical JS errors."""
    page = page_with_data
    await page.evaluate("() => UI.svm('stats')")
    await page.wait_for_timeout(800)
    assert_no_critical_errors(page, keywords=['TypeError', 'ReferenceError', 'AI_INSIGHTS'])
