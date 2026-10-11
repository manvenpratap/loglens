"""
test_11_accessibility.py — LogLens Regression Suite
Tests: Skip link, ARIA live regions, component ARIA roles, keyboard accessibility.
Covers Phase 11 (A11y Polish).
Consolidated for high-speed regression verification.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


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
