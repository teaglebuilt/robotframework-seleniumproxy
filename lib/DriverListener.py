from SeleniumLibrary import SeleniumLibrary
from robot.api import logger
from selenium.webdriver.support.events import AbstractEventListener


class DriverListener(AbstractEventListener):

    def __init__(self):
        AbstractEventListener.__init__(self)

    def before_navigate_to(self, url, driver):
        logger.console("before navigate '%s'" % driver.requests)

    def after_click(self, url, driver):
        logger.console("after click '%s'" % driver.requests)

    def before_close(self, url, driver):
        logger.console("before close '%s'" % driver.requests)

    def after_close(self, url, driver):
        logger.console("after close '%s'" % driver.requests)
