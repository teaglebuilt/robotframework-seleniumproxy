*** Settings ***
Library   SeleniumProxy    
Resource  keywords.robot
Library  Collections
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

Test Set Scope
    Set Selenium Timeout  15 sec
    ${options}=  Create Dictionary
    ${scopes}=  Create List  .*python.*  
    ${false}=  Convert To Boolean  False
    Set To Dictionary  ${options}  ssl_verify  ${false}
    Log  ${options}
    Open Proxy Browser  https://python.org  Chrome  ${options}
    Set Scope  ${scopes}
    Wait Until Page Loads
    Get Requests


*** Keywords ***
Setup Test Environment
    Set Selenium Timeout  15 sec
    Open Proxy Browser  https://www.python.org  Chrome
    Wait Until Page Loads
