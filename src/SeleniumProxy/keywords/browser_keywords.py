from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.keywords import BrowserManagementKeywords
from robot.api import logger
from robot.utils import is_truthy
from SeleniumProxy import webdriver
from SeleniumProxy.logger import get_logger


class BrowserKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.logger = get_logger("SeleniumProxy")
        self.logger.debug("BrowserKeywords_{}".format(ctx))
        self.manager = BrowserManagementKeywords(ctx)

    @keyword
    def open_proxy_browser(self, url=None, browser='chrome', alias=None):
        index = self.drivers.get_index(alias)
        if index:
            self.info('Using existing browser from index %s.' % index)
            self.manager.switch_browser(alias)
            if is_truthy(url):
                self.manager.go_to(url)
            return index
        return self._make_new_browser(url, browser, alias)

    @keyword
    def create_webdriver(self, driver_name, alias=None, kwargs={}, **init_kwargs):
        pass

    def _make_new_browser(self, url=None, browser='chrome', alias=None):
        logger.console(url)
        driver = self._make_driver(browser)
        logger.console(driver)
        driver = self._wrap_event_firing_webdriver(driver)
        logger.console(dir(driver))
        index = self.ctx.register_driver(driver, alias)
        if is_truthy(url):
            try:
                driver.get(url)
            except Exception:
                self.debug("Opened browser with session id %s but failed to open url '%s'." % (
                    driver.session_id, url))
                raise
        self.debug('Opened browser with session id %s.' % driver.session_id)
        return index

    def _wrap_event_firing_webdriver(self, driver):
        if not self.ctx.event_firing_webdriver:
            return driver
        self.debug('Wrapping driver to event_firing_webdriver.')
        return EventFiringWebDriver(driver, self.ctx.event_firing_webdriver())

    def _make_driver(self, browser):
        driver = webdriver.Chrome(options={'ssl_verify': False})
        driver.set_script_timeout(self.ctx.timeout)
        driver.implicitly_wait(self.ctx.implicit_wait)
        return driver
