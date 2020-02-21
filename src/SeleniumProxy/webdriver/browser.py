from selenium.webdriver import Chrome as _Chrome
from robot.api import logger


class Chrome(_Chrome):

    def __init__(self, *args, options=None, **kwargs):
        if options is None:
            options = {}
        self.client = ProxyClient()
        logger.console(dir(self.client))
        super().__init__(*args, **kwargs)

    def quit(self):
        super().quit()
