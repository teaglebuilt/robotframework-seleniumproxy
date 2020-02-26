from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumProxy.logger import get_logger, kwargstr, argstr
import wrapt


@wrapt.decorator
def log_wrapper(wrapped, instance, args, kwargs):
    instance.logger.debug("{}({}) [ENTERING]".format(
        wrapped.__name__, ", ".join([argstr(args), kwargstr(kwargs)])))
    ret = wrapped(*args, **kwargs)
    instance.logger.debug("{}() [LEAVING]".format(wrapped.__name__))
    return ret


class HTTPKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.logger = get_logger("SeleniumProxy")
        self.logger.debug("HTTPKeywords_{}".format(ctx))

    @log_wrapper
    @keyword
    def get_requests(self):
        return self.driver.requests

    @log_wrapper
    @keyword
    def wait_for_request(self, url):
        request = self.driver.wait_for_request(url)
        return request

    @log_wrapper
    @keyword
    def wait_for_response(self, url):
        response = self.driver.wait_for_response(url)
        return response
