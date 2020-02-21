from .handler import CaptureRequestHandler
from .server import ProxyHTTPServer
from SeleniumProxy.logger import get_logger
import http.client
import json
import logging
import threading


class ProxyClient:

    def __init__(self, address=None, port=None):
        self.logger = get_logger("SeleniumProxy")
        self.logger.debug("ProxyClient__init__()")
        self.client_address = address
        self.client_port = port
        self.proxy = None
        self.proxy_address = None
        self.proxy_port = None

    def create_proxy(self, address='127.0.0.1', port=0, proxy_config=None, options=None):
        if options is None:
            options = {}
        response_handler = options.get('response_handler')
        self.capture_requests = CaptureRequestHandler
        self.proxy = ProxyHTTPServer(
            (address, port), self.capture_requests, proxy_config=proxy_config, options=options)
        t = threading.Thread(name='SeleniumProxy Server',
                             target=self.proxy.serve_forever)
        t.daemon = not options.get('standalone')
        t.start()

        socketname = self.proxy.socket.getsockname()
        self.logger.debug('Socketname {}'.format(socketname))
        self.proxy_address = socketname[0]
        self.proxy_port = socketname[1]
        return self.proxy_address, self.proxy_port

    def destroy_proxy(self):
        self.proxy.shutdown()
        self.logger.debug('Close Proxy Server')
        self.proxy.server_close()
