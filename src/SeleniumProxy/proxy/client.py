from .handler import CaptureRequestHandler, ADMIN_PATH
from .server import ProxyHTTPServer
from SeleniumProxy.logger import get_logger, kwargstr, argstr
import http.client
import json
import logging
import threading
import wrapt


@wrapt.decorator
def log_wrapper(wrapped, instance, args, kwargs):
    instance.logger.debug("{}({}) [ENTERING]".format(
        wrapped.__name__, ", ".join([argstr(args), kwargstr(kwargs)])))
    ret = wrapped(*args, **kwargs)
    instance.logger.debug("{}() [LEAVING]".format(wrapped.__name__))
    return ret


class ProxyClient:

    def __init__(self, address=None, port=None):
        self.logger = get_logger("SeleniumProxy")
        self.logger.debug("ProxyClient__init__()")
        self.client_address = address
        self.client_port = port
        self.proxy = None
        self.proxy_address = None
        self.proxy_port = None

    @log_wrapper
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

    @log_wrapper
    def get_requests(self):
        return self._make_request('GET', '/requests')

    @log_wrapper
    def destroy_proxy(self):
        self.proxy.shutdown()
        self.proxy.server_close()

    @log_wrapper
    def _make_request(self, command, path, data=None):
        url = "{}{}".format(ADMIN_PATH, path)
        connection = http.client.HTTPConnection(
            self.proxy_address, self.proxy_port)
        args = {}
        if data is not None:
            args['body'] = json.dumps(data).encode('utf-8')

        connection.request(command, url, **args)
        try:
            response = connection.getresponse()
            if response.status != 200:
                raise ProxyException(
                    'Proxy returned status code {} for {}'.format(response.status, url))
            data = response.read()
            try:
                if response.getheader('Content-Type') == 'application/json':
                    data = json.loads(data.decode(encoding='utf-8'))
            except (UnicodeDecodeError, ValueError):
                pass
            return data
        except ProxyException:
            raise
        except Exception as e:
            raise ProxyException(
                'Unable to retrieve data from proxy: {}'.format(e))
        finally:
            try:
                connection.close()
            except ConnectionError:
                pass


class ProxyException(Exception):
    """Error communcating with proxy server"""
