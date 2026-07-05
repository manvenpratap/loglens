"""
test_15_regex_undo_redo.py — LogLens Regression Suite
Tests: Undo and Redo options while editing a regex pattern in the Rule Creator.
"""
import pytest
from playwright.async_api import expect
from conftest import assert_no_critical_errors


async def _load_settings_and_open_modal(page):
    """Helper: open the Settings tab and click Add Rule."""
    await page.evaluate("() => { if (S.cfg === null) CFG.load(JSON.parse(JSON.stringify(DEF_CFG))); }")
    await page.evaluate("() => UI.svm('cfg')")
    await page.wait_for_timeout(500)
    await page.click('#btn-ar')
    await page.wait_for_timeout(400)


@pytest.mark.asyncio
async def test_regex_undo_redo_functionality(page_with_data):
    """Undo and Redo buttons must change the regex pattern text value and follow history states."""
    page = page_with_data
    await _load_settings_and_open_modal(page)

    # 1. Expand advanced accordion to view the regex pattern textarea
    await page.click('#adv-hdr')
    await page.wait_for_timeout(300)

    # 2. Check that buttons exist
    btn_undo = page.locator('#btn-rx-undo')
    btn_redo = page.locator('#btn-rx-redo')
    e_rx = page.locator('#e-rx')
    chk_custom = page.locator('#e-use-custom-rx')

    # Initially both should be disabled
    await expect(btn_undo).to_be_disabled()
    await expect(btn_redo).to_be_disabled()

    # Enable custom regex pattern mode to unlock editing on e-rx
    await chk_custom.check()
    await page.wait_for_timeout(300)

    # Undo might be enabled here if checking custom auto-filled a wizard pattern.
    # Let's read the value after check.
    val_initial = await e_rx.input_value()

    # 3. Focus on regex input and type something different
    await e_rx.focus()
    await e_rx.fill("hello")
    # Dispatch manual input event
    await page.evaluate("() => document.getElementById('e-rx').dispatchEvent(new Event('input', { bubbles: true }))")
    await page.wait_for_timeout(300)

    # Undo should definitely be enabled now
    await expect(btn_undo).to_be_enabled()

    # 4. Perform Undo
    await btn_undo.click()
    await page.wait_for_timeout(300)

    # Value should go back to the state before "hello" (e.g. empty or auto-filled pattern)
    val_after_undo = await e_rx.input_value()
    assert val_after_undo == val_initial
    await expect(btn_redo).to_be_enabled()

    # 5. Perform Redo
    await btn_redo.click()
    await page.wait_for_timeout(300)

    # Value should restore to "hello"
    val_after_redo = await e_rx.input_value()
    assert val_after_redo == "hello"
    await expect(btn_redo).to_be_disabled()

    # Ensure no critical console errors occurred
    assert_no_critical_errors(page)
