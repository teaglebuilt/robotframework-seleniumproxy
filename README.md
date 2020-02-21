# SeleniumProxy

A library for RobotFramework that extends SeleniumLibrary.

SeleniumProxy inherits seleniums webdriver and captures all network activity generated by the webdriver. The webdriver stores data in a class with added keywords to interact with requests and responses.

Proxy Server is launched in the background with a proxy client added to the webdriver class that adds the methods needed to interact with the proxy server at run time.