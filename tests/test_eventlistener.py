from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener
from selenium.common.exceptions import NoSuchElementException
from SeleniumProxy import webdriver
import unittest


class Listener(AbstractEventListener, unittest.TestCase):

    def on_exception(self, exception, driver):
        self.assertIsInstance(driver, webdriver.Chrome)
        self.assertIsNotNone(driver.requests)


class TestListener(unittest.TestCase):

    def test_driver(self):
        driver = webdriver.Chrome(options={'ssl_verify': False})
        driver = EventFiringWebDriver(driver, Listener())
        driver.get("https://duckduckgo.com")
        try:
            driver.find_element_by_css_selector("div.that-does-not-exist")
        except NoSuchElementException:
            return True
        driver.quit()
