from .base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page, base_url: str = "") -> None:
        # Home page is typically the root, so we use the base_url directly
        super().__init__(page=page, base_url=base_url)
        self.logo_image = ".logo.img-responsive"
        self.login_link = ".header__nav-item.header__nav-sign-in"
        self.search_box = "input[name='q']"
        # We're at the root path
        self.path = "/"

    def get_logo_image_src(self) -> str:
        """Get the logo image src attribute using locator."""
        self.logger.info("Getting logo image src attribute")
        return self.get_element_attribute(self.logo_image, "src") or ""

    def click_login(self) -> None:
        """Click the login link using locator."""
        self.logger.info("Clicking login link")
        self.click_element_and_wait_for_navigation(self.login_link)

    def search_content(self, query: str) -> None:
        """Search for content on the page using locator."""
        self.logger.info(f"Searching for content: {query}")
        search_locator = self.locator(self.search_box)
        search_locator.fill(query)
        search_locator.press("Enter")
        self.wait_until_loaded()

    def is_logo_visible(self) -> bool:
        """Check if logo is visible using locator."""
        return self.is_visible(self.logo_image)

    def navigate(self, path: str = "") -> None:
        """Navigate to home page with optional additional path."""
        # If home page has its own path, use it as base
        full_path = path or self.path
        super().navigate(full_path)
