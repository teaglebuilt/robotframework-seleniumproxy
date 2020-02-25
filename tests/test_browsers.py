from SeleniumProxy import webdriver
from unittest import TestCase
import logging


logging.basicConfig(level=logging.DEBUG)


class BrowserIntegrationTest(TestCase):

    def test_chrome_can_access_requests(self):
        url = 'https://duckduckgo.com/'
        driver = webdriver.Chrome(options={'ssl_verify': False})
        driver.get(url)

        request = driver.wait_for_request(url)

        self.assertEqual(request.response.status_code, 200)
        self.assertIn('text/html', request.response.headers['Content-Type'])

        driver.quit()
