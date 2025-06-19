import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import (
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

# Import directly from project root
from constants import LOG_DIR, VIDEO_DIR, BrowserType, Resolution
from logging_config import configure_logging
from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.login_page import LoginPage


def pytest_addoption(parser) -> None:
    parser.addoption("--target", action="store", help="Target application URL")

    parser.addoption(
        "--browser-type",
        action="store",
        default=BrowserType.CHROMIUM.value,
        choices=BrowserType.values(),
        help="Browser type to use for testing: chromium, firefox, webkit, or edge",
    )
    
    parser.addoption(
        "--selenoid-url",
        action="store",
        default=None,
        help="Selenoid URL (e.g. http://localhost:4444/wd/hub). If provided, tests will run on Selenoid",
    )
    
    parser.addoption(
        "--browser-version",
        action="store",
        default="latest",
        help="Browser version to use in Selenoid (only used if --selenoid-url is provided)",
    )
    
    parser.addoption(
        "--resolution",
        action="store",
        default=Resolution.FHD.value,
        choices=Resolution.values(),
        help="Screen resolution for testing",
    )

    parser.addoption(
        "--wait-strategy",
        action="store",
        default="networkidle",
        choices=["networkidle", "domcontentloaded", "load", "commit"],
        help="Default wait strategy for page navigation (default: networkidle)",
    )


@pytest.fixture(scope="session")
def target_url(request) -> str:
    return request.config.getoption("--target")


@pytest.fixture(scope="session")
def browser_type(request) -> BrowserType:
    return BrowserType(request.config.getoption("--browser-type"))


@pytest.fixture(scope="session")
def selenoid_url(request) -> str:
    return request.config.getoption("--selenoid-url")


@pytest.fixture(scope="session")
def browser_version(request) -> str:
    return request.config.getoption("--browser-version")


@pytest.fixture(scope="session")
def resolution(request) -> Resolution:
    return Resolution(request.config.getoption("--resolution"))


@pytest.fixture(scope="session")
def wait_strategy(request) -> str:
    """Returns the default wait strategy for page navigation."""
    return request.config.getoption("--wait-strategy")





@pytest.fixture(scope="session")
def playwright() -> Generator[Playwright, None, None]:
    """Return a playwright instance that is shared among all tests."""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture
def page(browser_context, wait_strategy) -> Generator[Page, None, None]:
    """Create a new page in the browser context."""
    page = browser_context.new_page()
    page.set_default_timeout(15000)
    
    # Store the default wait strategy on the page for reference in BasePage methods
    page.default_wait_strategy = wait_strategy
    
    # Create a method to wait for page to be fully ready based on strategy
    def wait_for_ready():
        page.wait_for_load_state(wait_strategy)
    
    # Attach this helper to the page object
    page.wait_for_ready = wait_for_ready
    
    yield page
    page.close()


@pytest.fixture(scope="session")
def browser_context(
    playwright,
    browser_type: BrowserType, 
    selenoid_url: str, 
    browser_version: str,
    resolution: Resolution,
) -> Generator[BrowserContext, None, None]:
    """Create a browser context for testing."""
    # Map browser types to their respective launcher methods
    browser_launcher = {
        BrowserType.FIREFOX: playwright.firefox,
        BrowserType.WEBKIT: playwright.webkit,
        BrowserType.EDGE: playwright.chromium,
        BrowserType.CHROMIUM: playwright.chromium,
    }.get(browser_type, playwright.chromium)
    
    if selenoid_url:
        # Map browser types to Selenoid browser names
        browser_name = {
            BrowserType.CHROMIUM: "chrome",
            BrowserType.FIREFOX: "firefox",
            BrowserType.WEBKIT: "chrome",
            BrowserType.EDGE: "edge",
        }.get(browser_type, "chrome")
        
        logging.info(f"Connecting to Selenoid at {selenoid_url} with {browser_name}:{browser_version}")
        Path(VIDEO_DIR).mkdir(exist_ok=True)
        
        # Connect to Selenoid using CDP protocol
        browser = browser_launcher.connect_over_cdp(
            f"{selenoid_url.replace('/wd/hub', '')}/devtools/{browser_name}/{browser_version}/",
            timeout=30000
        )
        context = browser.new_context(
            viewport=resolution.value if resolution.value is None else {"width": resolution.value["width"], "height": resolution.value["height"]},
            record_video_dir=str(VIDEO_DIR)
        )
    else:
        if browser_type == BrowserType.EDGE:
            browser = browser_launcher.launch(channel="msedge", headless=False)
        else:
            browser = browser_launcher.launch(headless=False)
        context = browser.new_context(
            viewport=resolution.value if resolution.value is None else {"width": resolution.value["width"], "height": resolution.value["height"]}
        )

    yield context
    context.close()
    browser.close()


def pytest_configure(config):
    """Create logs/ dir and configure root logger once for the test session."""
    config.addinivalue_line("markers", "smoke: mark a test as a smoke test")
    config.addinivalue_line("markers", "regression: mark a test as a regression test")
    
    console_level = config.option.log_level or "INFO"
    logs_dir = Path(LOG_DIR)
    logs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_log_file = logs_dir / f"test_{timestamp}.log"

    configure_logging(
        level=console_level,
        logfile_path=str(session_log_file),
        enable_console=True,
    )
    logging.getLogger(__name__).info("Logging to %s", session_log_file)
    os.environ["LOG_LEVEL"] = console_level


@pytest.fixture(autouse=True)
def logger():
    """Provides a logger instance for tests. 
    
    This fixture is automatically used in all tests.
    """
    return logging.getLogger("test")


@pytest.fixture
def base_page(page, target_url) -> BasePage:
    """Creates a BasePage instance with the page and target URL."""
    from pages.base_page import BasePage
    return BasePage(page=page, base_url=target_url)


@pytest.fixture
def home_page(page, target_url) -> HomePage:
    """Creates a HomePage instance with the page and target URL."""
    from pages.home_page import HomePage
    return HomePage(page=page, base_url=target_url)


@pytest.fixture
def login_page(page, target_url) -> "LoginPage":
    """Creates a LoginPage instance with the page and target URL."""
    from pages.login_page import LoginPage
    return LoginPage(page=page, base_url=target_url)
