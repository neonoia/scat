*** Settings ***
Library     Selenium2Library
Library     ../lib/fileParser.py

*** Test Cases ***
QA Test Automation
    Open Browser To Upload File
    Check Uploaded File

*** Keywords ***
Open Browser to Upload File
    Open Browser                    http://10.99.143.80:8080/       browser=chrome
    Choose File To Be Uploaded
    Upload File

Choose File To Be Uploaded
    Page Should Contain Button      xpath://*[@id="file"]
    Choose File                     xpath://*[@id="file"]           /home/budiman/Documents/automation/SKU.xlsx

Upload File
    Page Should Contain Button      xpath://*[@id="myButton"]
    # Click Element                   xpath://*[@id="myButton"]

Check Uploaded File
    ${sku}=                Read SKU File       /home/budiman/Documents/automation/SKU.csv
    Log To Console         ${sku}