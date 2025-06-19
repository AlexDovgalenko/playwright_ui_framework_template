from typing import TYPE_CHECKING

import pytest
from playwright.sync_api import Page

from constants import BrowserType
from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.login_page import LoginPage

if TYPE_CHECKING:
    from logging import Logger


def test_click_element(base_page, browser_type: BrowserType) -> None:
    """Test clicking on an element using locators."""
    base_page.navigate()
    
    # Using locators provides auto-waiting and better error handling
    base_page.click_element("#example-button")

def test_fill_text(base_page) -> None:
    """Test filling text using locators."""
    base_page.navigate()
    
    # Locators auto-wait for elements and provide better interactions
    base_page.fill_text("#example-input", "Test Input")
    base_page.expect_value("#example-input", "Test Input")

def test_home_page_logo(home_page, browser_type: BrowserType) -> None:
    """Test home page logo visibility using locators."""
    home_page.navigate()
    
    # Using expect assertions for better test reliability
    home_page.expect_visible(home_page.logo_image)
    
    logo_src = home_page.get_logo_image_src()
    assert logo_src != ""

def test_login_functionality(login_page) -> None:
    """Test login functionality using locators."""
    login_page.navigate()
    
    # Assert form is visible before interacting
    login_page.expect_login_form_visible()
    
    # Perform login
    login_page.login("test@example.com", "password123", remember_me=True)

def test_search_functionality(home_page) -> None:
    """Test search functionality using locators."""
    home_page.navigate()
    
    # Search with auto-waiting locators
    home_page.search_content("test query")
    
    # Verify search results or page changes
    # home_page.expect_visible(".search-results")
