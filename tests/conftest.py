"""
conftest.py — LogLens Regression Test Suite
Shared fixtures and utilities for all Playwright tests.
"""
import pathlib
import pytest
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

# ── Path to the app ───────────────────────────────────────────────────────────
APP_URL = pathlib.Path('/Volumes/Study/Projects/loglens/loglens.html').as_uri()

# ── Standard demo data (mirrors built-in demo log S.trees shape) ─────────────
DEMO_TREES_JS = """
window._testDataInjected = true;
const _t0 = Date.now() - 10000;
const _mk = (i, thr, lvl, dur, cid) => ({
  id: 'n' + i,
  ruleId: 'r1', ruleName: 'Op-' + i,
  elementName: 'Element-' + i, payload: '{}',
  thread: thr, timestamp: _t0 + i * 300, duration: dur,
  endTimestamp: _t0 + i * 300 + dur,
  behavior: 'push', level: lvl,
  slaBreached: (dur > 2000),
  correlationId: cid || 'trace-' + (i % 3 + 1),
  rawLine: 'line ' + i, events: [], visualStyle: {}
});
const _main = Array.from({length: 20}, (_, i) =>
  _mk(i, 'main', i % 5 === 0 ? 'ERROR' : 'INFO', 200 + i * 150, 'TX-A' + (i % 3))
);
const _worker = Array.from({length: 10}, (_, i) =>
  _mk(100 + i, 'worker', 'INFO', 3000 + i * 500, 'TX-B' + (i % 2))
);
S.trees = { main: _main, worker: _worker };
S.threads = ['main', 'worker'];
S.activeThr = 'main';
S.ganttZoom = 1;
S.viewMode = 'gantt';
S.stats = { fileSize: 1024 * 1024, linesProcessed: 30, totalNodes: 30, slaBreaches: 2 };
if (typeof UI !== 'undefined' && UI.render) {
  UI.render(S.trees, S.threads, S.stats);
  UI.svm('gantt');
}
"""

DISMISS_ONBOARDING_JS = """() => {
  const ob = document.getElementById('ob-ov');
  if (ob) ob.style.display = 'none';
  const skip = document.getElementById('skip-link');
  if (skip) skip.style.display = 'none';
}"""


# ── Pytest-asyncio settings ───────────────────────────────────────────────────
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (run with -m slow to select)"
    )


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def event_loop_policy():
    """Use default asyncio event loop policy."""
    import asyncio
    return asyncio.DefaultEventLoopPolicy()


@pytest.fixture(scope="function")
async def page_with_data(pytestconfig):
    """
    Launches Chromium, navigates to loglens.html, dismisses the onboarding
    overlay, and injects a standard synthetic dataset into S.trees so every
    test starts from a consistent, data-loaded state.

    Yields the Playwright Page object. Automatically closes browser on teardown.
    """
    console_errors = []
    async with async_playwright() as pw:
        browser: Browser = await pw.chromium.launch(headless=True)
        ctx: BrowserContext = await browser.new_context(
            viewport={'width': 1400, 'height': 900}
        )
        page: Page = await ctx.new_page()

        # Capture console errors for post-test assertion
        page.on('console', lambda m: console_errors.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: console_errors.append(f'PAGE ERROR: {e}'))

        await page.goto(APP_URL, wait_until='domcontentloaded')
        await page.wait_for_timeout(700)
        await page.evaluate(DISMISS_ONBOARDING_JS)
        await page.evaluate(DEMO_TREES_JS)

        page._ll_console_errors = console_errors  # attach for test access

        yield page

        await browser.close()


@pytest.fixture(scope="function")
async def blank_page(pytestconfig):
    """
    Launches Chromium and navigates to loglens.html WITHOUT injecting demo data.
    Useful for testing the first-run/empty state experience or raw onboarding flow.
    Yields the Page. Browser is closed on teardown.
    """
    console_errors = []
    async with async_playwright() as pw:
        browser: Browser = await pw.chromium.launch(headless=True)
        ctx: BrowserContext = await browser.new_context(
            viewport={'width': 1400, 'height': 900}
        )
        page: Page = await ctx.new_page()

        page.on('console', lambda m: console_errors.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: console_errors.append(f'PAGE ERROR: {e}'))

        await page.goto(APP_URL, wait_until='domcontentloaded')
        await page.wait_for_timeout(700)

        page._ll_console_errors = console_errors

        yield page

        await browser.close()


# ── Shared helper (importable from tests) ─────────────────────────────────────
def assert_no_critical_errors(page, keywords=None):
    """
    Assert that no JS errors matching the given keywords were emitted.
    Default keywords cover all major LogLens modules.
    """
    keywords = keywords or [
        'TypeError', 'ReferenceError', 'SyntaxError',
        'AI_INSIGHTS', 'FOCUS_MODE', 'TIMELINE_NAV', 'TRACE_EXPLORER',
        'GANTT', 'STATS', 'WM', 'ONBOARD'
    ]
    errors = getattr(page, '_ll_console_errors', [])
    hits = [e for e in errors if any(kw in e for kw in keywords)]
    assert not hits, f'Critical JS errors detected:\n' + '\n'.join(hits)
