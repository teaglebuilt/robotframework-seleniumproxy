*** Settings ***
Library   SeleniumProxy    
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
    ${scopes}=  Create List  .*python.*
    ${false}=  Convert To Boolean  False
    Set To Dictionary  ${options}  ssl_verify  ${false}
    Set To Dictionary  ${options}  scopes  ${scopes}
    Log  ${options}
    Open Proxy Browser  https://www.python.org  Chrome  ${options}
    Wait Until Page Loads