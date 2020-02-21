from SeleniumProxy.logger import get_logger, kwargstr, argstr
from .proxy2 import ProxyRequestHandler
from urllib.parse import parse_qs, urlparse
import socket
import logging
import wrapt


@wrapt.decorator
def log_wrapper(wrapped, instance, args, kwargs):
    instance.logger.debug("{}({}) [ENTERING]".format(
        wrapped.__name__, ", ".join([argstr(args), kwargstr(kwargs)])))
    ret = wrapped(*args, **kwargs)
    instance.logger.debug("{}() [LEAVING]".format(wrapped.__name__))
    return ret


class ClientMixin:

    def client_handler(self):
        parse_result = urlparse(self.path)
        path, params = parse_result.path, parse_qs(parse_result.query)

        if path == '/requests':
            if self.command == 'GET':
                self._get_requests()
        else:
            raise RuntimeError(
                'No handler configured for: {} {}'.format(self.command, self.path))

    def _get_requests(self):
        self._send_response(json.dumps(self.server.storage.load_requests()).encode(
            'utf-8'), 'application/json')


class CaptureRequestHandler(ClientMixin, ProxyRequestHandler):

    def __init__(self, *args, **kwargs):
        self.logger = get_logger("SeleniumProxy")
        self.logger.debug("CaptureRequestHandler __init__")
        try:
            super().__init__(*args, **kwargs)
        except (ConnectionError, socket.timeout, FileNotFoundError) as e:
            if self.server.options.get('suppress_connection_errors', True):
                log.debug(str(e))
            else:
                raise e

    @log_wrapper
    def request_handler(self, request, request_body):
        self.logger.debug(request, request_body)
        self.server.storage.save_request(request, request_body)

    @property
    def certdir(self):
        return self.server.storage.get_cert_dir()
