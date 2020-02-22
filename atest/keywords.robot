*** Settings ***
Library         Process


*** Keywords ***
Kill Proxy Server
    ${pid}=  Get Process Object  chromedri
    Log  ${pid} 
    