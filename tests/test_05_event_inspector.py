"""
test_05_event_inspector.py — LogLens Regression Suite
Tests: Event Inspector open/close on tree row click, content verification, Escape dismiss.
Covers Phase 3 (Event Inspector side drawer).
"""
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_event_inspector_hidden_initially(page_with_data):
    """Event Inspector must be hidden before a row is clicked."""
    page = page_with_data
    inspector = page.locator('#event-inspector')
    assert not await inspector.is_visible(), 'Inspector should be hidden on load'


@pytest.mark.asyncio
async def test_event_inspector_opens_on_tree_row_click(page_with_data):
    """Clicking a tree row must open the Event Inspector."""
    page = page_with_data
    await page.evaluate("() => UI.svm('tree')")
    await page.wait_for_timeout(400)

    first_row = page.locator('.tree-row').first
    await first_row.wait_for(state='visible', timeout=5000)
    await first_row.click()
    await page.wait_for_timeout(400)

    inspector = page.locator('#event-inspector')
    await expect(inspector).to_be_visible(timeout=3000)


@pytest.mark.asyncio
async def test_event_inspector_shows_metadata(page_with_data):
    """Inspector body must contain Rule Name and Thread fields."""
    page = page_with_data
    await page.evaluate("() => UI.svm('tree')")
    await page.wait_for_timeout(400)

    await page.locator('.tree-row').first.click()
    await page.wait_for_timeout(400)

    body = await page.locator('#ins-body-content').text_content()
    assert 'Rule Name' in body, 'Inspector body should show Rule Name field'
    assert 'Thread' in body, 'Inspector body should show Thread field'


@pytest.mark.asyncio
async def test_event_inspector_closes_on_button_click(page_with_data):
    """Clicking the close button must hide the Inspector."""
    page = page_with_data
    await page.evaluate("() => UI.svm('tree')")
    await page.wait_for_timeout(400)

    await page.locator('.tree-row').first.click()
    await page.wait_for_timeout(300)

    await page.click('#btn-ins-close')
    await page.wait_for_timeout(300)
    assert not await page.locator('#event-inspector').is_visible(), \
        'Inspector should close after clicking close button'


@pytest.mark.asyncio
async def test_event_inspector_closes_on_escape(page_with_data):
    """Pressing Escape must close the Event Inspector."""
    page = page_with_data
    await page.evaluate("() => UI.svm('tree')")
    await page.wait_for_timeout(400)

    await page.locator('.tree-row').first.click()
    await page.wait_for_timeout(300)

    await page.keyboard.press('Escape')
    await page.wait_for_timeout(300)
    assert not await page.locator('#event-inspector').is_visible(), \
        'Inspector should close on Escape'
