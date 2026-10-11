"""
test_05_event_inspector.py — LogLens Regression Suite
Tests: Event Inspector open/close on tree row click, content verification, Escape dismiss, auto close on nav/thread/empty canvas.
Covers Phase 3 (Event Inspector side drawer).
Consolidated for high-speed regression verification.
"""
import re
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_event_inspector_lifecycle_and_metadata(page_with_data):
    """Event Inspector opens on row click, displays metadata, and closes via button or Escape key."""
    page = page_with_data
    inspector = page.locator('#event-inspector')
    assert not await inspector.is_visible(), 'Inspector should be hidden on load'

    # Open via row click
    await page.evaluate("() => UI.svm('tree')")
    first_row = page.locator('.tree-row').first
    await first_row.wait_for(state='visible', timeout=5000)
    await first_row.click()
    await expect(inspector).to_be_visible(timeout=3000)

    # Verify metadata fields
    body = await page.locator('#ins-body-content').text_content()
    assert 'Rule Name' in body, 'Inspector body should show Rule Name field'
    assert 'Thread' in body, 'Inspector body should show Thread field'

    # Close via button
    await page.click('#btn-ins-close')
    await expect(inspector).not_to_be_visible(timeout=2000)

    # Re-open and close via Escape
    await first_row.click()
    await expect(inspector).to_be_visible(timeout=2000)
    await page.keyboard.press('Escape')
    await expect(inspector).not_to_be_visible(timeout=2000)

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_event_inspector_auto_close_conditions(page_with_data):
    """Event Inspector auto-closes on view navigation, thread switch, and empty canvas click."""
    page = page_with_data
    inspector = page.locator('#event-inspector')

    # 1. Navigating to non-event view (settings)
    await page.evaluate("() => UI.svm('tree')")
    first_row = page.locator('.tree-row').first
    await first_row.wait_for(state='visible', timeout=5000)
    await first_row.click()
    await expect(inspector).to_be_visible(timeout=3000)

    await page.evaluate("() => UI.svm('cfg')")
    await expect(inspector).not_to_be_visible(timeout=2000)

    # 2. Thread switch
    await page.evaluate("() => { UI.svm('tree'); UI.sw('main'); }")
    await first_row.click()
    await expect(inspector).to_be_visible(timeout=2000)

    await page.evaluate("() => UI.sw('worker')")
    await expect(inspector).not_to_be_visible(timeout=2000)

    # 3. Empty canvas click
    await page.evaluate("() => UI.svm('tree')")
    await first_row.click()
    await expect(inspector).to_be_visible(timeout=2000)
    await expect(first_row).to_have_class(re.compile(r'kb-focus'))

    await page.evaluate("""() => {
        const vscroll = document.getElementById('tree-vscroll');
        if (vscroll) {
            vscroll.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
        }
    }""")
    await expect(inspector).not_to_be_visible(timeout=2000)
    assert await page.locator('.tree-row.kb-focus').count() == 0

    assert_no_critical_errors(page)
