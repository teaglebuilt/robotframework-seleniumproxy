from selenium.webdriver.support.events import AbstractEventListener
from robot.api import logger


class SeleniumProxyListener(AbstractEventListener):

    def __init__(self):
        AbstractEventListener.__init__(self)

    def before_navigate_to(self, url, driver):
        logger.debug(url, driver.requests)

    def after_click(self, url, driver):
        logger.debug(url, driver.requests)
