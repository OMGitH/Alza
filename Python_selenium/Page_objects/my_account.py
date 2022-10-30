from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from Config.test_data import TestData
from Page_objects.base_page import BasePage


class MyAccount(BasePage):
    # Identification of objects on my account page.
    account_settings_dropdown = (By.XPATH, "//div[@data-testid='menuSection-MyAccount']")
    my_account_menu_item = (By.XPATH, "//a[@data-testid='menuButton-UserSettings']")
    my_account_list_of_watchdogs = (By.XPATH, "//a[@data-testid='menuButton-UserWatchDog']")

    data_is_saving_text = (By.XPATH, "//span[@class='saving']/span[@class='text']")
    data_was_saved_text = (By.XPATH, "//span[@class='saved']/span[@class='text']")

    """
    Original uploaded code.
    data_is_saving_text = (By.XPATH, "//span[@class='saving'][contains(@style, 'inline')]/span[@class='text']")
    data_was_saved_text = (By.XPATH, "//span[@class='saved'][contains(@style, 'inline')]/span[@class='text']")
    """

    street_input = (By.NAME, "street")
    street_input_correctly_filled = (By.XPATH, "//input[@name='street'][contains(@class, 'valid')][not(contains(@class, 'empt'))]")
    zip_input = (By.NAME, "zip")
    zip_input_correctly_filled = (By.XPATH, "//input[@name='zip'][contains(@class, 'valid')][not(contains(@class, 'empt'))]")
    city_input = (By.NAME, "city")
    watchdog_item = (By.XPATH, "//div[@class='watchDogInfo']/a")
    watchdog_item_1st_checkbox = (By.XPATH, "//div[@class='watchDogInfoItem priceLimit']//span[@class='checkboxBlue checked']")
    watchdog_item_2nd_checkbox = (By.XPATH, "//div[@class='watchDogInfoItem inStock']//span[@class='checkboxBlue checked']")
    watchdog_price_limit_provided = (By.XPATH, "//span[@class='watchDogStatusLabel']/span")
    watchdog_item_removal_confirmation_button = (By.XPATH, "//div[@id='alzaDialog'][not(contains(@style, 'opacity'))]//span[@class='btnx normal green ok']")
    watchdog_remove_question_dialog = (By.ID, "alzaDialog")
    text_all_items_removed_from_watchdog_list = (By.XPATH, "//div[@id='noWatchDogArticle'][not(contains(@style, 'none'))]//div[@class='alzBox warn']")

    # Initialization.
    def __init__(self, driver):
        super().__init__(driver)

    # Actions on my account page.
    def my_account_click_account_settings_dropdown(self):
        self.base_click(self.account_settings_dropdown)

    def my_account_click_my_account_menu_item(self):
        self.base_click(self.my_account_menu_item)
        # Following method helps initialize the page as validations there are dynamic.
        self.base_element_exists(self.data_was_saved_text)

    def my_account_click_at_watchdog_list_menu_item(self):
        self.base_click(self.my_account_list_of_watchdogs)

    def my_account_provide_street(self):
        self.base_clear_input(self.street_input)
        self.base_send_keys(self.street_input, TestData.street_and_number)
        self.base_is_visible(self.street_input_correctly_filled)
        self.base_send_keys(self.street_input, Keys.TAB)
        self.base_is_visible(self.data_is_saving_text)
        self.base_is_visible(self.data_was_saved_text)

    def my_account_provide_zip(self):
        self.base_clear_input(self.zip_input)
        self.base_send_keys(self.zip_input, TestData.zip)
        self.base_is_visible(self.zip_input_correctly_filled)
        self.base_send_keys(self.zip_input, Keys.TAB)
        self.base_is_visible(self.data_is_saving_text)
        self.base_is_visible(self.data_was_saved_text)

    def my_account_provide_city(self):
        self.base_clear_input(self.city_input)
        self.base_send_keys(self.city_input, TestData.city)
        self.base_send_keys(self.city_input, Keys.TAB)
        self.base_is_visible(self.data_is_saving_text)
        self.base_is_visible(self.data_was_saved_text)

    def my_account_get_street_value(self):
        if self.base_is_visible(self.street_input):
            self.base_click(self.street_input)
            street_value = self.base_get_element_attribute_value(self.street_input, "value")
            self.base_send_keys(self.street_input, Keys.TAB)
            return street_value

    def my_account_get_zip_value(self):
        if self.base_is_visible(self.zip_input):
            self.base_click(self.zip_input)
            zip_value = self.base_get_element_attribute_value(self.zip_input, "value")
            self.base_send_keys(self.zip_input, Keys.TAB)
            return zip_value

    def my_account_get_city_value(self):
        if self.base_is_visible(self.city_input):
            self.base_click(self.city_input)
            city_value = self.base_get_element_attribute_value(self.city_input, "value")
            return city_value

    def my_account_clear_street_input(self):
        self.base_click(self.street_input)
        self.base_is_visible(self.street_input_correctly_filled)
        self.base_clear_input_by_pressing_backspace(self.street_input, "value")
        self.base_is_invisible(self.street_input_correctly_filled)
        self.base_send_keys(self.street_input, Keys.TAB)
        self.base_is_visible(self.data_is_saving_text)
        self.base_is_visible(self.data_was_saved_text)

    def my_account_clear_zip_input(self):
        self.base_click(self.zip_input)
        self.base_is_visible(self.zip_input_correctly_filled)
        self.base_clear_input_by_pressing_backspace(self.zip_input, "value")
        self.base_is_invisible(self.zip_input_correctly_filled)
        self.base_send_keys(self.zip_input, Keys.TAB)
        self.base_is_visible(self.data_is_saving_text)
        self.base_is_visible(self.data_was_saved_text)

    def my_account_clear_city_input(self):
        self.base_click(self.city_input)
        self.base_clear_input_by_pressing_backspace(self.city_input, "value")
        self.base_send_keys(self.city_input, Keys.TAB)
        self.base_is_visible(self.data_is_saving_text)
        self.base_is_visible(self.data_was_saved_text)

    def my_account_watchdog_list_get_watchdog_item_name(self):
        if self.base_is_visible(self.watchdog_item):
            watchdog_item_name = self.base_get_element_text(self.watchdog_item)
            return watchdog_item_name

    def my_account_watchdog_get_price_limit_provided(self):
        if self.base_is_visible(self.watchdog_price_limit_provided):
            watchdog_price_limit = self.base_get_element_text(self.watchdog_price_limit_provided)
            watchdog_price_limit = watchdog_price_limit.replace(" ", "")
            watchdog_price_limit = watchdog_price_limit.replace("Kč", "")
            return watchdog_price_limit

    def my_account_watchdog_list_remove_item_close_success_dialog(self):
        self.base_click(self.watchdog_item_1st_checkbox)
        self.base_click(self.watchdog_item_2nd_checkbox)
        self.base_click(self.watchdog_item_removal_confirmation_button)
        self.base_is_invisible(self.watchdog_remove_question_dialog)

    def my_account_watchdog_list_get_text_once_all_items_removed(self):
        if self.base_is_visible(self.text_all_items_removed_from_watchdog_list):
            all_items_removed_message = self.base_get_element_text(self.text_all_items_removed_from_watchdog_list)
            return all_items_removed_message
