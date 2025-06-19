def test_login_page(home_page, login_page, logger) -> None:
    logger.info("Navigate to the Base page")
    home_page.navigate()
    logger.info("Navigate to the login page")
    home_page.click_login()
    logger.info("Input email and password")
    login_page.login(email="user@example.com", password="securepassword")
