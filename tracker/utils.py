from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class Utils:
    def __init__(self, driver):
        self.driver = driver

    def wait(self, xpath):
        WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, xpath)))
