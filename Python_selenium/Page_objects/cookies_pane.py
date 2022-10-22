from Page_objects.base_page import BasePage
from selenium.webdriver.common.by import By


class CookiesPane(BasePage):

    # Identification of objects on cookies pane.
    cookies_pane = (By.XPATH, "//div[@class='cookies-info__container']")
    reject_all_button = (By.XPATH, "//a[@data-action-id-value='0']")

    # Initialization.
    def __init__(self, driver):
        super().__init__(driver)

    # Actions on cookies pane.
    def cookies_pane_click_reject_all(self):
        self.base_click(self.reject_all_button)

    def cookies_pane_is_invisible(self):
        flag = self.base_is_invisible(self.cookies_pane)
        return flag