from handler import CaptureRequestHandler
from server import ProxyHTTPServer
from robot.api import logger
import http.client
import json
import logging
import threading


class ProxyClient:

    def __init__(self, address, port):
        self.client_address = address
        self.client_port = port
        self.proxy = None
        self.proxy_address = None
        self.proxy_port = None

    def create_proxy(self, address='127.0.0.1', port=0, config=None, options=None):
       if options is None:
           options = {}
        response_handler = options.get('response_handler')
        self.capture_requests = CaptureRequestHandler
        print(self.capture_requests)
        logger.console(dir(self.capture_requests))
        # self.proxy = ProxyHTTPServer((address, port))
    
    def destroy_proxy(self):
        self.proxy.shutdown()
        self.proxy.server_close()
