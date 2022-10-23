from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

from time import sleep

url = "https://www.alza.cz/"
reject_all_button = (By.XPATH, "//a[@data-action-id-value='0']")
login_link = (By.ID, "lblLogin")
sign_in_button_active = (By.XPATH, "//button[@id='btnLogin'][not(contains(@class, 'disabled'))]")
sign_in_button_disabled = (By.XPATH, "//button[@id='btnLogin'][not(contains(@class, 'disabled'))]")
sign_in_button = (By.ID, "btnLogin")
login_frame = (By.ID, "loginIframe")
email_input = (By.XPATH, "//input[@id='userName' and not(@readonly)]")
password_input = (By.XPATH, "//input[@id='password' and not(@readonly)]")
pet_supplies_menu_item = (By.LINK_TEXT, "Chovatelské potřeby")
first_pet_supply_item_link = (By.XPATH, "(//div[@data-react-client-component='carousel'])[1]//div[@data-testid='item'][1]")
watchdog_link = (By.CLASS_NAME, "watchproduct")
street_input = (By.NAME, "street")
zip_input = (By.NAME, "zip")
city_input = (By.NAME, "city")
# watchdog_availability_checkbox = (By.XPATH, "//input[@id='chbCommodityAvailable']")
# watchdog_price_checkbox = (By.XPATH, "//input[@id='chbPriceReduction']")

user_profile_link = (By.ID, "lblUser")



watchdog_price_checkbox = (By.XPATH, "//div[@class='watchDogInfoItem priceLimit']//span[contains(@class, 'checkboxBlue')]")
watchdog_availability_checkbox = (By.XPATH, "//div[@class='watchDogInfoItem inStock']//span[contains(@class, 'checkboxBlue')]")
user_profile_link = (By.ID, "lblUser")
account_settings_dropdown = (By.XPATH, "//div[@data-testid='menuSection-MyAccount']")
my_account_list_of_watches = (By.XPATH, "//a[@data-testid='menuButton-UserWatchDog']")
my_account_menu_item = (By.XPATH, "//a[@data-testid='menuButton-UserSettings']")
watchdog_confirm_button = (By.XPATH, "//div[@id='alzaDialog'][not(contains(@style, 'none'))]//a[@id='btnConfirm']")
watchdog_success_dialog = (By.XPATH, "//div[@id='alzaDialog'][not(contains(@style, 'none'))]//div[@class='successBody']")
watchdog_success_dialog_x_close = (By.XPATH, "//div[@id='alzaDialog'][not(contains(@style, 'none'))]//div[@class='close']")

timeout = 10


driver = webdriver.Chrome()

driver.get(url)

WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(reject_all_button)).click()

WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(login_link)).click()

WebDriverWait(driver, timeout).until(EC.frame_to_be_available_and_switch_to_it(login_frame))

WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(email_input)).send_keys("wedey95103@haizail.com")

WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(password_input)).send_keys("PasHes12")

WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(sign_in_button)).click()

WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(user_profile_link)).click()

WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(account_settings_dropdown)).click()

WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(my_account_menu_item)).click()

for clear_attempt in range(3):
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(street_input)).clear()
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(zip_input)).clear()
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(city_input)).clear()

    driver.refresh()

    element_attribute_value = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(street_input)).get_attribute("value")

    if element_attribute_value == "":
        element_attribute_value = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(zip_input)).get_attribute("value")

        if element_attribute_value == "":
            element_attribute_value = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(city_input)).get_attribute("value")

            if element_attribute_value == "":
                break





# element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(pet_supplies_menu_item))
# action = ActionChains(driver)
# action.move_to_element(element).click().perform()
#
# WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(first_pet_supply_item_link)).click()
#
# WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(watchdog_link)).click()
#
# WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(watchdog_confirm_button)).click()
#
# WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(watchdog_success_dialog_x_close)).click()
#
# WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(user_profile_link)).click()
#
# WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(account_settings_dropdown)).click()
#
# WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(my_account_list_of_watches)).click()
#
# sleep(2)
#
# price = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(watchdog_price_checkbox)).is_selected()
# print(price)
#
# avail = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(watchdog_availability_checkbox)).is_selected()
# print(avail)


# assert WebDriverWait(driver, timeout).until(EC.element_located_selection_state_to_be(watchdog_availability_checkbox, True))
#
# assert WebDriverWait(driver, timeout).until(EC.element_located_selection_state_to_be(watchdog_price_checkbox, True))





