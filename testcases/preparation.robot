*** Settings ***
Documentation    Suite description
Library           Selenium2Library

*** Variables ***
${browser name}   Chrome
${headless}   TRUE
@{chrome_arguments}    --disable-infobars    --headless    --disable-gpu

*** Keywords ***
Preparation browser
    Run keyword if  '${browser name}'=='Chrome' and '${headless}'=='TRUE'  Chrome headless
    ...  ELSE IF  '${browser name}'=='Chrome' and '${headless}'=='FALSE'   Create Webdriver    Chrome
    ...  ELSE IF  '${browser name}'=='Safari' and '${headless}'=='FALSE'   Create Webdriver    Safari
    Set Selenium Implicit Wait   30 seconds
    Set Selenium Speed	 0.5 seconds

Set Chrome Options
    [Documentation]    Set Chrome options for headless mode
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    : FOR    ${option}    IN    @{chrome_arguments}
    \    Call Method    ${options}    add_argument    ${option}
    [Return]    ${options}

Chrome headless
    ${chrome_options}=    Set Chrome Options
    Create Webdriver    Chrome    chrome_options=${chrome_options}
