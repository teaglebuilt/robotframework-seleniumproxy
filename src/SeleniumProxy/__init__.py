from SeleniumLibrary import SeleniumLibrary
from SeleniumProxy.keywords import BrowserKeywords
from .logger import get_logger


class SeleniumProxy(SeleniumLibrary):

    def __init__(self, timeout=5.0, implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None, plugins=None,
                 event_firing_webdriver=None):
        SeleniumLibrary.__init__(self, timeout=5.0, implicit_wait=0.0,
                                 run_on_failure='Capture Page Screenshot',
                                 screenshot_root_directory=None, plugins=None,
                                 event_firing_webdriver=None)
        self.logger = get_logger("SeleniumProxy")
        self.logger.debug("__init__()")
        self.add_library_components([BrowserKeywords(self)])
