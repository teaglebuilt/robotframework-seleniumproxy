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
        """Initialise a new Firefox WebDriver instance.

        Args:
            options: The seleniumproxy options dictionary.
        """
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
        self.client.destroy_proxy()
        super().quit()


class Chrome(InspectRequestsMixin, _Chrome):
    """Extends the Chrome webdriver to provide additional methods for inspecting requests."""

    def __init__(self, *args, options=None, **kwargs):
        self.logger = get_logger("SeleniumProxy")
        self.logger.info("ChromeDriver __init__")
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


class Safari(InspectRequestsMixin, _Safari):
    """Extends the Safari webdriver to provide additional methods for inspecting requests."""

    def __init__(self, options=None, *args, **kwargs):
        """Initialise a new Safari WebDriver instance.

        Args:
            options: The seleniumproxy options dictionary.
        """
        if options is None:
            options = {}

        # Safari does not support automatic proxy configuration through the
        # DesiredCapabilities API, and thus has to be configured manually.
        # Whatever port number is chosen for that manual configuration has to
        # be passed in the options.
        assert 'port' in options, 'You must set a port number in the options'

        self._client = AdminClient()
        self._client.create_proxy(
            port=options.pop('port', 0),
            proxy_config=options.pop('proxy', None),
            options=options
        )

        super().__init__(*args, **kwargs)

    def quit(self):
        self._client.destroy_proxy()
        super().quit()


class Edge(InspectRequestsMixin, _Edge):
    """Extends the Edge webdriver to provide additional methods for inspecting requests."""

    def __init__(self, options=None, *args, **kwargs):
        """Initialise a new Edge WebDriver instance.

        Args:
            options: The seleniumproxy options dictionary.
        """
        if options is None:
            options = {}

        # Edge does not support automatic proxy configuration through the
        # DesiredCapabilities API, and thus has to be configured manually.
        # Whatever port number is chosen for that manual configuration has to
        # be passed in the options.
        assert 'port' in options, 'You must set a port number in the options'

        self._client = AdminClient()
        self._client.create_proxy(
            port=options.pop('port', 0),
            proxy_config=options.pop('proxy', None),
            options=options
        )

        super().__init__(*args, **kwargs)

    def quit(self):
        self._client.destroy_proxy()
        super().quit()
