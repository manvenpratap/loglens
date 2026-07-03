"""
test_12_log4j_import.py — LogLens Regression Suite
Tests: Log4j XML importing, inline result visibility, preview modal overlay rendering,
and automatic default configuration fallback initialization when S.cfg is null.
"""
import os
import tempfile
import pytest
from playwright.async_api import expect
from conftest import DISMISS_ONBOARDING_JS, assert_no_critical_errors


@pytest.mark.asyncio
async def test_log4j_import_inline_and_empty_config(blank_page):
    """
    Importing a log4j XML file in an empty configuration state must:
    1. Populate the inline `#lj-res` container under the import button.
    2. Auto-initialize S.cfg with defaults if currently null.
    3. Import the selected appenders successfully and update the rules view.
    """
    page = blank_page

    # 1. Dismiss onboarding via the skip button to expose the Settings view
    btn_skip = page.locator('#ob-skip')
    await expect(btn_skip).to_be_visible()
    await btn_skip.click()
    await page.wait_for_timeout(500)

    # Verify that the Settings panel is visible
    p_cfg = page.locator('#p-cfg')
    await expect(p_cfg).to_be_visible()

    # Verify that S.cfg is indeed null initially on blank page
    cfg_val = await page.evaluate("() => S.cfg")
    assert cfg_val is None, "S.cfg should be null initially on a blank page"

    # Verify that the Add Rule button is disabled initially
    btn_ar = page.locator('#btn-ar')
    await expect(btn_ar).to_be_disabled()

    # 2. Create a temporary log4j XML file
    xml_content = """<log4j:configuration xmlns:log4j="http://jakarta.apache.org/log4j/">
    <appender name="my_console_appender" class="org.apache.log4j.ConsoleAppender">
        <layout class="org.apache.log4j.PatternLayout">
            <param name="ConversionPattern" value="%d{yyyy-MM-dd HH:mm:ss,SSS} %-5p [%t] %c - %m%n"/>
        </layout>
    </appender>
</log4j:configuration>"""

    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
        f.write(xml_content.encode('utf-8'))
        temp_xml_path = f.name

    try:
        # 3. Simulate clicking the "Import XML Config File" button and uploading the file
        async with page.expect_file_chooser() as fc_info:
            await page.click("#btn-lj-imp")
        file_chooser = await fc_info.value
        await file_chooser.set_files(temp_xml_path)

        # 4. Assert that `#lj-res` is visible and populated inline
        lj_res = page.locator('#lj-res')
        await expect(lj_res).to_be_visible(timeout=5000)

        # Check text content in inline result area
        text_content = await lj_res.text_content()
        assert "Found 1 appender" in text_content
        assert "my_console_appender" in text_content

        # 5. Click the "Preview & Import" button
        btn_show_sh = page.locator('#btn-show-sh')
        await expect(btn_show_sh).to_be_visible()
        await btn_show_sh.click()

        # 6. Verify that the sheet overlay modal `#sh-ov` opens (remove hidden class)
        sh_ov = page.locator('#sh-ov')
        await expect(sh_ov).to_have_class("sh-ov")

        # 7. Click the "Import Selected" button
        btn_shi = page.locator('#btn-shi')
        await expect(btn_shi).to_be_visible()
        await btn_shi.click()

        # 8. Assert that the sheet modal is closed/hidden
        await expect(sh_ov).to_have_class("sh-ov hidden")

        # 9. Verify S.cfg is now loaded and contains the new rule
        cfg_loaded = await page.evaluate("() => S.cfg !== null")
        assert cfg_loaded, "S.cfg should have been initialized from defaults"

        rules_count = await page.evaluate("() => S.cfg.elementRules.length")
        # Should contain default rules + 1 imported appender rule
        assert rules_count > 0, "Rules should be loaded into state"

        # Check that the custom appender rule name exists
        has_imported_rule = await page.evaluate(
            "() => S.cfg.elementRules.some(r => r.name.includes('my_console_appender'))"
        )
        assert has_imported_rule, "State should contain the imported appender rule"

        # 10. Verify that `#btn-ar` is now enabled
        await expect(btn_ar).not_to_be_disabled()

        # Check for any console/JS errors
        assert_no_critical_errors(page)

    finally:
        # Cleanup
        if os.path.exists(temp_xml_path):
            os.remove(temp_xml_path)
