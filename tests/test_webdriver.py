from SeleniumProxy.webdriver.request import Request, Response, InspectRequestsMixin
from unittest.mock import call, Mock
from unittest import TestCase
import uuid


class Driver(InspectRequestsMixin):
    def __init__(self, client):
        self._client = client

class TestRequestMixins(TestCase):

    def setUp(self):
        self.mock_client = Mock()
        self.driver = Driver(self.mock_client)

    def test_last_request(self):
        self.mock_client.get_last_request.return_value = {
            'id': '98765',
            'method': 'GET',
            'path': 'http://www.example.com/different/path?foo=bar',
            'headers': {
                'Accept': '*/*',
                'Host': 'www.example.com'
            },
            'response': {
                'status_code': 200,
                'reason': 'OK',
                'headers': {
                    'Content-Type': 'text/plain',
                    'Content-Length': '98425'
                }
            }
        }

        last_request = self.driver.last_request

        self.mock_client.get_last_request.assert_called_once_with()
        self.assertEqual(last_request.path, 'http://www.example.com/different/path?foo=bar')
        self.assertEqual(last_request.response.headers['Content-Length'], '98425')
    
    def test_last_request_none(self):
        self.mock_client.get_last_request.return_value = None

        last_request = self.driver.last_request

        self.mock_client.get_last_request.assert_called_once_with()
        self.assertIsNone(last_request)

    def test_set_scopes(self):
        mock_client = Mock()
        driver = Driver(mock_client)
        scopes = [
            '.*stackoverflow.*',
            '.*github.*'
        ]
        driver.scopes = scopes
        mock_client.set_scopes.assert_called_once_with(scopes)

    def test_get_scopes(self):
        mock_client = Mock()
        driver = Driver(mock_client)
        driver.scopes
        mock_client.get_scopes.assert_called_once_with()
