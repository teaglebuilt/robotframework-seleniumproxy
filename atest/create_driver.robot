*** Settings ***
Library   SeleniumProxy    event_firing_webdriver=${EXECDIR}/lib/DriverListener.py
Library   RobotListener
Resource  keywords.robot


*** Test Cases ***
Create Driver Instance
    Set Selenium Timeout  15 sec
    Open Proxy Browser  https://www.duckduckgo.com  Chrome
    Wait Until Page Loads
    Close All Browsers
