import pytest

from selenium import webdriver

from Config.test_data import TestData


@pytest.fixture
def initialize_driver(request):
    driver = webdriver.Chrome()
    driver.get(TestData.url)
    request.cls.driver = driver
    yield
    driver.quit()