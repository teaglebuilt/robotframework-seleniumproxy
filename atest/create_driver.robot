*** Settings ***
Library  SeleniumProxy


*** Test Cases ***
Create Driver Instance
    Open Proxy Browser  https://www.duckduckgo.com  Chrome
    Close All Browsers