from selenium.webdriver.support.events import AbstractEventListener
from SeleniumProxy.logger import get_logger, kwargstr, argstr
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
        self.logger = get_logger("SeleniumProxy")
        self.logger.debug("Listener")
        AbstractEventListener.__init__(self)

    @log_wrapper
    def before_navigate_to(self, url, driver):
        self.logger.debug(url, driver.requests)

    @log_wrapper
    def after_click(self, url, driver):
        self.logger.debug(url, driver.requests)
