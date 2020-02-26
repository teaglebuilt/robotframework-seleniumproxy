*** Settings ***
Library   SeleniumProxy    event_firing_webdriver=${EXECDIR}/lib/DriverListener.py
Library   Collections
Library   BuiltIn
Resource  keywords.robot

Test Teardown  Close All Browsers


*** Test Cases ***
Create Chrome Driver Instance
    Set Selenium Timeout  15 sec
    Open Proxy Browser  https://www.python.org  Chrome
    Wait Until Page Loads

Create Firefox Driver Instance
    Set Selenium Timeout  15 sec
    Open Proxy Browser  https://www.python.org  Firefox
    Wait Until Page Loads

Create Chrome Driver With Options
    Set Selenium Timeout  15 sec
    ${options}=  Create Dictionary
    ${false}=  Convert To Boolean  True
    Set To Dictionary  ${options}  ssl_verify  ${false}
    Log  ${options}
    Open Proxy Browser  https://www.python.org  Chrome  ${options}
    Wait Until Page Loads