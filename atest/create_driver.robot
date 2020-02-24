*** Settings ***
Library   SeleniumProxy
Resource  keywords.robot

*** Test Cases ***
Create Driver Instance
    Open Proxy Browser  https://www.duckduckgo.com  Chrome
    Close All Browsers
