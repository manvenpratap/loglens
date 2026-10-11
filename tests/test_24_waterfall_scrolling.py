"""
test_24_waterfall_scrolling.py — LogLens Regression Suite
Tests: Waterfall (Gantt) mode vertical and horizontal scrolling, container layout, and header sync.
Covers:
- View container flex constraints and overflow isolation (res overflow-y: hidden, gw bounded height).
- Vertical mouse wheel scrolling within .g-rows without page displacement.
- Horizontal timeline scrolling with automatic header (.g-hdr) alignment synchronization.
- Keyboard arrow navigation and focusability (tabindex="0").
- Rapid tab switching stability and zero critical runtime errors.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


@pytest.mark.asyncio
async def test_waterfall_container_dimensions_and_overflow(page_with_data):
    """Waterfall view must constrain .gw within viewport, keeping header/toolbar/nav visible and .g-rows scrollable."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(400)

    # 1. Outer container #res must have overflow-y: hidden to isolate view scrolling
    res_overflow = await page.evaluate("() => document.getElementById('res').style.overflowY")
    assert res_overflow == 'hidden', f"Expected #res style.overflowY to be 'hidden', got '{res_overflow}'"

    # 2. .gw must be bounded within viewport (not expanding to thousands of pixels)
    gw_height, res_height = await page.evaluate("""() => [
        document.querySelector('.gw').clientHeight,
        document.getElementById('res').clientHeight
    ]""")
    assert gw_height <= res_height, f".gw height ({gw_height}px) must be bounded by #res ({res_height}px)"

    # 3. .g-rows must have scrollable content (scrollHeight > clientHeight)
    can_scroll, client_h, scroll_h = await page.evaluate("""() => {
        const rows = document.querySelector('.g-rows');
        return [rows.scrollHeight > rows.clientHeight, rows.clientHeight, rows.scrollHeight];
    }""")
    assert can_scroll is True, f".g-rows must have scrollable content: clientHeight={client_h}, scrollHeight={scroll_h}"

    # 4. Toolbar and Timeline Navigator must be attached and visible
    await expect(page.locator('.g-toolbar')).to_be_visible()
    await expect(page.locator('.g-hdr')).to_be_visible()
    await expect(page.locator('.tl-nav-wrap')).to_be_visible()

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_waterfall_vertical_wheel_scrolling(page_with_data):
    """Mouse wheel scrolling over .g-rows must increase scrollTop while keeping #res at scrollTop 0."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(400)

    # Move mouse over .g-rows
    box = await page.locator('.g-rows').bounding_box()
    assert box is not None, ".g-rows bounding box should exist"
    await page.mouse.move(box['x'] + 120, box['y'] + 120)

    # Dispatch mouse wheel scroll
    await page.mouse.wheel(0, 300)
    await page.wait_for_timeout(300)

    rows_scroll_top, res_scroll_top = await page.evaluate("""() => [
        document.querySelector('.g-rows').scrollTop,
        document.getElementById('res').scrollTop
    ]""")
    assert rows_scroll_top > 0, f"Expected .g-rows scrollTop > 0 after wheel, got {rows_scroll_top}"
    assert res_scroll_top == 0, f"#res scrollTop must remain 0 to prevent toolbar displacement, got {res_scroll_top}"

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_waterfall_horizontal_scrolling_and_header_sync(page_with_data):
    """Horizontal scrolling on .g-rows must automatically sync the time axis header (.g-hdr) scroll position."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(400)

    # 1. Zoom in 2x to create horizontal overflow
    await page.evaluate("() => GANTT_ZOOM_PAN.applyZoom(2)")
    await page.wait_for_timeout(250)

    # 2. Scroll .g-rows horizontally
    target_left = 180
    await page.evaluate(f"() => {{ document.querySelector('.g-rows').scrollLeft = {target_left}; }}")
    await page.wait_for_timeout(250)

    rows_left, hdr_left = await page.evaluate("""() => [
        document.querySelector('.g-rows').scrollLeft,
        document.querySelector('.g-hdr').scrollLeft
    ]""")
    assert rows_left == target_left, f"Expected rows scrollLeft == {target_left}, got {rows_left}"
    assert hdr_left == rows_left, f"Header scrollLeft ({hdr_left}) must match rows scrollLeft ({rows_left})"

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_waterfall_keyboard_scrolling(page_with_data):
    """Focusing .g-rows and pressing ArrowDown must scroll the waterfall rows vertically."""
    page = page_with_data
    await page.evaluate("() => UI.svm('gantt')")
    await page.wait_for_timeout(400)

    # 1. Verify tabindex and focus
    tabindex = await page.locator('.g-rows').get_attribute('tabindex')
    assert tabindex == '0', f"Expected .g-rows tabindex='0', got {tabindex}"

    await page.evaluate("() => document.querySelector('.g-rows').focus()")
    await page.wait_for_timeout(100)

    # 2. Press ArrowDown multiple times
    for _ in range(4):
        await page.keyboard.press('ArrowDown')
        await page.wait_for_timeout(60)

    scroll_top = await page.evaluate("() => document.querySelector('.g-rows').scrollTop")
    assert scroll_top > 0, f"Expected keyboard ArrowDown to scroll rows (scrollTop > 0), got {scroll_top}"

    assert_no_critical_errors(page)


@pytest.mark.asyncio
async def test_waterfall_rapid_tab_switching_scroll_stability(page_with_data):
    """Switching between Split, Tree, Waterfall, and Trace views retains correct scrollability in Waterfall mode."""
    page = page_with_data

    views = ['split', 'tree', 'gantt', 'trace', 'gantt']
    for v in views:
        await page.evaluate(f"() => UI.svm('{v}')")
        await page.wait_for_timeout(150)

    # Final verification on Waterfall mode
    state = await page.evaluate("""() => {
        const rows = document.querySelector('.g-rows');
        const res = document.getElementById('res');
        return {
            resOverflowY: res.style.overflowY,
            canScroll: rows ? rows.scrollHeight > rows.clientHeight : false,
            hasHdr: document.querySelector('.g-hdr') !== null
        };
    }""")
    assert state['resOverflowY'] == 'hidden'
    assert state['canScroll'] is True
    assert state['hasHdr'] is True

    assert_no_critical_errors(page)
