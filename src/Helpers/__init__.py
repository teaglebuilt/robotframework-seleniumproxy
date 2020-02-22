from psutil import Process, wait_procs, NoSuchProcess
from robotlibcore import DynamicCore, keyword
from robot.api import logger


class Helpers(DynamicCore):

    def __init__(self):
        DynamicCore.__init__(self, [])

    @keyword
    def kill_process(self, parent):
        if isinstance(parent, int):
            try:
                par = Process(parent)
                logger.console(par)
            except NoSuchProcess:
                self.warn("Unable to kill process id:{}".format(parent))
                return
        else:
            par = parent
        for child_process in par.children():
