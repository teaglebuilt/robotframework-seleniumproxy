from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.keywords import BrowserManagementKeywords
from robot.api import logger
from SeleniumProxy import webdriver


class BrowserKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.manager = BrowserManagementKeywords(ctx)

    @keyword
    def open_browser(self, host):
        logger.console("host", host)
        webdriver.Chrome()
        

    @keyword
    def create_webdriver(self, driver_name, alias=None, kwargs={}, **init_kwargs):
        pass