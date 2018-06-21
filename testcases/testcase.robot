*** Settings ***
Library     Selenium2Library
Library     ../lib/fileParser.py
Library     ../lib/kafkaMessage.py
Library     ../lib/couchbaseCheck.py

*** Test Cases ***
Initialize Browser To Upload
    Open Browser To Upload File
Check And Match SKU
    Match SKU File With Kafka
    Match SKU File With Couchbase

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

Match SKU File With Kafka
    ${sku}                          Read SKU File                   /home/budiman/Documents/automation/SKU.xlsx
    Set Global Variable             ${sku}
    ${messages}                     Get Topic Messages              SkuCreateRequested              10.99.143.96:9092
    ${result}                       Match File With Kafka           ${sku}                          ${messages}
    Run Keyword If                  '${result}' == 'False'          Log                             SKU Does not exist in Kafka                     ERROR
    ...                             ELSE    Log                     Passed

Match SKU File With Couchbase
    ${cb}=                          Check In Couchbase              ${sku}
    Run Keyword If                  '${cb}' == 'False'              Log                             SKU Does not exist in Couchbase Server          ERROR
    ...                             ELSE    Log                     Passed