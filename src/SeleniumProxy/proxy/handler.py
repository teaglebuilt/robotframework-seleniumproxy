from .proxy2 import ProxyRequestHandler
import socket
import logging

log = logging.getLogger(__name__)


class CaptureRequestHandler(ProxyRequestHandler):

    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
        except (ConnectionError, socket.timeout, FileNotFoundError) as e:
            if self.server.options.get('suppress_connection_errors', True):
                log.debug(str(e))
            else:
                raise e

    def request_handler(self, request, request_body):
        log.info(request, request_body)

    @property
    def certdir(self):
        return self.server.storage.get_cert_dir()
