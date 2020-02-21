from selenium.webdriver import Chrome as _Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from SeleniumProxy.logger import get_logger
from SeleniumProxy.proxy import ProxyClient
from .request import InspectRequestMixin


class Chrome(InspectRequestMixin, _Chrome):

    def __init__(self, *args, options=None, **kwargs):
        if options is None:
            options = {}
        self.logger = get_logger("SeleniumProxy")
        self.logger.debug("Chrome__init__()")
        self.client = ProxyClient()
        addr, port = self.client.create_proxy(
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
                'noProxy': [],
            }
            capabilities['acceptInsecureCerts'] = True

            kwargs['desired_capabilities'] = capabilities
        super().__init__(*args, **kwargs)

    def quit(self):
        self.client.destroy_proxy()
        super().quit()
