from selenium.webdriver.common.by import By
from Page_objects.base_page import BasePage


class LoginDialog(BasePage):
    # Identification of objects on login dialog.
    login_frame = (By.ID, "loginIframe")
    email_input = (By.XPATH, "//input[@id='userName' and not(@readonly)]")
    password_input = (By.XPATH, "//input[@id='password' and not(@readonly)]")
    sign_in_button_active = (By.XPATH, "//button[@id='btnLogin'][not(contains(@class, 'disabled'))]")
    sign_in_button_disabled = (By.XPATH, "//button[@id='btnLogin'][not(contains(@class, 'disabled'))]")
    signed_in_user_text = (By.ID, "lblUser")
    login_dialog_out_of_frame = (By.XPATH, "//div[@data-testid='alzaDialog']")
    login_dialog_in_frame = (By.CLASS_NAME, "login-body")
    provide_email_text = (By.XPATH, "//label[@for='userName']/parent::div/span")
    provide_password_text = (By.XPATH, "//label[@for='password']/parent::div/span")

    # Initialization.
    def __init__(self, driver):
        super().__init__(driver)

    # Actions on login dialog.
    def login_switch_to_login_frame(self):
        self.base_switch_to_frame(self.login_frame)

    def login_provide_email(self, username):
        self.base_clear_input(self.email_input)
        self.base_send_keys(self.email_input, username)

    def login_provide_password(self, password):
        self.base_clear_input(self.password_input)
        self.base_send_keys(self.password_input, password)

    def login_click_signin_button(self):
        self.base_click(self.sign_in_button_active)

    def login_switch_back_from_login_frame(self):
        self.base_switch_back_from_frame()

    def login_dialog_is_visible_in_frame(self):
        flag = self.base_is_visible(self.login_dialog_in_frame)
        return flag

    def login_dialog_is_invisible_out_of_frame(self):
        flag = self.base_is_invisible(self.login_dialog_out_of_frame)
        return flag

    def login_get_blank_email_text(self):
        if self.base_is_visible(self.provide_email_text):
            email_text = self.base_get_element_text(self.provide_email_text)
            return email_text

    def login_get_blank_password_text(self):
        if self.base_is_visible(self.provide_password_text):
            password_text = self.base_get_element_text(self.provide_password_text)
            return password_text

    def login_get_disabled_login_button_text(self):
        if self.base_is_visible(self.sign_in_button_disabled):
            disabled_button_text = self.base_get_element_text(self.sign_in_button_disabled)
            return disabled_button_text

    def login_get_signed_in_text(self):
        if self.base_is_visible(self.signed_in_user_text):
            signed_in_user_text = self.base_get_element_text(self.signed_in_user_text)
            return signed_in_user_text

    def login_successful_login(self, username, password):
        self.base_switch_to_frame(self.login_frame)
        self.base_clear_input(self.email_input)
        self.base_send_keys(self.email_input, username)
        self.base_clear_input(self.password_input)
        self.base_send_keys(self.password_input, password)
        self.base_click(self.sign_in_button_active)
        self.base_switch_back_from_frame()
        self.base_is_invisible(self.login_dialog_out_of_frame)