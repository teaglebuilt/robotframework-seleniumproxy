from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.keywords import BrowserManagementKeywords
from selenium.webdriver.support.events import EventFiringWebDriver
from robot.utils import is_truthy
from SeleniumProxy import webdriver
from SeleniumProxy.logger import get_logger, kwargstr, argstr
import wrapt


@wrapt.decorator
def log_wrapper(wrapped, instance, args, kwargs):
    instance.logger.debug("{}({}) [ENTERING]".format(
        wrapped.__name__, ", ".join([argstr(args), kwargstr(kwargs)])))
    ret = wrapped(*args, **kwargs)
    instance.logger.debug("{}() [LEAVING]".format(wrapped.__name__))
    return ret


class BrowserKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.logger = get_logger("SeleniumProxy")
        self.logger.debug("BrowserKeywords_{}".format(ctx))
        self.manager = BrowserManagementKeywords(ctx)

    @log_wrapper
    @keyword
    def open_proxy_browser(self, url=None, browser='chrome', proxy_options=None, alias=None):
        """Open Browser.
        The ``url`` is the address you wish to open the browser with.  https://google.com
        The ``browser`` argument is the browser type you wish to run. Chrome or Firefox

        ``proxy_settings`` parameter is optional and if provided, it must be a dictionary.
        Optional Settings:

        If the site you are testing uses a self-signed certificate then you must set the verify_ssl option to False
        ```
        {
            'verify_ssl': False
        }
        ```

        The number of seconds Selenium Wire should wait before timing out requests.

        ```
        {
            'connection_timeout': None  # Never timeout
        }
        ```

        If the site you are testing sits behind a proxy server you can tell Selenium Wire about that proxy server in the options you pass to the webdriver instance. The configuration takes the following format:

        ```
        {
        'proxy': {
            'http': 'http://username:password@host:port',
            'https': 'https://username:password@host:port',
            'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
            }
        }
        ```



        Example:
        | `Open Proxy Browser` | https://duckduckgo.com | Chrome |  ${proxy_dict_options}
        """
        index = self.drivers.get_index(alias)
        if index:
            self.info('Using existing browser from index %s.' % index)
            self.manager.switch_browser(alias)
            if is_truthy(url):
                self.manager.go_to(url)
            return index
        return self._make_new_browser(url, browser, proxy_options, alias)

    @keyword
    def create_webdriver(self, driver_name, alias=None, kwargs={}, **init_kwargs):
        pass

    def _make_new_browser(self, url, browser, proxy_options, alias=None):
        driver = self._make_proxy_driver(browser, proxy_options)
        driver = self._wrap_event_firing_webdriver(driver)
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

    @log_wrapper
    def _make_proxy_driver(self, browser, proxy_options):
        if browser == 'Chrome':
            driver = webdriver.Chrome(options=proxy_options)
        elif browser == 'Firefox':
            driver = webdriver.Firefox(options=proxy_options)
        else:
            raise Exception("Browser Type Not Available")
        driver.set_script_timeout(self.ctx.timeout)
        driver.implicitly_wait(self.ctx.implicit_wait)
        return driver
