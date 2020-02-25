from robot.api import logger
import robot


class RobotListener(object):

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    def _end_suite(self, name, attrs):
        logger.info(str(attrs), also_console=True)
