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
        Credential fields are blank, signin button is pressed and is checked that login dialog stays open and there are corresponding error messages displayed.
        Then wrong email address is provided with correct password, signin button is pressed and is checked that login dialog stays displayed and there is correct
        text on signin button.
        Then correct email address is provided with wrong password, signin button is pressed and is checked that login dialog stays displayed and there is correct
        text on signin button.
        Then both correct email address and correct password are provided, signin button is pressed and is checked that login dialog disappears and correct
        user email is displayed in upper part of the screen.
        At the end logout link is clicked and is checked that login link is present.
        """

        self.login_dialog = LoginDialog(self.driver)
        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)

        # Reject all cookies.
        self.cookies_pane.cookies_pane_click_reject_all()
        assert self.cookies_pane.cookies_pane_is_invisible(), "Cookies pane is still visible but shall not be."

        # Click login link and switch to login frame.
        self.top_section.top_section_click_login_link()
        self.login_dialog.login_switch_to_login_frame()

        # Unsuccessful login:
        # Email and password fields blank.
        self.login_dialog.login_click_signin_button()
        assert self.login_dialog.login_dialog_is_visible_in_frame(), "Login dialog is not visible though it shall be."
        actual_blank_email_text = self.login_dialog.login_get_blank_email_text()
        assert actual_blank_email_text == TestData.blank_email_text, f"Wrong message for blank e-mail input field. Current message is {actual_blank_email_text} but it shall be {TestData.blank_email_text}."
        actual_blank_password_text = self.login_dialog.login_get_blank_password_text()
        assert actual_blank_password_text == TestData.blank_password_text, f"Wrong message for blank password input field. Current message is {actual_blank_password_text} but it shall be {TestData.blank_password_text}."

        # Wrong email and correct password provided.
        self.login_dialog.login_provide_email(TestData.incorrect_user_name)
        self.login_dialog.login_provide_password(TestData.password)
        self.login_dialog.login_click_signin_button()
        assert self.login_dialog.login_dialog_is_visible_in_frame(), "Login dialog is not visible though it shall be."
        actual_disabled_login_button_text = self.login_dialog.login_get_disabled_login_button_text()
        assert actual_disabled_login_button_text == TestData.signin_button_incorrect_user_name_password_text, f"Wrong message at signin button when incorrect email provided. Current message is {actual_disabled_login_button_text} but it shall be {TestData.signin_button_incorrect_user_name_password_text}."

        # Correct email and wrong password provided.
        self.login_dialog.login_provide_email(TestData.user_name)
        self.login_dialog.login_provide_password(TestData.incorrect_password)
        self.login_dialog.login_click_signin_button()
        assert self.login_dialog.login_dialog_is_visible_in_frame(), "Login dialog is not visible though it shall be."
        actual_disabled_login_button_text = self.login_dialog.login_get_disabled_login_button_text()
        assert actual_disabled_login_button_text == TestData.signin_button_incorrect_user_name_password_text, f"Wrong message at signin button when incorrect password provided. Current message is {actual_disabled_login_button_text} but it shall be {TestData.signin_button_incorrect_user_name_password_text}."

        # Successful login.
        self.login_dialog.login_provide_email(TestData.user_name)
        self.login_dialog.login_provide_password(TestData.password)
        self.login_dialog.login_click_signin_button()
        self.login_dialog.login_switch_back_from_login_frame()
        assert self.login_dialog.login_dialog_is_invisible_out_of_frame(), "Login dialog is still visible but shall not be."
        actual_signed_in_text = self.login_dialog.login_get_signed_in_text()
        assert actual_signed_in_text == TestData.user_signed_in_text, f"Wrong text in the top menu. Current text is {actual_signed_in_text} but shall be {TestData.user_signed_in_text}. User is not logged in though shall be?"

        # Logout.
        self.top_section.top_section_click_logout_link()
        assert self.top_section.top_section_login_link_is_visible(), "Login link is not visible, though it shall be."

    def test_basket_add_remove_item(self):
        """
        Tests adding and removing item from basket. First all cookies are rejected then logs in, adds computer to basket, then goes to basket,
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
        # Fill in credentials, login, switch back to page.
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
        # Check item name, count and price.
        actual_computer_name = self.basket.basket_get_item_name()
        assert first_computer_name in actual_computer_name, f"Wrong name of computer in basket. Actual name is {actual_computer_name} but it shall be {first_computer_name}. Computer that shall be in basket is not?"
        actual_number_of_computers_in_basket = self.basket.basket_get_item_count()
        assert actual_number_of_computers_in_basket == TestData.number_of_items_in_basket, f"Wrong number of computers in basket. There are {actual_number_of_computers_in_basket} computers but there shall be {TestData.number_of_items_in_basket} computer."
        actual_computer_price_in_basket = self.basket.basket_get_item_price()
        assert actual_computer_price_in_basket == first_computer_price, f"Wrong computer price in basket. Price is {actual_computer_price_in_basket} but shall be {first_computer_price}."
        # Remove item from basket and check it is empty.
        self.basket.basket_click_down_arrow_price()
        self.basket.basket_click_down_arrow_price_remove()
        actual_text_once_basket_empty = self.basket.basket_get_text_once_all_items_removed()
        assert actual_text_once_basket_empty == TestData.text_once_all_items_removed_from_basket, f"Wrong text once basket is empty. Text is {actual_text_once_basket_empty} but it shall be {TestData.text_once_all_items_removed_from_basket}. Basket is not empty?"

        # Logout.
        self.top_section.top_section_click_logout_link()

    def test_search(self):
        """
        Tests search functionality in 2 ways. First all cookies are rejected then logs in, provides search value, presses search button
        and checks header of result and that amount of items found is bigger than 0.
        Then provides search value, waits for suggestions to appear, clicks first article in suggestions and checks that name of article contains
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
        self.top_section.top_section_search_provide_value(TestData.search_value_via_search_button)
        self.top_section.top_section_click_search_button()
        # Check result.
        actual_search_result_title = self.main_page.main_page_get_search_result_header()
        assert actual_search_result_title == TestData.search_result_header_via_search_button, f"Wrong header of looked up section is displayed. Actual header is {actual_search_result_title} but it shall be {TestData.search_result_header_via_search_button}. Wrong section displayed?"
        assert self.main_page.main_page_get_search_result_items_amount() > 0, "0 items found."

        # Search for "recenze" and choose from suggestion:
        self.top_section.top_section_search_provide_value(TestData.search_value_via_suggestion)
        self.top_section.top_section_search_suggestion_click_1st_article()
        # Check result.
        actual_search_result_title = self.main_page.main_page_get_search_result_header().lower()
        assert TestData.search_result_word_in_title_via_suggestion in actual_search_result_title, f"Found article doesn't contain looked up word in title. Actual article title is {actual_search_result_title}, it does not contain word {TestData.search_result_word_in_title_via_suggestion}."

        # Logout.
        self.top_section.top_section_click_logout_link()

    def test_watchdog_add_remove_item(self):
        """
        Tests adding and removing item from watchdog list. First all cookies are rejected then logs in, adds watchdog to pet supply item,
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
        actual_pet_supply_name = self.my_account.my_account_watchdog_list_get_watchdog_item_name()
        assert actual_pet_supply_name == first_pet_supply_name, f"Wrong name of pet supply in watchdogs. Actual pet supply name in watchdogs is {actual_pet_supply_name} but it shall be {first_pet_supply_name}. Pet supply that shall be in watchdogs is not?"
        # Remove item from watchdog list.
        self.my_account.my_account_watchdog_list_remove_item_close_success_dialog()
        actual_text_once_watchdog_list_empty = self.my_account.my_account_watchdog_list_get_text_once_all_items_removed()
        assert actual_text_once_watchdog_list_empty == TestData.text_once_all_items_removed_from_watchdog_list, f"Wrong text once watchodg list is empty. Acutal text is {actual_text_once_watchdog_list_empty} but it shall be {TestData.text_once_all_items_removed_from_watchdog_list}. Watchdog list is not empty?"

        # Logout.
        self.top_section.top_section_click_logout_link()

    def test_additional_account_changes(self):
        """
        Tests changes of information in user account. First all cookies are rejected then logs in and navigates to user account page.
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
        actual_street_and_number = self.my_account.my_account_get_street_value()
        assert actual_street_and_number == TestData.street_and_number, f"Wrong street and number. Actual street and number is {actual_street_and_number} but it shall be {TestData.street_and_number}."
        actual_zip = self.my_account.my_account_get_zip_value()
        assert actual_zip == TestData.zip, f"Wrong zip. Actual zip is {actual_zip} but it shall be {TestData.zip}."
        actual_city = self.my_account.my_account_get_city_value()
        assert actual_city == TestData.city, f"Wrong city. Actual city is {actual_city} but it shall be {TestData.city}."

        # Clear street, zip, city.
        self.my_account.my_account_clear_street_input()
        self.my_account.my_account_clear_zip_input()
        self.my_account.my_account_clear_city_input()
        # Refresh page to refresh values for assertions.
        self.helpers.helpers_refresh_page()
        assert self.my_account.my_account_get_street_value() == "", "Street input field is not empty though it shall be."
        assert self.my_account.my_account_get_zip_value() == "", "Zip input field is not empty though it shall be."
        assert self.my_account.my_account_get_city_value() == "", "City input field is not empty though it shall be."

        # Logout.
        self.top_section.top_section_click_logout_link()