from urllib.parse import urljoin

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page, base_url: str = "") -> None:
        super().__init__(page=page, base_url=base_url)
        self.path = "/users/sign_in"
        self.url = urljoin(base=base_url, url=self.path)
        
        # Element selectors
        self.email_field = "#user_email"
        self.password_field = "#user_password"
        self.signin_button = "input[value='Sign in']"
        self.error_message = ".alert-error"
        self.remember_checkbox = "#user_remember_me"

    def input_email(self, email: str) -> None:
        """Input email into the email field using locator."""
        self.logger.info(f"Filling in email field: {email}")
        self.fill_text(self.email_field, email)

    def input_password(self, password: str) -> None:
        """Input password into the password field using locator."""
        self.logger.info("Filling in password field")
        self.fill_text(self.password_field, password)

    def click_submit(self) -> None:
        """Click the submit button using locator."""
        self.logger.info("Clicking submit button")
        self.click_element_and_wait_for_navigation(self.signin_button)
    
    def toggle_remember_me(self) -> None:
        """Toggle the remember-me checkbox using locator."""
        self.logger.info("Toggling remember-me checkbox")
        if not self.is_checked(self.remember_checkbox):
            self.click_element(self.remember_checkbox)

    def login(self, email: str, password: str, remember_me: bool = False) -> None:
        """Login with the given credentials using locators."""
        self.navigate()
        self.input_email(email)
        self.input_password(password)
        if remember_me:
            self.toggle_remember_me()
        self.click_submit()

    def get_error_message(self) -> str:
        """Get the error message if login failed using locator."""
        if self.is_visible(self.error_message):
            return self.get_text(self.error_message)
        return ""

    def expect_login_form_visible(self) -> None:
        """Assert that login form elements are visible using expect."""
        self.expect_visible(self.email_field)
        self.expect_visible(self.password_field)
        self.expect_visible(self.signin_button)

    def expect_error_message(self, expected_message: str) -> None:
        """Assert that error message contains expected text using expect."""
        self.expect_text(self.error_message, expected_message)
