import pytest

from Config.test_data import TestData
from Helpers.helpers import Helpers
from Page_objects.basket import Basket
from Page_objects.login_dialog import LoginDialog
from Page_objects.main_page import MainPage
from Page_objects.my_account import MyAccount
from Page_objects.top_section import TopSection
from Page_objects.cookies_pane import CookiesPane


@pytest.mark.usefixtures("initialize_driver")
class TestsAlza:

    def test_login_logout(self):
        """
        Tests log in functionality. First all cookies are rejected, then login is clicked to invoke login dialog.
        Credential fields are blank, signin button is pressed and is checked that login dialog stays open and there are correspondent error messages displayed.
        Then wrong email address is provided with correct password, signin button is pressed and is checked that login dialog stays displayed.
        Then correct email address is provided with wrong password, signin button is pressed and is checked that login dialog stays displayed.
        Then both correct email address and correct password are provided, signin button is pressed and is checked that login dialog disappears and correct
        user email is displayed in upper part of the screen.
        At the end logout link is clicked and is checked that login link is present.
        """

        self.login_dialog = LoginDialog(self.driver)
        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)

        # Reject all cookies.
        self.cookies_pane.cookies_pane_click_reject_all()
        assert self.cookies_pane.cookies_pane_is_invisible()

        # Click login link and switch to login frame.
        self.top_section.top_section_click_login_link()
        self.login_dialog.login_switch_to_login_frame()

        # Unsuccessful login:
        # Email and password fields blank.
        self.login_dialog.login_click_signin_button()
        assert self.login_dialog.login_dialog_is_visible_in_frame()
        assert self.login_dialog.login_get_blank_email_text() == TestData.blank_email_text
        assert self.login_dialog.login_get_blank_password_text() == TestData.blank_password_text

        # Wrong email and correct password provided.
        self.login_dialog.login_provide_email(TestData.incorrect_user_name)
        self.login_dialog.login_provide_password(TestData.password)
        self.login_dialog.login_click_signin_button()
        assert self.login_dialog.login_dialog_is_visible_in_frame()
        assert self.login_dialog.login_get_disabled_login_button_text() == TestData.signin_button_incorrect_text

        # Correct email and wrong password provided.
        self.login_dialog.login_provide_email(TestData.user_name)
        self.login_dialog.login_provide_password(TestData.incorrect_password)
        self.login_dialog.login_click_signin_button()
        assert self.login_dialog.login_dialog_is_visible_in_frame()
        assert self.login_dialog.login_get_disabled_login_button_text() == TestData.signin_button_incorrect_text

        # Successful login.
        self.login_dialog.login_provide_email(TestData.user_name)
        self.login_dialog.login_provide_password(TestData.password)
        self.login_dialog.login_click_signin_button()
        self.login_dialog.login_switch_back_from_login_frame()
        assert self.login_dialog.login_dialog_is_invisible_out_of_frame()
        assert self.login_dialog.login_get_signed_in_text() == TestData.user_signed_in_text

        # Logout.
        self.top_section.top_section_click_logout_link()
        assert self.top_section.top_section_login_link_is_visible()

    def test_basket_add_remove_item(self):
        """
        Test adding and removing from basket. First all cookies are rejected then logs in, adds computer to basket, then goes to basket,
        checks name of item present, its count and price. Then removes item from basket and checks basket is empty.
        At the end logs out.
        """

        self.login_dialog = LoginDialog(self.driver)
        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.main_page = MainPage(self.driver)
        self.basket = Basket(self.driver)

        # Reject all cookies.
        self.cookies_pane.cookies_pane_click_reject_all()

        # Log into application:
        # Click login link.
        self.top_section.top_section_click_login_link()
        #   # Fill in credentials, login, switch back to page.
        self.login_dialog.login_successful_login(TestData.user_name, TestData.password)

        # Putting into basket:
        # Navigate to computers.
        self.main_page.main_page_hover_click_computers_notebooks_menu_item()
        self.main_page.main_page_click_computers_tile()
        # Get first computer name and price and put it into basket and go there.
        first_computer_name = self.main_page.main_page_get_first_computer_name()
        first_computer_price = self.main_page.main_page_get_first_computer_price()
        self.main_page.main_page_click_first_computer_buy_button()
        self.main_page.main_page_click_cont_to_basket_button()

        # On basket page:
        # Close assistant bubble if present:
        self.basket.basket_close_assistant_bubble_if_exists()
        # Check item name, count and price.
        assert first_computer_name in self.basket.basket_get_item_name()
        assert self.basket.basket_get_item_count() == TestData.number_of_items_in_basket
        assert first_computer_price == self.basket.basket_get_item_price()
        # Remove item from basket and check it is empty.
        self.basket.basket_click_down_arrow_price()
        self.basket.basket_click_down_arrow_price_remove()
        assert self.basket.basket_get_text_once_all_items_removed() == TestData.text_once_all_items_removed_from_basket

        # Logout.
        self.top_section.top_section_click_logout_link()

    def test_search(self):
        """
        Test search functionality in 2 ways. First all cookies are rejected then logs in, provides search value, presses search button
        and checks header of result and that amount of items found is bigger than 0.
        Then provides search value, waits for suggestions to appear, clicks first article in suggestions and check that name of article contains
        looked up word.
        At the end logs out.
        """

        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.login_dialog = LoginDialog(self.driver)
        self.main_page = MainPage(self.driver)

        # Reject all cookies.
        self.cookies_pane.cookies_pane_click_reject_all()

        # Log into application:
        # Click login link.
        self.top_section.top_section_click_login_link()
        # Fill in credentials, login, switch back to page.
        self.login_dialog.login_successful_login(TestData.user_name, TestData.password)

        # Search for "jízdní kola" and click search button:
        self.top_section.top_section_search_provide(TestData.search_value_via_search_button)
        self.top_section.top_section_click_search_button()
        # Check result.
        assert self.main_page.main_page_get_search_result_header() == TestData.search_result_header_via_search_button
        assert self.main_page.main_page_get_search_result_items_amount() > 0

        # Search for "recenze" and choose from suggestion:
        self.top_section.top_section_search_provide(TestData.search_value_via_suggestion)
        self.top_section.top_section_search_suggestion_click_1st_article()
        # Check result.
        assert TestData.search_result_word_in_header_via_suggestion in self.main_page.main_page_get_search_result_header().lower()

        # Logout.
        self.top_section.top_section_click_logout_link()

    def test_watchdog_add_remove_item(self):
        """
        Test adding and removing from watchdog list. First all cookies are rejected then logs in, adds watchdog to pet supply item,
        then goes to watchdog list, checks name of item present. Then removes item from watchdog list and checks watchdog list is empty.
        At the end logs out.
        """

        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.login_dialog = LoginDialog(self.driver)
        self.main_page = MainPage(self.driver)
        self.my_account = MyAccount(self.driver)

        # Reject all cookies.
        self.cookies_pane.cookies_pane_click_reject_all()

        # Log into application:
        # Click login link.
        self.top_section.top_section_click_login_link()
        # Fill in credentials, login, switch back to page.
        self.login_dialog.login_successful_login(TestData.user_name, TestData.password)

        # Navigate to pet supplies, open first pet supply and get its name.
        self.main_page.main_page_hover_click_pet_supplies_menu_item()
        self.main_page.main_page_click_first_pet_suppy_item()
        first_pet_supply_name = self.main_page.main_page_get_first_pet_supply_name()

        # Setting watch price.
        self.main_page.main_page_click_watch_price()
        self.main_page.main_page_watchdog_set_price_limit(TestData.watchdog_price_limit)
        self.main_page.main_page_watchdog_click_confirm_button()

        # Check list of watchdogs:
        # Go to list of watchdogs.
        self.top_section.top_section_click_user_profile_link()
        self.my_account.my_account_click_account_settings_dropdown()
        self.my_account.my_account_click_at_watchdog_list_menu_item()
        # Check watched item name.
        assert self.my_account.my_account_watchdog_list_get_watchdog_item_name() == first_pet_supply_name
        # Remove item from watchdog list.
        self.my_account.my_account_watchdog_list_remove_item_close_success_dialog()
        assert self.my_account.my_account_watchdog_list_get_text_once_all_items_removed() == TestData.text_once_all_items_removed_from_watchdog_list

        # Logout.
        self.top_section.top_section_click_logout_link()

    def test_account_changes(self):
        """
        Test changes of information in user account. First all cookies are rejected then logs in and navigates to user account page.
        Then street, zip and city fields are filled in.
        Then navigates to main page and back to user account page where is checked that fields still have values provided into them.
        After that fields are returned to original state, i.e. cleared.
        At the end logs out.
        """

        self.login_dialog = LoginDialog(self.driver)
        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.my_account = MyAccount(self.driver)
        self.helpers = Helpers(self.driver)

        # Reject all cookies.
        self.cookies_pane.cookies_pane_click_reject_all()

        # Log into application:
        # Click login link.
        self.top_section.top_section_click_login_link()
        # Fill in credentials and login.
        self.login_dialog.login_successful_login(TestData.user_name, TestData.password)
        # Switch from login frame back to page.
        self.login_dialog.login_switch_back_from_login_frame()

        # Changes to my account:
        # Navigate to my account page.
        self.top_section.top_section_click_user_profile_link()
        self.my_account.my_account_click_account_settings_dropdown()
        self.my_account.my_account_click_my_account_menu_item()
        # Fill in street, zip, city.
        self.my_account.my_account_provide_street()
        self.my_account.my_account_provide_zip()
        self.my_account.my_account_provide_city()
        # Go back to main page.
        self.top_section.top_section_click_alza_icon()
        # Go back to my account page and check provided values are stored.
        self.top_section.top_section_click_user_profile_link()
        self.my_account.my_account_click_account_settings_dropdown()
        self.my_account.my_account_click_my_account_menu_item()
        assert self.my_account.my_account_get_street_value() == TestData.street_and_number
        assert self.my_account.my_account_get_zip_value() == TestData.zip
        assert self.my_account.my_account_get_city_value() == TestData.city

        # Clear city, street, zip. City as the first one because it is not validated thus if cleared as last it could happen it won't be saved.
        self.my_account.my_account_clear_city_input()
        self.my_account.my_account_clear_street_input()
        self.my_account.my_account_clear_zip_input()
        # Refresh page to make sure fields are cleared.
        self.helpers.helpers_refresh_page()

        # Logout.
        self.top_section.top_section_click_logout_link()