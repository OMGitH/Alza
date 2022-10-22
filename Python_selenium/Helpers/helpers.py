# This class contains helper methods.

class Helpers:
    # Initialization.
    def __init__(self, driver):
        self.driver = driver

    def helpers_refresh_page(self):
        self.driver.refresh()



