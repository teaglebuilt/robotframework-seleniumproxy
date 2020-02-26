*** Settings ***
Library   SeleniumProxy    event_firing_webdriver=${EXECDIR}/lib/DriverListener.py
Library   RobotListener
Resource  keywords.robot

Test Teardown  Close All Browsers


*** Test Cases ***
Create Driver Instance
    Setup Test Environment

Get Requests
    Setup Test Environment
    ${r}=  Get Requests
    Log  ${r}

Wait For Requests
    Setup Test Environment
    Wait For Request  https://www.python.org

Wait For Response
    Setup Test Environment
    Click Element  //*[@id="about"]/a
    Wait For Response  https://www.python.org/about


*** Keywords ***
Setup Test Environment
    Set Selenium Timeout  15 sec
    Open Proxy Browser  https://www.python.org  Chrome
    Wait Until Page Loads
