from proxy2 import ProxyRequestHandler
import socket


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
        print(request, request_body)
