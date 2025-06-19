import functools
import logging
import time
from typing import Any, Callable, Optional, TypeVar, cast
from urllib.parse import urljoin

from playwright.sync_api import Locator, Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize the BasePage with a Playwright Page object and base URL.

        Args:
            page: Playwright Page object
            base_url: Base URL for the application
        """
        if not isinstance(page, Page):
            raise TypeError(f"Expected Page object but got {type(page)}")

        self.page = page
        self.url = base_url
        self.logger = logging.getLogger(name=__name__)

    T = TypeVar("T")

    @staticmethod
    def retry(retries: int = 3, base_delay: float = 1.0):
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(wrapped=func)
            def wrapper(self, *args, **kwargs) -> Any | None:
                for attempt in range(1, retries + 1):
                    try:
                        self.logger.info(
                            f"Attempt {attempt} for action: {func.__name__}"
                        )
                        return func(self, *args, **kwargs)
                    except Exception as e:
                        self.logger.warning(f"Attempt {attempt} failed: {e}")
                        if attempt < retries:
                            delay = base_delay * (
                                2 ** (attempt - 1)
                            )  # Exponential backoff
                            self.logger.info(
                                f"Retrying action {func.__name__} after {delay:.2f} seconds..."
                            )
                            time.sleep(delay)
                        else:
                            self.logger.error(
                                f"Action {func.__name__} failed after {retries} attempts"
                            )
                            raise
            return wrapper
        return decorator

    def locator(self, selector: str) -> Locator:
        """Get a locator for the given selector."""
        return self.page.locator(selector)

    @retry()
    def wait_until_loaded(self) -> None:
        """Wait for any navigation/redirection to complete and page to be ready."""
        self.logger.info("Waiting for navigation to complete")
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")
        self.logger.info("Page is loaded and ready.")

    def back(self):
        self.page.go_back()
        return self

    def forward(self):
        self.page.go_forward()
        return self

    def refresh(self):
        self.page.reload()
        return self

    @retry()
    def navigate(self, path: str = "") -> None:
        """Navigate to the page URL by provided path.

        Args:
            path: Optional path to append to the base URL
        """
        full_url = urljoin(base=self.url, url=path) if self.url else path

        if not full_url:
            raise ValueError(
                "No URL provided for navigation. Either provide a path or set base_url."
            )

        self.logger.info(f"Navigating to {full_url}")
        self.page.goto(url=full_url)
        self.wait_until_loaded()

    @retry()
    def click_element_and_wait_for_navigation(self, selector: str) -> None:
        """Click element and wait for navigation using locator."""
        self.logger.info(f"Clicking element that triggers navigation: {selector}")
        with self.page.expect_navigation():
            self.locator(selector).click()
        self.wait_until_loaded()
        self.logger.info(f"Page loaded after clicking element: {selector}")

    @retry()
    def click_element(self, selector: str) -> None:
        """Click on an element using locator."""
        self.logger.info(f"Clicking element: {selector}")
        self.locator(selector).click()

    @retry()
    def fill_text(self, selector: str, text: str) -> None:
        """Fill text into an input field using locator."""
        self.logger.info(f"Filling text into element: {selector}")
        self.locator(selector).fill(text)

    @retry()
    def get_text(self, selector: str) -> str:
        """Get text content from an element using locator."""
        self.logger.info(f"Getting text from element: {selector}")
        return self.locator(selector).text_content() or ""

    @retry()
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible using locator."""
        return self.locator(selector).is_visible()

    @retry()
    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled using locator."""
        return self.locator(selector).is_enabled()

    @retry()
    def is_checked(self, selector: str) -> bool:
        """Check if checkbox/radio is checked using locator."""
        return self.locator(selector).is_checked()

    @retry()
    def wait_for_element(self, selector: str, timeout: Optional[float] = None) -> None:
        """Wait for element to be visible using locator."""
        self.logger.info(f"Waiting for element: {selector}")
        self.locator(selector).wait_for(state="visible", timeout=timeout)

    @retry()
    def wait_for_element_hidden(self, selector: str, timeout: Optional[float] = None) -> None:
        """Wait for element to be hidden using locator."""
        self.logger.info(f"Waiting for element to be hidden: {selector}")
        self.locator(selector).wait_for(state="hidden", timeout=timeout)

    @retry()
    def get_element_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Get element attribute value using locator."""
        self.logger.info(f"Getting attribute '{attribute}' from element: {selector}")
        return self.locator(selector).get_attribute(attribute)

    @retry()
    def select_option(self, selector: str, value: str) -> None:
        """Select an option in a dropdown using locator."""
        self.logger.info(f"Selecting option '{value}' in dropdown: {selector}")
        self.locator(selector).select_option(value)

    @retry()
    def hover_element(self, selector: str) -> None:
        """Hover over an element using locator."""
        self.logger.info(f"Hovering over element: {selector}")
        self.locator(selector).hover()

    @retry()
    def double_click_element(self, selector: str) -> None:
        """Double click an element using locator."""
        self.logger.info(f"Double clicking element: {selector}")
        self.locator(selector).dblclick()

    @retry()
    def right_click_element(self, selector: str) -> None:
        """Right click an element using locator."""
        self.logger.info(f"Right clicking element: {selector}")
        self.locator(selector).click(button="right")

    @retry()
    def press_key(self, selector: str, key: str) -> None:
        """Press a key on an element using locator."""
        self.logger.info(f"Pressing key '{key}' on element: {selector}")
        self.locator(selector).press(key)

    @retry()
    def clear_and_fill(self, selector: str, text: str) -> None:
        """Clear input field and fill with new text using locator."""
        self.logger.info(f"Clearing and filling element: {selector}")
        locator = self.locator(selector)
        locator.clear()
        locator.fill(text)

    @retry()
    def get_element_count(self, selector: str) -> int:
        """Get count of elements matching selector using locator."""
        return self.locator(selector).count()

    @retry()
    def take_screenshot(self, path: str) -> None:
        """Take a screenshot."""
        self.page.screenshot(path=path)

    def expect_visible(self, selector: str) -> None:
        """Assert that element is visible using expect and locator."""
        expect(self.locator(selector)).to_be_visible()

    def expect_hidden(self, selector: str) -> None:
        """Assert that element is hidden using expect and locator."""
        expect(self.locator(selector)).to_be_hidden()

    def expect_text(self, selector: str, expected_text: str) -> None:
        """Assert that element contains expected text using expect and locator."""
        expect(self.locator(selector)).to_contain_text(expected_text)

    def expect_value(self, selector: str, expected_value: str) -> None:
        """Assert that input element has expected value using expect and locator."""
        expect(self.locator(selector)).to_have_value(expected_value)

    def expect_attribute(self, selector: str, attribute: str, expected_value: str) -> None:
        """Assert that element has expected attribute value using expect and locator."""
        expect(self.locator(selector)).to_have_attribute(attribute, expected_value)

    def expect_count(self, selector: str, expected_count: int) -> None:
        """Assert that elements matching selector have expected count using expect and locator."""
        expect(self.locator(selector)).to_have_count(expected_count)
