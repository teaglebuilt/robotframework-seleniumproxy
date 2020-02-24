from SeleniumProxy import webdriver
from unittest import TestCase
import logging


logging.basicConfig(level=logging.DEBUG)


class BrowserIntegrationTest(TestCase):

    def test_chrome_can_access_requests(self):
        url = 'https://cardatonce.eftsource.com/'
        driver = webdriver.Chrome(seleniumwire_options={'ssl_verify': False})
        driver.get(url)

        request = driver.requests

        self.assertEqual(request.response.status_code, 200)
        self.assertIn('text/html', request.response.headers['Content-Type'])

        driver.quit()
