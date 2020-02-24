from SeleniumProxy.logger import get_logger, kwargstr, argstr
from .proxy2 import ProxyRequestHandler
from urllib.parse import parse_qs, urlparse
import socket
import logging
import wrapt
import json


@wrapt.decorator
def log_wrapper(wrapped, instance, args, kwargs):
    instance.logger.debug("{}({}) [ENTERING]".format(
        wrapped.__name__, ", ".join([argstr(args), kwargstr(kwargs)])))
    ret = wrapped(*args, **kwargs)
    instance.logger.debug("{}() [LEAVING]".format(wrapped.__name__))
    return ret


ADMIN_PATH = 'http://seleniumwire'


class AdminMixin:

    admin_path = ADMIN_PATH

    def admin_handler(self):
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

    def _get_request_body(self, request_id):
        body = self.server.storage.load_request_body(request_id[0])
        self._send_body(body)

    def _get_response_body(self, request_id):
        body = self.server.storage.load_response_body(request_id[0])
        self._send_body(body)

    def _send_response(self, body, content_type):
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(body))
        self.end_headers()
        if isinstance(body, str):
            body = body.encode('utf-8')
        self.wfile.write(body)


class CaptureRequestHandler(AdminMixin, ProxyRequestHandler):

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
        self.logger.debug("request_handler", request, request_body)
        self.server.storage.save_request(request, request_body)

    def response_handler(self, request, request_body, response, response_body):
        self.logger.debug("response_handler", response, response_body)

    @property
    def certdir(self):
        return self.server.storage.get_cert_dir()
