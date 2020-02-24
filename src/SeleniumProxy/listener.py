from SeleniumProxy.logger import get_logger, kwargstr, argstr
from SeleniumLibrary import SeleniumLibrary
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.support.events import AbstractEventListener
import wrapt


@wrapt.decorator
def log_wrapper(wrapped, instance, args, kwargs):
    instance.logger.debug("{}({}) [ENTERING]".format(
        wrapped.__name__, ", ".join([argstr(args), kwargstr(kwargs)])))
    ret = wrapped(*args, **kwargs)
    instance.logger.debug("{}() [LEAVING]".format(wrapped.__name__))
    return ret


class SeleniumProxyListener(AbstractEventListener):

    def __init__(self):
        AbstractEventListener.__init__(self)
        self.instance = self._get_sl()
        self.logger = get_logger("SeleniumProxyListener")
        self.logger.debug("__init__()")

    def _get_sl(self):
        libraries = BuiltIn().get_library_instance(all=True)
        for library in libraries:
            if isinstance(libraries[library], SeleniumLibrary):
                return libraries[library]
        return None

    @log_wrapper
    def before_navigate_to(self, url, driver):
        self.logger.debug(url, driver.requests)

    @log_wrapper
    def after_click(self, url, driver):
        self.logger.debug(url, driver.requests)
