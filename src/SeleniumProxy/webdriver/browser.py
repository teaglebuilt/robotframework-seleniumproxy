from selenium.webdriver import Chrome as _Chrome
from selenium.webdriver import Edge as _Edge
from selenium.webdriver import Firefox as _Firefox
from selenium.webdriver import Safari as _Safari
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from SeleniumProxy.logger import get_logger, argstr, kwargstr
from SeleniumProxy.proxy.client import AdminClient
from .request import InspectRequestsMixin
import wrapt


@wrapt.decorator
def log_wrapper(wrapped, instance, args, kwargs):
    instance.logger.debug("{}({}) [ENTERING]".format(
        wrapped.__name__, ", ".join([argstr(args), kwargstr(kwargs)])))
    ret = wrapped(*args, **kwargs)
    instance.logger.debug("{}() [LEAVING]".format(wrapped.__name__))
    return ret


class Firefox(InspectRequestsMixin, _Firefox):
    """Extends the Firefox webdriver to provide additional methods for inspecting requests."""

    def __init__(self, *args, options=None, **kwargs):
        self.logger = get_logger("SeleniumProxy")
        self.logger.info("GeckoDriver __init__")
        if options is None:
            options = {}

        self._client = AdminClient()
        addr, port = self._client.create_proxy(
            port=options.pop('port', 0),
            proxy_config=options.pop('proxy', None),
            options=options
        )

        if 'port' not in options:  # Auto config mode
            try:
                capabilities = kwargs.pop('desired_capabilities')
            except KeyError:
                capabilities = DesiredCapabilities.FIREFOX.copy()

            capabilities['proxy'] = {
                'proxyType': 'manual',
                'httpProxy': '{}:{}'.format(addr, port),
                'sslProxy': '{}:{}'.format(addr, port),
                'noProxy': [],
            }
            capabilities['acceptInsecureCerts'] = True

            kwargs['capabilities'] = capabilities

        super().__init__(*args, **kwargs)

    def quit(self):
        self._client.destroy_proxy()
        super().quit()


class Chrome(InspectRequestsMixin, _Chrome):
    """Extends the Chrome webdriver to provide additional methods for inspecting requests."""

    def __init__(self, *args, options=None, **kwargs):
        self.logger = get_logger("SeleniumProxy")
        self.logger.info("ChromeDriver __init__")
        self.logger.info("options {} {} {}".format(options, argstr(args), kwargstr(kwargs)))
        if options is None:
            options = {}

        self._client = AdminClient()
        addr, port = self._client.create_proxy(
            port=options.pop('port', 0),
            proxy_config=options.pop('proxy', None),
            options=options
        )

        if 'port' not in options:  # Auto config mode
            try:
                capabilities = kwargs.pop('desired_capabilities')
            except KeyError:
                capabilities = DesiredCapabilities.CHROME.copy()

            capabilities['proxy'] = {
                'proxyType': 'manual',
                'httpProxy': '{}:{}'.format(addr, port),
                'sslProxy': '{}:{}'.format(addr, port),
                'noProxy': ''
            }
            capabilities['acceptInsecureCerts'] = True

            kwargs['desired_capabilities'] = capabilities

        super().__init__(*args, **kwargs)

    def quit(self):
        self._client.destroy_proxy()
        super().quit()
