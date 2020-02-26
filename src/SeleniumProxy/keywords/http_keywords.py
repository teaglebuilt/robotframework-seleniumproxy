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
        """
        Get all Requests as a list upon arrival to path.
        """
        return self.driver.requests

    @log_wrapper
    @keyword
    def wait_for_request(self, url, timeout=10):
        """"
        Wait for a request by the url address/path
        ``url`` https://duckduckgo.com
        ``timeout`` default is 10 seconds
        Example:
        | Wait For Request | https://duckduckgo.com | timeout=30
        """
        request = self.driver.wait_for_request(url, timeout)
        return request

    @log_wrapper
    @keyword
    def wait_for_response(self, url):
        """"
        Wait for a request by the url address/path
        ``url`` https://duckduckgo.com
        ``timeout`` default is 10 seconds
        Example:
        | Wait For Response | https://python.org/about | timeout=30
        """
        response = self.driver.wait_for_response(url)
        return response
