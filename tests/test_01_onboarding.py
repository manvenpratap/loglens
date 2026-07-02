"""
test_01_onboarding.py — LogLens Regression Suite
Tests: Onboarding overlay visibility, Demo load flow, empty-state first-run guide.
Covers Phase 1 (Onboarding), Phase 10 (First-Run UX).
"""
import pytest
from playwright.async_api import expect
from conftest import APP_URL, DISMISS_ONBOARDING_JS


@pytest.mark.asyncio
async def test_onboarding_overlay_shown_on_load(blank_page):
    """Onboarding overlay must be visible before any interaction."""
    ob = blank_page.locator('#ob-ov')
    await expect(ob).to_be_visible(timeout=5000)


@pytest.mark.asyncio
async def test_demo_load_dismisses_onboarding(blank_page):
    """Clicking Try Demo loads data and hides the onboarding overlay."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await expect(demo_btn).to_be_visible(timeout=5000)
    await demo_btn.click()
    await expect(page.locator('#ob-ov')).to_be_hidden(timeout=15000)
    await expect(page.locator('#stats-bar')).to_be_visible(timeout=15000)


@pytest.mark.asyncio
async def test_result_container_visible_after_demo(blank_page):
    """#res container must be visible after demo loads."""
    page = blank_page
    demo_btn = page.locator('#ob-btn-demo')
    await demo_btn.wait_for(state='visible', timeout=5000)
    await demo_btn.click()
    await page.wait_for_selector('#stats-bar', state='visible', timeout=15000)
    await expect(page.locator('#res')).to_be_visible()


@pytest.mark.asyncio
async def test_empty_state_guide_injected(blank_page):
    """
    With no data and onboarding dismissed, navigating to gantt should show
    the #emp empty state enriched with the 3-step guide (Phase 10).
    """
    page = blank_page
    # Dismiss onboarding without loading data
    await page.evaluate(DISMISS_ONBOARDING_JS)
    # Switch to gantt view (no data)
    await page.evaluate("() => { if (typeof UI !== 'undefined') UI.svm('gantt'); }")
    await page.wait_for_timeout(400)

    emp = page.locator('#emp')
    await expect(emp).to_be_visible(timeout=3000)

    # Guide should be injected by Phase 10 patch
    guide = page.locator('.emp-guide')
    await expect(guide).to_be_visible(timeout=3000)

    steps = page.locator('.emp-guide-step')
    assert await steps.count() == 3, 'Expect exactly 3 step cards in guide'


@pytest.mark.asyncio
async def test_empty_state_shortcuts_strip(blank_page):
    """Shortcut hint chips must render in the first-run guide."""
    page = blank_page
    await page.evaluate(DISMISS_ONBOARDING_JS)
    await page.evaluate("() => { if (typeof UI !== 'undefined') UI.svm('gantt'); }")
    await page.wait_for_timeout(400)

    shortcuts = page.locator('.emp-shortcut')
    count = await shortcuts.count()
    assert count >= 3, f'Expected at least 3 shortcut chips, got {count}'
